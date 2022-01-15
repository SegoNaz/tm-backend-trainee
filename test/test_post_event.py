def test_create_event(test_app):
    event_data = {
        "views": 10,
        "clicks": 10,
        "cost": 1.99,
        "date": "2022-01-12"
    }
    response = test_app.post('api/v1/stat', json=event_data)
    assert response.status_code == 201
    body = response.json()
    assert body == event_data


def test_create_event_invalid_cost(test_app):
    event_data = {
        "views": 100,
        "clicks": 100,
        "cost": 1.999,
        "date": "2022-01-09"
    }
    response = test_app.post('api/v1/stat', json=event_data)
    assert response.status_code == 422
    body = response.json()
    assert body == {'detail': [{'loc': ['body', 'cost'],
                                'msg': 'Invalid cost value: 1.999', 'type': 'value_error'}]}


def test_create_event_invalid_views(test_app):
    event_data = {
        "views": -100,
        "clicks": 100,
        "cost": 1.99,
        "date": "2022-01-09"
    }
    response = test_app.post('api/v1/stat', json=event_data)
    assert response.status_code, 422
    body = response.json()
    assert body == {'detail': [{'loc': ['body', 'views'],
                                'msg': 'ensure this value is greater than or equal to 0',
                                'type': 'value_error.number.not_ge', 'ctx': {'limit_value': 0}}]}


def test_create_event_invalid_clicks(test_app):
    event_data = {
        "views": 11,
        "clicks": -11,
        "cost": 11.99,
        "date": "2022-01-12"
    }
    response = test_app.post('api/v1/stat', json=event_data)
    assert response.status_code, 422
    body = response.json()
    assert body == {"detail": [{"loc": ["body", "clicks"],
                                "msg": "ensure this value is greater than or equal to 0",
                                "type": "value_error.number.not_ge",
                                "ctx": {"limit_value": 0}}]}


def test_create_event_invalid_date(test_app):
    event_data = {
        "views": 110,
        "clicks": 110,
        "cost": 111.99,
        "date": "2022-01-112"
    }
    response = test_app.post('api/v1/stat', json=event_data)
    assert response.status_code, 422
    body = response.json()
    assert body == {"detail": [{"loc": ["body", "date"],
                                "msg": "invalid date format",
                                "type": "value_error.date"}]}
