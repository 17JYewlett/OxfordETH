import requests

API_URL = "http://127.0.0.1:5000"

def test_get_courts():
    response = requests.get(f"{API_URL}/courts?postcode=WC2N 5DU")
    print(response.json())

def test_get_coaches():
    response = requests.get(f"{API_URL}/coaches?court=Central Tennis Club")
    print(response.json())

def test_create_session():
    data = {"coach": "0xA1B2C3D4E5F6G7H8I9J0", "amount": "0.5"}
    response = requests.post(f"{API_URL}/create_session", json=data)
    print(response.json())

if __name__ == "__main__":
    test_get_courts()
    test_get_coaches()
    test_create_session()