import os
import pytest
import numpy as np
import cv2
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.core.database import SessionLocal
from app.models.all_models import Inspection, User
from app.services.rule_engine import RuleEngine
from app.services.image_quality import ImageQualityAnalyzer
from app.services.pdf_report_service import PDFReportService

client = TestClient(app)

@pytest.fixture
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Scenario 1: Valid packaged product (Compliant)
def test_scenario_1_valid_packaged_product():
    engine = RuleEngine()
    decls = [
        {"field_name": "mrp", "detected_value": "₹ 150.00 (Incl. of all taxes)", "normalized_value": "₹ 150.00 (Incl. of all taxes)", "confidence": 0.98, "has_tax_inclusive": True},
        {"field_name": "net_quantity", "detected_value": "500 g", "normalized_value": "500 g", "confidence": 0.98, "unit": "g"},
        {"field_name": "manufacturer", "detected_value": "National Foods Ltd, Industrial Area, Sector 5, New Delhi 110001", "normalized_value": "National Foods Ltd, Industrial Area, Sector 5, New Delhi 110001", "confidence": 0.96},
        {"field_name": "manufacturing_date", "detected_value": "08/2026", "normalized_value": "08/2026", "confidence": 0.97},
        {"field_name": "consumer_care", "detected_value": "care@nationalfoods.in, 1800-222-333", "normalized_value": "care@nationalfoods.in, 1800-222-333", "confidence": 0.95},
        {"field_name": "generic_name", "detected_value": "Wheat Flour (Atta)", "normalized_value": "Wheat Flour (Atta)", "confidence": 0.95},
        {"field_name": "unit_sale_price", "detected_value": "₹ 0.30 / g", "normalized_value": "₹ 0.30 / g", "confidence": 0.95}
    ]
    images = [
        {"surface_type": "FRONT", "quality_score": 0.95, "blur": False, "glare": False, "is_empty": False},
        {"surface_type": "BACK", "quality_score": 0.95, "blur": False, "glare": False, "is_empty": False}
    ]
    results = engine.evaluate_inspection(decls, images, category="PACKAGED_FOOD")
    outcome = engine.compute_overall_outcome(results)
    assert outcome == "PASS"

# Scenario 2: Missing MRP
def test_scenario_2_missing_mrp():
    engine = RuleEngine()
    decls = [
        {"field_name": "net_quantity", "detected_value": "500 g", "normalized_value": "500 g", "confidence": 0.98, "unit": "g"},
        {"field_name": "manufacturer", "detected_value": "ABC Ltd, New Delhi 110001", "normalized_value": "ABC Ltd, New Delhi 110001", "confidence": 0.96},
        {"field_name": "manufacturing_date", "detected_value": "08/2026", "normalized_value": "08/2026", "confidence": 0.97},
        {"field_name": "consumer_care", "detected_value": "care@abc.com", "normalized_value": "care@abc.com", "confidence": 0.95}
    ]
    images = [
        {"surface_type": "FRONT", "quality_score": 0.95, "blur": False, "glare": False, "is_empty": False},
        {"surface_type": "BACK", "quality_score": 0.95, "blur": False, "glare": False, "is_empty": False}
    ]
    results = engine.evaluate_inspection(decls, images)
    mrp_finding = next((r for r in results if r["field"] == "mrp"), None)
    assert mrp_finding is not None
    assert mrp_finding["outcome"] == "POSSIBLE_NON_COMPLIANCE"
    assert "Rule 6(1)(e)" in mrp_finding["legal_reference"]

# Scenario 3: Missing Manufacturer Address
def test_scenario_3_missing_manufacturer_address():
    engine = RuleEngine()
    decls = [
        {"field_name": "mrp", "detected_value": "₹ 50.00 (Incl. of all taxes)", "normalized_value": "₹ 50.00 (Incl. of all taxes)", "confidence": 0.98, "has_tax_inclusive": True},
        {"field_name": "net_quantity", "detected_value": "200 g", "normalized_value": "200 g", "confidence": 0.98, "unit": "g"},
        {"field_name": "manufacturing_date", "detected_value": "05/2026", "normalized_value": "05/2026", "confidence": 0.97},
        {"field_name": "consumer_care", "detected_value": "care@abc.com", "normalized_value": "care@abc.com", "confidence": 0.95}
    ]
    images = [
        {"surface_type": "FRONT", "quality_score": 0.95, "blur": False, "glare": False, "is_empty": False},
        {"surface_type": "BACK", "quality_score": 0.95, "blur": False, "glare": False, "is_empty": False}
    ]
    results = engine.evaluate_inspection(decls, images)
    mfg_finding = next((r for r in results if r["field"] == "manufacturer"), None)
    assert mfg_finding is not None
    assert mfg_finding["outcome"] == "POSSIBLE_NON_COMPLIANCE"
    assert "Rule 6(1)(a)" in mfg_finding["legal_reference"]

# Scenario 4: Missing Net Quantity
def test_scenario_4_missing_net_quantity():
    engine = RuleEngine()
    decls = [
        {"field_name": "mrp", "detected_value": "₹ 50.00 (Incl. of all taxes)", "normalized_value": "₹ 50.00 (Incl. of all taxes)", "confidence": 0.98, "has_tax_inclusive": True},
        {"field_name": "manufacturer", "detected_value": "ABC Ltd, Delhi 110001", "normalized_value": "ABC Ltd, Delhi 110001", "confidence": 0.96},
        {"field_name": "manufacturing_date", "detected_value": "05/2026", "normalized_value": "05/2026", "confidence": 0.97},
        {"field_name": "consumer_care", "detected_value": "care@abc.com", "normalized_value": "care@abc.com", "confidence": 0.95}
    ]
    images = [
        {"surface_type": "FRONT", "quality_score": 0.95, "blur": False, "glare": False, "is_empty": False},
        {"surface_type": "BACK", "quality_score": 0.95, "blur": False, "glare": False, "is_empty": False}
    ]
    results = engine.evaluate_inspection(decls, images)
    qty_finding = next((r for r in results if r["field"] == "net_quantity"), None)
    assert qty_finding is not None
    assert qty_finding["outcome"] == "POSSIBLE_NON_COMPLIANCE"

# Scenario 5: Missing Manufacturing/Packing Date
def test_scenario_5_missing_date():
    engine = RuleEngine()
    decls = [
        {"field_name": "mrp", "detected_value": "₹ 50.00 (Incl. of all taxes)", "normalized_value": "₹ 50.00 (Incl. of all taxes)", "confidence": 0.98, "has_tax_inclusive": True},
        {"field_name": "net_quantity", "detected_value": "200 g", "normalized_value": "200 g", "confidence": 0.98, "unit": "g"},
        {"field_name": "manufacturer", "detected_value": "ABC Ltd, Delhi 110001", "normalized_value": "ABC Ltd, Delhi 110001", "confidence": 0.96},
        {"field_name": "consumer_care", "detected_value": "care@abc.com", "normalized_value": "care@abc.com", "confidence": 0.95}
    ]
    images = [
        {"surface_type": "FRONT", "quality_score": 0.95, "blur": False, "glare": False, "is_empty": False},
        {"surface_type": "BACK", "quality_score": 0.95, "blur": False, "glare": False, "is_empty": False}
    ]
    results = engine.evaluate_inspection(decls, images)
    date_finding = next((r for r in results if r["field"] == "manufacturing_date"), None)
    assert date_finding is not None
    assert date_finding["outcome"] == "POSSIBLE_NON_COMPLIANCE"
    assert "Rule 6(1)(d)" in date_finding["legal_reference"]

# Scenario 6: Missing Consumer Care Details
def test_scenario_6_missing_consumer_care():
    engine = RuleEngine()
    decls = [
        {"field_name": "mrp", "detected_value": "₹ 50.00 (Incl. of all taxes)", "normalized_value": "₹ 50.00 (Incl. of all taxes)", "confidence": 0.98, "has_tax_inclusive": True},
        {"field_name": "net_quantity", "detected_value": "200 g", "normalized_value": "200 g", "confidence": 0.98, "unit": "g"},
        {"field_name": "manufacturer", "detected_value": "ABC Ltd, Delhi 110001", "normalized_value": "ABC Ltd, Delhi 110001", "confidence": 0.96},
        {"field_name": "manufacturing_date", "detected_value": "05/2026", "normalized_value": "05/2026", "confidence": 0.97}
    ]
    images = [
        {"surface_type": "FRONT", "quality_score": 0.95, "blur": False, "glare": False, "is_empty": False},
        {"surface_type": "BACK", "quality_score": 0.95, "blur": False, "glare": False, "is_empty": False}
    ]
    results = engine.evaluate_inspection(decls, images)
    care_finding = next((r for r in results if r["field"] == "consumer_care"), None)
    assert care_finding is not None
    assert care_finding["outcome"] == "POSSIBLE_NON_COMPLIANCE"
    assert "Rule 6(1)(n)" in care_finding["legal_reference"]

# Scenario 7: Blurry Product Image
def test_scenario_7_blurry_image(tmp_path):
    analyzer = ImageQualityAnalyzer()
    img = np.full((600, 600, 3), 220, dtype=np.uint8)
    cv2.rectangle(img, (50, 50), (550, 550), (0, 0, 0), 2)
    cv2.putText(img, "NET QTY: 500g MRP Rs 100", (70, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    blurry = cv2.GaussianBlur(img, (31, 31), 0)
    path = str(tmp_path / "blurry_pkg.jpg")
    cv2.imwrite(path, blurry)

    res = analyzer.analyze(path)
    assert res["blur"] is True
    assert res["quality_score"] < 0.80

# Scenario 8: Blank Packaging Image
def test_scenario_8_blank_packaging_image(tmp_path):
    analyzer = ImageQualityAnalyzer()
    blank = np.full((500, 500, 3), 255, dtype=np.uint8)
    path = str(tmp_path / "blank_pkg.jpg")
    cv2.imwrite(path, blank)

    res = analyzer.analyze(path)
    assert res["is_empty"] is True
    assert res["quality_score"] == 0.0

# Scenario 9: Multiple Packaging Surfaces
def test_scenario_9_multiple_surfaces():
    engine = RuleEngine()
    decls = [
        {"field_name": "generic_name", "detected_value": "Biscuits", "normalized_value": "Biscuits", "confidence": 0.95},
        {"field_name": "net_quantity", "detected_value": "100 g", "normalized_value": "100 g", "confidence": 0.98, "unit": "g"},
        {"field_name": "mrp", "detected_value": "₹ 20.00 (Incl. of all taxes)", "normalized_value": "₹ 20.00 (Incl. of all taxes)", "confidence": 0.98, "has_tax_inclusive": True},
        {"field_name": "manufacturer", "detected_value": "Biscuit Co, Mumbai 400001", "normalized_value": "Biscuit Co, Mumbai 400001", "confidence": 0.95},
        {"field_name": "manufacturing_date", "detected_value": "05/2026", "normalized_value": "05/2026", "confidence": 0.95},
        {"field_name": "consumer_care", "detected_value": "care@biscuit.com", "normalized_value": "care@biscuit.com", "confidence": 0.95},
        {"field_name": "unit_sale_price", "detected_value": "₹ 0.20 / g", "normalized_value": "₹ 0.20 / g", "confidence": 0.95}
    ]
    images = [
        {"surface_type": "FRONT", "quality_score": 0.92, "blur": False, "glare": False, "is_empty": False},
        {"surface_type": "BACK", "quality_score": 0.90, "blur": False, "glare": False, "is_empty": False},
        {"surface_type": "SIDE", "quality_score": 0.88, "blur": False, "glare": False, "is_empty": False}
    ]
    results = engine.evaluate_inspection(decls, images)
    outcome = engine.compute_overall_outcome(results)
    assert outcome == "PASS"

# Scenario 10: Contradictory Net Quantity Across Surfaces
def test_scenario_10_contradictory_quantity():
    engine = RuleEngine()
    decls = [
        {"field_name": "net_quantity", "detected_value": "500 g", "normalized_value": "500 g", "confidence": 0.98, "unit": "g", "bbox": [10, 10, 50, 50]},
        {"field_name": "net_quantity", "detected_value": "450 g", "normalized_value": "450 g", "confidence": 0.97, "unit": "g", "bbox": [10, 10, 50, 50]},
        {"field_name": "mrp", "detected_value": "₹ 50.00 (Incl. of all taxes)", "normalized_value": "₹ 50.00 (Incl. of all taxes)", "confidence": 0.98, "has_tax_inclusive": True},
        {"field_name": "manufacturer", "detected_value": "Brand Corp, Delhi 110001", "normalized_value": "Brand Corp, Delhi 110001", "confidence": 0.95},
        {"field_name": "manufacturing_date", "detected_value": "05/2026", "normalized_value": "05/2026", "confidence": 0.95},
        {"field_name": "consumer_care", "detected_value": "help@brand.com", "normalized_value": "help@brand.com", "confidence": 0.95}
    ]
    images = [
        {"surface_type": "FRONT", "quality_score": 0.95, "blur": False, "glare": False, "is_empty": False},
        {"surface_type": "BACK", "quality_score": 0.95, "blur": False, "glare": False, "is_empty": False}
    ]
    results = engine.evaluate_inspection(decls, images)
    con_finding = next((r for r in results if r["rule_id"] == "PC-CON-001"), None)
    assert con_finding is not None
    assert con_finding["outcome"] == "REVIEW"
    assert "contradict" in con_finding["explanation"].lower()

# Scenario 11: Invalid Image Format (Handled Gracefully)
def test_scenario_11_invalid_image_format(tmp_path):
    analyzer = ImageQualityAnalyzer()
    corrupt_file = tmp_path / "corrupt.jpg"
    corrupt_file.write_bytes(b"NOT_A_REAL_IMAGE_DATA_123456789")

    res = analyzer.analyze(str(corrupt_file))
    assert res["quality_score"] == 0.0
    assert res["is_empty"] is True
    assert "Unable to decode" in res["issues"][0]

# Scenario 12: Oversized Image Handled Gracefully
def test_scenario_12_oversized_image(tmp_path):
    analyzer = ImageQualityAnalyzer()
    large_img = np.full((2500, 2500, 3), 200, dtype=np.uint8)
    cv2.putText(large_img, "NET QTY: 1 kg", (300, 1200), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 0, 0), 4)
    path = str(tmp_path / "large.jpg")
    cv2.imwrite(path, large_img)

    res = analyzer.analyze(path)
    assert res["resolution_ok"] is True
    assert res["quality_score"] > 0.0

# Scenario 13: PDF Report Generation
def test_scenario_13_pdf_report_generation(tmp_path):
    pdf_service = PDFReportService()
    test_insp_data = {
        "id": "test-insp-uuid",
        "inspection_number": "INSP-TEST-0001",
        "product_name": "Organic Honey 500g",
        "brand_name": "PureLife",
        "category": "PACKAGED_FOOD",
        "status": "FINALIZED",
        "overall_outcome": "PASS",
        "created_at": "2026-11-18 10:00:00",
        "final_remarks": "Passed statutory compliance audit.",
        "compliance_results": [
            {
                "rule_id": "PC-DEC-007",
                "field": "mrp",
                "detected_value": "₹ 250.00",
                "outcome": "PASS",
                "severity": "CRITICAL",
                "legal_reference": "Rule 6(1)(e)",
                "explanation": "Valid MRP declared inclusive of taxes."
            }
        ],
        "declarations": [
            {
                "field_name": "mrp",
                "detected_value": "₹ 250.00",
                "normalized_value": "₹ 250.00",
                "confidence": 0.98
            }
        ],
        "reviewer_actions": []
    }
    report_path = pdf_service.generate_inspection_report(test_insp_data)
    assert os.path.exists(report_path)
    assert os.path.getsize(report_path) > 1000
    with open(report_path, "rb") as f:
        header = f.read(5)
        assert header == b"%PDF-"

# Scenario 14: Database Persistence
def test_scenario_14_database_persistence(db_session: Session):
    import uuid
    unique_insp_num = f"INSP-TEST-{uuid.uuid4().hex[:8].upper()}"
    test_insp = Inspection(
        inspection_number=unique_insp_num,
        product_name="Persisted Coffee 200g",
        brand_name="AromaBeans",
        category="PACKAGED_COMMODITY",
        status="FINALIZED",
        overall_outcome="PASS"
    )
    db_session.add(test_insp)
    db_session.commit()
    db_session.refresh(test_insp)

    fetched = db_session.query(Inspection).filter(Inspection.id == test_insp.id).first()
    assert fetched is not None
    assert fetched.inspection_number == unique_insp_num
    assert fetched.product_name == "Persisted Coffee 200g"

# Scenario 15: API Authentication
def test_scenario_15_api_auth():
    # Valid login
    res_valid = client.post("/api/v1/auth/login", json={"email": "inspector@gov.in", "password": "demo"})
    assert res_valid.status_code == 200
    token = res_valid.json()["access_token"]
    assert token is not None

    # Invalid login
    res_invalid = client.post("/api/v1/auth/login", json={"email": "wrong@gov.in", "password": "badpassword"})
    assert res_invalid.status_code == 400

# Scenario 16: Dashboard Statistics
def test_scenario_16_dashboard_statistics():
    res = client.get("/api/v1/dashboard/summary")
    assert res.status_code == 200
    data = res.json()
    assert "total_inspections" in data
    assert "compliant_count" in data
    assert "needs_review_count" in data
    assert "non_compliance_count" in data
    assert isinstance(data["recent_inspections"], list)
