import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class ThaiProvincesAPIError(RuntimeError):
    """Raised when the API cannot be reached or returns an error response."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


class ThaiProvincesAPI:
    """Small dependency-free client for https://thaiprovincesapi.vercel.app."""

    def __init__(self, base_url: str = "https://thaiprovincesapi.vercel.app", timeout: float = 10.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _get(self, path: str, params: dict[str, str] | None = None) -> object:
        url = f"{self.base_url}{path}"
        if params:
            url = f"{url}?{urlencode(params)}"
        request = Request(url, headers={"Accept": "application/json", "User-Agent": "thai-provinces-python/1.0"})
        try:
            with urlopen(request, timeout=self.timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            try:
                error_body = json.loads(exc.read().decode("utf-8"))
                detail = error_body.get("detail", str(exc)) if isinstance(error_body, dict) else str(error_body)
            except (json.JSONDecodeError, UnicodeDecodeError):
                detail = str(exc)
            raise ThaiProvincesAPIError(str(detail), exc.code) from exc
        except (URLError, TimeoutError, json.JSONDecodeError) as exc:
            raise ThaiProvincesAPIError(f"Unable to request Thai Provinces API: {exc}") from exc

    def health(self) -> dict[str, str]:
        return self._get("/health")  # type: ignore[return-value]

    def list_provinces(self) -> list[dict[str, object]]:
        return self._get("/api/provinces")  # type: ignore[return-value]

    def list_districts(self, province_id: int) -> list[dict[str, object]]:
        return self._get(f"/api/provinces/{province_id}/districts")  # type: ignore[return-value]

    def list_subdistricts(self, district_id: int) -> list[dict[str, object]]:
        return self._get(f"/api/districts/{district_id}/subdistricts")  # type: ignore[return-value]

    def search(self, zipcode: str) -> dict[str, object]:
        return self._get("/api/search", {"zipcode": zipcode})  # type: ignore[return-value]