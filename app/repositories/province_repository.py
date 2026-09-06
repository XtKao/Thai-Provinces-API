import json
from functools import lru_cache
from pathlib import Path

from pydantic import RootModel, ValidationError

from app.models import AddressResult, Province


class ProvinceData(RootModel[list[Province]]):
    """Validated internal representation of the nested source document."""


class ProvinceRepository:
    def __init__(self, data_path: Path) -> None:
        self.data_path = data_path
        self._provinces = self._load()

    def _load(self) -> list[Province]:
        if not self.data_path.is_file():
            raise FileNotFoundError(f"Data file was not found: {self.data_path}")
        try:
            with self.data_path.open(encoding="utf-8") as data_file:
                document = json.load(data_file)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Data file contains invalid JSON: {exc}") from exc
        if not isinstance(document, dict) or not isinstance(document.get("provinces"), list):
            raise ValueError("Data file must contain a top-level 'provinces' array.")
        try:
            return ProvinceData.model_validate(document["provinces"]).root
        except ValidationError as exc:
            raise ValueError(f"Data file failed schema validation: {exc}") from exc

    def list_provinces(self) -> list[Province]:
        return sorted(self._provinces, key=lambda province: province.id)

    def find_province(self, province_id: int) -> Province | None:
        return next((item for item in self._provinces if item.id == province_id), None)

    def find_district(self, district_id: int):
        for province in self._provinces:
            district = next((item for item in province.districts if item.id == district_id), None)
            if district is not None:
                return province, district
        return None

    def search_by_zipcode(self, zipcode: str) -> list[AddressResult]:
        results: list[AddressResult] = []
        for province in self._provinces:
            for district in province.districts:
                for subdistrict in district.subdistricts:
                    if subdistrict.zipcode == zipcode:
                        results.append(AddressResult(
                            province_id=province.id, province_name_th=province.name_th, province_name_en=province.name_en,
                            district_id=district.id, district_name_th=district.name_th, district_name_en=district.name_en,
                            subdistrict_id=subdistrict.id, subdistrict_name_th=subdistrict.name_th,
                            subdistrict_name_en=subdistrict.name_en, zipcode=subdistrict.zipcode,
                        ))
        return sorted(results, key=lambda result: result.subdistrict_id)


@lru_cache(maxsize=1)
def get_repository(data_path: Path) -> ProvinceRepository:
    return ProvinceRepository(data_path)