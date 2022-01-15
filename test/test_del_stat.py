def test_del_stat(test_app):
    response = test_app.delete('api/v1/stat')
    assert response.status_code == 204
    assert response.text == ''

