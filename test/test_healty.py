# from .. app.main import app
# from fastapi.testclient import TestClient
#
# client = TestClient(app)


def test_health_check(test_app):
    response = test_app.get('/')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}

