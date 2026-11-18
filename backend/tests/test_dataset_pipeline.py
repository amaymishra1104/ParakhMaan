import os
import pytest
from app.services.dataset_pipeline import dataset_pipeline

def test_dataset_audit_pipeline():
    audit = dataset_pipeline.audit_dataset()
    assert "total_images_scanned" in audit
    assert audit["total_images_scanned"] >= 10
    assert audit["valid_images"] > 0
    assert audit["corrupted_images_count"] == 0
    assert "saved_report_path" in audit
    assert os.path.exists(audit["saved_report_path"])

def test_dataset_sample_inspection_pipeline():
    results = dataset_pipeline.test_sample_pipeline(max_samples=2)
    assert len(results) == 2
    for res in results:
        assert "quality_score" in res
        assert "overall_outcome" in res
        assert res["overall_outcome"] in ["PASS", "REVIEW", "POSSIBLE_NON_COMPLIANCE"]
