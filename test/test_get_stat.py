def test_get_stat_from_empty_db(test_app):
    request_data = {'from': '2022-01-13', 'to': '2022-01-13', 'order_column': 'date'}
    response = test_app.get('api/v1/stat/', data=request_data)
    assert response.status_code == 404
    body = response.json()
    assert body == {
        "detail": "Not Found"
    }


def test_get_stat_data_exist(test_app):
    event_data = {
        "views": 100,
        "clicks": 100,
        "cost": 2.99,
        "date": "2022-01-12"
    }
    response = test_app.post('api/v1/stat', json=event_data)
    assert response.status_code == 201
    body = response.json()
    assert body == event_data

    request_data = {'from': '2022-01-12', 'to': '2022-01-12', 'order_column': 'date'}
    response = test_app.get('api/v1/stat/', params=request_data)
    assert response.status_code == 200
    body = response.json()
    assert body == [
        {
            "views": 100,
            "clicks": 100,
            "cost": 2.99,
            "date": "2022-01-12",
            "cpc": 0.03,
            "cpm": 29.9
        }
    ]
