import pytest
import requests
import vcr

@vcr.use_cassette('tests/vcr_cassettes/loan.yaml')
def test_post_loan():

    url = "http://localhost:5000/loan/create"

    payload="{\r\n    \"purchase_name\": \"Miami Cruise\",\r\n    \"account_id\": 1,\r\n    \"amount\": 1500.5\r\n}"
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    assert response.status_code == 200
