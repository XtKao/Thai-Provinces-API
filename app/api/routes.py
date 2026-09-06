from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.dependencies import get_province_repository
from app.models import AddressSearchResponse, DistrictSummary, ErrorResponse, ProvinceSummary, Subdistrict
from app.repositories.province_repository import ProvinceRepository

router = APIRouter()


@router.get("/provinces", response_model=list[ProvinceSummary], tags=["Provinces"], summary="List all provinces")
def list_provinces(repository: ProvinceRepository = Depends(get_province_repository)) -> list[ProvinceSummary]:
    return [ProvinceSummary.model_validate(province) for province in repository.list_provinces()]


@router.get("/provinces/{province_id}/districts", response_model=list[DistrictSummary], tags=["Provinces"], summary="List province districts", responses={404: {"model": ErrorResponse}})
def list_districts(province_id: int, repository: ProvinceRepository = Depends(get_province_repository)) -> list[DistrictSummary]:
    province = repository.find_province(province_id)
    if province is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Province with id {province_id} was not found.")
    return [DistrictSummary.model_validate(district) for district in sorted(province.districts, key=lambda item: item.id)]


@router.get("/districts/{district_id}/subdistricts", response_model=list[Subdistrict], tags=["Districts"], summary="List district subdistricts", responses={404: {"model": ErrorResponse}})
def list_subdistricts(district_id: int, repository: ProvinceRepository = Depends(get_province_repository)) -> list[Subdistrict]:
    result = repository.find_district(district_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"District with id {district_id} was not found.")
    _, district = result
    return sorted(district.subdistricts, key=lambda item: item.id)


@router.get("/search", response_model=AddressSearchResponse, tags=["Search"], summary="Search addresses by zipcode", responses={404: {"model": ErrorResponse}})
def search(zipcode: str = Query(..., pattern=r"^\d{5}$", examples=["10400"], description="รหัสไปรษณีย์ 5 หลัก"), repository: ProvinceRepository = Depends(get_province_repository)) -> AddressSearchResponse:
    results = repository.search_by_zipcode(zipcode)
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Zipcode {zipcode} was not found.")
    return AddressSearchResponse(zipcode=zipcode, count=len(results), results=results)

