from pathlib import Path

from app.repositories.province_repository import ProvinceRepository, get_repository

DATA_PATH = Path(__file__).resolve().parent / "data" / "data.json"


def get_province_repository() -> ProvinceRepository:
    return get_repository(DATA_PATH)