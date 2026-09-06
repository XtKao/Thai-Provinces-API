def test_list_provinces(client):
    response = client.get("/api/provinces")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 77
    assert list(data[0]) == ["id", "name_th", "name_en"]


def test_list_districts(client):
    response = client.get("/api/provinces/10/districts")
    assert response.status_code == 200
    assert response.json()[0]["id"] == 1001
    assert "subdistricts" not in response.json()[0]


def test_missing_province(client):
    response = client.get("/api/provinces/99/districts")
    assert response.status_code == 404
    assert response.json()["detail"] == "Province with id 99 was not found."


def test_list_subdistricts(client):
    response = client.get("/api/districts/1001/subdistricts")
    assert response.status_code == 200
    assert response.json()[0]["zipcode"] == "10200"


def test_missing_district(client):
    response = client.get("/api/districts/9999/subdistricts")
    assert response.status_code == 404


def test_search_and_count(client):
    response = client.get("/api/search", params={"zipcode": "10400"})
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == len(data["results"])
    assert data["zipcode"] == "10400"


def test_missing_zipcode(client):
    assert client.get("/api/search", params={"zipcode": "00000"}).status_code == 404


def test_invalid_zipcodes(client):
    for zipcode in ("1234", "123456", "12a45"):
        assert client.get("/api/search", params={"zipcode": zipcode}).status_code == 422


def test_health_and_root(client):
    assert client.get("/health").status_code == 200
    assert client.get("/health").json()["status"] == "ok"
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/docs"