import os
import hashlib
import json
from typing import Dict, List, Any
import cv2
import numpy as np
from PIL import Image

from app.services.image_quality import image_quality_analyzer
from app.services.ocr_service import ocr_service
from app.services.declaration_service import declaration_extractor
from app.services.rule_engine import rule_engine

class DatasetPipeline:
    """
    Ingestion, validation, and audit pipeline for the official SIH26034 Legal Metrology
    packaging commodity dataset (including converted Google Drive images).
    """

    def __init__(self, dataset_dir: str = None):
        if dataset_dir is None:
            candidates = [
                os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "dataset_images"),
                os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "dataset_images"),
                os.path.abspath("dataset_images"),
                os.path.abspath("../dataset_images"),
                os.path.abspath("SIH-34-main/dataset_images"),
            ]
            for c in candidates:
                if os.path.exists(c):
                    self.dataset_dir = c
                    break
            else:
                self.dataset_dir = candidates[1]
        else:
            self.dataset_dir = dataset_dir

    def calculate_file_hash(self, file_path: str) -> str:
        hasher = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

    def audit_dataset(self) -> Dict[str, Any]:
        """
        Scans all dataset images, checks for corruption, detects duplicates,
        computes image metrics, and produces an audit summary.
        """
        if not os.path.exists(self.dataset_dir):
            return {"error": f"Dataset directory {self.dataset_dir} does not exist"}

        files = [
            f for f in os.listdir(self.dataset_dir)
            if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp", ".heic"))
        ]

        seen_hashes: Dict[str, str] = {}
        duplicates: List[Dict[str, str]] = []
        corrupted_files: List[str] = []
        valid_records: List[Dict[str, Any]] = []

        total_files = len(files)
        sharpness_list: List[float] = []
        quality_scores: List[float] = []

        for f in sorted(files):
            file_path = os.path.join(self.dataset_dir, f)
            # 1. Hash & Duplicate Check
            file_hash = self.calculate_file_hash(file_path)
            if file_hash in seen_hashes:
                duplicates.append({
                    "original": seen_hashes[file_hash],
                    "duplicate": f,
                    "hash": file_hash
                })
            else:
                seen_hashes[file_hash] = f

            # 2. Corruption & Image Metric Check
            try:
                img = cv2.imread(file_path)
                if img is None:
                    corrupted_files.append(f)
                    continue

                h, w = img.shape[:2]
                quality = image_quality_analyzer.analyze(file_path)
                sharpness_list.append(quality["sharpness_score"])
                quality_scores.append(quality["quality_score"])

                valid_records.append({
                    "filename": f,
                    "dimensions": f"{w}x{h}",
                    "width": w,
                    "height": h,
                    "quality_score": round(quality["quality_score"], 3),
                    "sharpness": round(quality["sharpness_score"], 2),
                    "blur": quality["blur"],
                    "glare": quality["glare"],
                    "is_empty": quality["is_empty"]
                })
            except Exception:
                corrupted_files.append(f)

        summary = {
            "dataset_directory": self.dataset_dir,
            "total_images_scanned": total_files,
            "valid_images": len(valid_records),
            "corrupted_images_count": len(corrupted_files),
            "corrupted_files": corrupted_files,
            "duplicate_count": len(duplicates),
            "duplicates": duplicates,
            "mean_quality_score": round(float(np.mean(quality_scores)), 3) if quality_scores else 0.0,
            "mean_sharpness_variance": round(float(np.mean(sharpness_list)), 2) if sharpness_list else 0.0,
            "records": valid_records
        }

        # Save audit report to backend storage
        storage_report_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "storage"
        )
        os.makedirs(storage_report_dir, exist_ok=True)
        report_path = os.path.join(storage_report_dir, "dataset_audit_report.json")
        try:
            with open(report_path, "w", encoding="utf-8") as rf:
                json.dump(summary, rf, indent=2)
            summary["saved_report_path"] = report_path
        except Exception as e:
            summary["save_error"] = str(e)

        return summary

    def test_sample_pipeline(self, max_samples: int = 5) -> List[Dict[str, Any]]:
        """
        Runs sample dataset images through the complete OCR -> Declarations -> Rule Engine pipeline.
        """
        if not os.path.exists(self.dataset_dir):
            return []

        files = sorted([
            f for f in os.listdir(self.dataset_dir)
            if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
        ])[:max_samples]

        pipeline_results = []

        for f in files:
            path = os.path.join(self.dataset_dir, f)
            quality = image_quality_analyzer.analyze(path)
            spans = ocr_service.extract_text(path, surface_type="FRONT")
            decls = declaration_extractor.extract_from_spans(spans)

            images_meta = [{
                "surface_type": "FRONT",
                "quality_score": quality["quality_score"],
                "blur": quality["blur"],
                "glare": quality["glare"],
                "is_empty": quality["is_empty"]
            }]

            compliance = rule_engine.evaluate_inspection(decls, images_meta)
            outcome = rule_engine.compute_overall_outcome(compliance)

            pipeline_results.append({
                "image": f,
                "quality_score": quality["quality_score"],
                "ocr_spans_detected": len(spans),
                "declarations_extracted": len(decls),
                "extracted_fields": [d["field_name"] for d in decls],
                "compliance_violations_count": len([c for c in compliance if c["outcome"] == "POSSIBLE_NON_COMPLIANCE"]),
                "overall_outcome": outcome
            })

        return pipeline_results

dataset_pipeline = DatasetPipeline()
