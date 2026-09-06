"""Download and normalize Thailand geography data into the API schema."""
import json
import sys
from collections import defaultdict
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

SOURCE_URL = "https://raw.githubusercontent.com/thailand-geography-data/thailand-geography-json/main/src/geography.json"
OUTPUT_PATH = Path(__file__).resolve().parents[1] / "app" / "data" / "data.json"


def download_source(url: str = SOURCE_URL) -> object:
    try:
        request = Request(url, headers={"User-Agent": "thai-provinces-api-generator/1.0"})
        with urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Unable to download or parse source data: {exc}") from exc


def as_records(document: object) -> list[dict[str, object]]:
    if isinstance(document, list):
        records = document
    elif isinstance(document, dict):
        for key in ("data", "results", "items", "geography"):
            if isinstance(document.get(key), list):
                records = document[key]
                break
        else:
            raise ValueError("Source object must contain an array under data, results, items, or geography.")
    else:
        raise ValueError("Source JSON must be an array or an object containing an array.")
    if not all(isinstance(record, dict) for record in records):
        raise ValueError("Source records must be JSON objects.")
    return records


def required(record: dict[str, object], *keys: str) -> object:
    for key in keys:
        if key in record and record[key] not in (None, ""):
            return record[key]
    raise ValueError(f"Missing required source field; expected one of: {', '.join(keys)}")


def normalize(document: object) -> dict[str, list[dict[str, object]]]:
    provinces: dict[int, dict[str, object]] = {}
    districts: dict[int, dict[str, object]] = {}
    seen_subdistricts: set[int] = set()
    for record in as_records(document):
        province_id = int(required(record, "provinceCode", "province_id", "provinceId"))
        district_id = int(required(record, "districtCode", "district_id", "districtId"))
        subdistrict_id = int(required(record, "subdistrictCode", "subdistrict_id", "subdistrictId"))
        zipcode = str(required(record, "postalCode", "zipcode", "zipCode")).zfill(5)
        if len(zipcode) != 5 or not zipcode.isdigit():
            raise ValueError(f"Invalid zipcode for subdistrict {subdistrict_id}: {zipcode!r}")
        if subdistrict_id in seen_subdistricts:
            raise ValueError(f"Duplicate subdistrict ID: {subdistrict_id}")
        seen_subdistricts.add(subdistrict_id)
        if province_id not in provinces:
            provinces[province_id] = {"id": province_id, "name_th": str(required(record, "provinceNameTh", "province_name_th")), "name_en": str(required(record, "provinceNameEn", "province_name_en")), "districts": []}
        elif provinces[province_id]["name_th"] != str(required(record, "provinceNameTh", "province_name_th")):
            raise ValueError(f"Conflicting province data for ID {province_id}")
        if district_id not in districts:
            district = {"id": district_id, "name_th": str(required(record, "districtNameTh", "district_name_th")), "name_en": str(required(record, "districtNameEn", "district_name_en")), "subdistricts": []}
            districts[district_id] = district
            provinces[province_id]["districts"].append(district)
        subdistrict = {"id": subdistrict_id, "name_th": str(required(record, "subdistrictNameTh", "subdistrict_name_th")), "name_en": str(required(record, "subdistrictNameEn", "subdistrict_name_en")), "zipcode": zipcode}
        districts[district_id]["subdistricts"].append(subdistrict)
    result = {"provinces": sorted(provinces.values(), key=lambda item: item["id"])}
    for province in result["provinces"]:
        province["districts"].sort(key=lambda item: item["id"])
        for district in province["districts"]:
            district["subdistricts"].sort(key=lambda item: item["id"])
    validate(result)
    return result


def validate(document: dict[str, list[dict[str, object]]]) -> None:
    provinces = document["provinces"]
    if len(provinces) != 77:
        raise ValueError(f"Expected 77 provinces, found {len(provinces)}")
    province_ids: set[int] = set()
    district_ids: set[int] = set()
    subdistrict_ids: set[int] = set()
    district_count = 0
    subdistrict_count = 0
    for province in provinces:
        if province["id"] in province_ids or not province["districts"]:
            raise ValueError(f"Invalid or duplicate province: {province['id']}")
        province_ids.add(province["id"])
        for district in province["districts"]:
            if district["id"] in district_ids or not district["subdistricts"]:
                raise ValueError(f"Invalid or duplicate district: {district['id']}")
            district_ids.add(district["id"])
            district_count += 1
            for subdistrict in district["subdistricts"]:
                if subdistrict["id"] in subdistrict_ids:
                    raise ValueError(f"Duplicate subdistrict: {subdistrict['id']}")
                subdistrict_ids.add(subdistrict["id"])
                subdistrict_count += 1
    if district_count < 700 or subdistrict_count < 7000:
        raise ValueError(f"Source appears incomplete: {district_count} districts, {subdistrict_count} subdistricts")


def main() -> int:
    try:
        document = normalize(download_source())
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_PATH.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        districts = sum(len(province["districts"]) for province in document["provinces"])
        subdistricts = sum(len(district["subdistricts"]) for province in document["provinces"] for district in province["districts"])
        print(f"Generated {OUTPUT_PATH}: {len(document['provinces'])} provinces, {districts} districts, {subdistricts} subdistricts, {OUTPUT_PATH.stat().st_size} bytes")
        return 0
    except (RuntimeError, ValueError, TypeError, KeyError) as exc:
        print(f"Data generation failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())