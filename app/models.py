from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

Zipcode = Annotated[str, Field(pattern=r"^\d{5}$", description="รหัสไปรษณีย์ 5 หลัก")]


class ProvinceSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: int = Field(description="รหัสจังหวัด")
    name_th: str = Field(description="ชื่อจังหวัดภาษาไทย")
    name_en: str = Field(description="ชื่อจังหวัดภาษาอังกฤษ")


class DistrictSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: int = Field(description="รหัสอำเภอหรือเขต")
    name_th: str = Field(description="ชื่ออำเภอหรือเขตภาษาไทย")
    name_en: str = Field(description="ชื่ออำเภอหรือเขตภาษาอังกฤษ")


class Subdistrict(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: int = Field(description="รหัสตำบลหรือแขวง")
    name_th: str = Field(description="ชื่อตำบลหรือแขวงภาษาไทย")
    name_en: str = Field(description="ชื่อตำบลหรือแขวงภาษาอังกฤษ")
    zipcode: Zipcode


class District(DistrictSummary):
    subdistricts: list[Subdistrict] = Field(description="รายการตำบลหรือแขวง")


class Province(ProvinceSummary):
    districts: list[District] = Field(description="รายการอำเภอหรือเขต")


class AddressResult(BaseModel):
    model_config = ConfigDict(extra="forbid")
    province_id: int
    province_name_th: str
    province_name_en: str
    district_id: int
    district_name_th: str
    district_name_en: str
    subdistrict_id: int
    subdistrict_name_th: str
    subdistrict_name_en: str
    zipcode: Zipcode


class AddressSearchResponse(BaseModel):
    zipcode: Zipcode
    count: int = Field(ge=0, description="จำนวนผลลัพธ์")
    results: list[AddressResult]


class ErrorResponse(BaseModel):
    detail: str = Field(description="รายละเอียดข้อผิดพลาด")


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str