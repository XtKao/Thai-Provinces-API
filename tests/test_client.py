import io
from urllib.error import HTTPError

import pytest

from thai_provinces.client import ThaiProvincesAPI, ThaiProvincesAPIError


def test_client_methods(monkeypatch):
    client = ThaiProvincesAPI()
    calls = []

    def fake_get(path, params=None):
        calls.append((path, params))
        return []

    monkeypatch.setattr(client, "_get", fake_get)
    assert client.list_provinces() == []
    assert client.list_districts(10) == []
    assert client.list_subdistricts(1001) == []
    assert client.search("10400") == []
    assert calls == [
        ("/api/provinces", None),
        ("/api/provinces/10/districts", None),
        ("/api/districts/1001/subdistricts", None),
        ("/api/search", {"zipcode": "10400"}),
    ]


def test_client_error_has_status_code(monkeypatch):
    client = ThaiProvincesAPI()
    monkeypatch.setattr(client, "_get", lambda *_args, **_kwargs: (_ for _ in ()).throw(ThaiProvincesAPIError("not found", 404)))
    try:
        client.list_provinces()
    except ThaiProvincesAPIError as exc:
        assert exc.status_code == 404
    else:
        raise AssertionError("Expected ThaiProvincesAPIError")


def test_client_handles_non_object_error_body(monkeypatch):
    client = ThaiProvincesAPI()
    error = HTTPError("https://example.test", 500, "server error", {}, io.BytesIO(b'["server error"]'))
    monkeypatch.setattr("thai_provinces.client.urlopen", lambda *_args, **_kwargs: (_ for _ in ()).throw(error))

    with pytest.raises(ThaiProvincesAPIError, match="server error") as raised:
        client.health()

    assert raised.value.status_code == 500