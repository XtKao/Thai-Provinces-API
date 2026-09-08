import pytest

from scripts.generate_data import normalize


def record(province_id: int, district_id: int, subdistrict_id: int) -> dict[str, object]:
    return {
        "provinceCode": province_id,
        "provinceNameTh": f"จังหวัด {province_id}",
        "provinceNameEn": f"Province {province_id}",
        "districtCode": district_id,
        "districtNameTh": f"อำเภอ {district_id}",
        "districtNameEn": f"District {district_id}",
        "subdistrictCode": subdistrict_id,
        "subdistrictNameTh": f"ตำบล {subdistrict_id}",
        "subdistrictNameEn": f"Subdistrict {subdistrict_id}",
        "postalCode": 10000,
    }


def test_normalize_rejects_district_id_shared_by_provinces():
    records = [record(province_id, 1001, province_id * 10000 + 1) for province_id in range(1, 78)]
    records.append(record(77, 1001, 770002))

    with pytest.raises(ValueError, match="belongs to multiple provinces"):
        normalize(records)


def test_normalize_rejects_conflicting_district_names():
    records = [record(province_id, 1000 + province_id, province_id * 10000 + 1) for province_id in range(1, 78)]
    conflicting = record(1, 1001, 19999)
    conflicting["districtNameTh"] = "ชื่ออำเภอที่ขัดแย้ง"
    records.append(conflicting)

    with pytest.raises(ValueError, match="Conflicting district data"):
        normalize(records)