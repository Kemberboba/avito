import pytest
import requests

BASE_URL = 'https://qa-internship.avito.com/api/1'

def test_create_ad_success():
    payload = {"sellerID": 8800, "name": "Рабочая тетрадь", "price": 1200}
    response = requests.post(f"{BASE_URL}/item", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data['status'], str)

def test_create_ad_missing_name():
    payload = {"sellerID": 8800, "price": 2500}
    response = requests.post(f"{BASE_URL}/item", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert 'result' in data
    assert 'message' in data['result']

def test_create_ad_invalid_sellerID():
    payload = {"sellerID": "abc", "name": "Смартфон", "price": 10000}
    response = requests.post(f"{BASE_URL}/item", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert 'result' in data
    assert 'message' in data['result']

def test_get_ad_by_id_success():
    ad_id = "fe5ae029-e567-4dd4-ad35-0b27c2b4d432"
    response = requests.get(f"{BASE_URL}/item/{ad_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    ad = data[0]
    assert ad['id'] == ad_id
    assert ad['sellerId'] == 8800
    assert ad['name'] == "Рабочая тетрадь"
    assert ad['price'] == 1200
    assert ad['statistics']['likes'] == 0
    assert ad['statistics']['viewCount'] == 0
    assert ad['statistics']['contacts'] == 0

def test_get_ad_by_id_not_found():
    response = requests.get(f"{BASE_URL}/item/9999999")
    assert response.status_code == 404
    data = response.json()
    assert 'result' in data
    assert 'message' in data['result']

def test_get_ad_by_id_server_error():
    response = requests.get(f"{BASE_URL}/item/123")
    assert response.status_code in [500, 404]

def test_get_ads_by_sellerID_success():
    response = requests.get(f"{BASE_URL}/8800/item")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    for ad in data:
        assert ad['sellerId'] == 8800

def test_get_ads_by_sellerID_no_ads():
    response = requests.get(f"{BASE_URL}/100500/item")
    assert response.status_code == 200
    data = response.json()
    assert data == []

def test_get_ads_by_sellerID_invalid():
    response = requests.get(f"{BASE_URL}/abc/item")
    assert response.status_code == 400
    data = response.json()
    assert 'result' in data
    assert 'message' in data['result']

def test_get_statistics_success():
    ad_id = "fe5ae029-e567-4dd4-ad35-0b27c2b4d432"
    response = requests.get(f"{BASE_URL}/statistic/{ad_id}")
    assert response.status_code == 200
    data = response.json()
    stats = data[0]
    assert stats['likes'] == 0
    assert stats['viewCount'] == 0
    assert stats['contacts'] == 0

def test_get_statistics_not_found():
    response = requests.get(f"{BASE_URL}/statistic/555")
    assert response.status_code == 404
    data = response.json()
    assert 'result' in data
    assert 'message' in data['result']

if __name__ == '__main__':
    pytest.main()
