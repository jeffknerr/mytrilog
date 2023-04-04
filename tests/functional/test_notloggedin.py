from app import create_app

# https://testdriven.io/blog/flask-pytest/

def test_bad_profile(test_client):
    """
    look for certain strings when trying to access profile,
    but not logged in as a real user
    """
    response = test_client.get('/mytrilog/user/notarealuser')
    assert response.status_code == 302
    assert b"You should be redirected automatically " in response.data
    assert b"If not, click the link." in response.data
