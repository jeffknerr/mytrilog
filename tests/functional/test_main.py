from app import create_app

# https://testdriven.io/blog/flask-pytest/

def test_login_page(test_client):
    """look for certain strings and valid status in login page"""
    response = test_client.get('/mytrilog/auth/login')
    assert response.status_code == 200
    assert b"Sign In" in response.data
    assert b"Username" in response.data
    assert b"Password" in response.data
    assert b"Remember Me" in response.data
    assert b"New User?" in response.data
    assert b"Forgot Your Password?" in response.data

def test_redir_to_login(test_client):
    """look for redirect to login page"""
    response = test_client.get('/mytrilog/')
    assert response.status_code == 302
    assert b"You should be redirected automatically" in response.data

# this one doesn't work for my app...
#def test_login_post():
#    """look for method not allowed"""
#    flask_app = create_app()
#    with flask_app.test_client() as test_client:
#        response = test_client.get('/mytrilog/auth/login')
#        assert response.status_code == 405
#        assert b"Sign In" not in response.data
