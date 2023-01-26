from app import create_app

def test_login_page():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    flask_app = create_app()

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.get('/mytrilog/auth/login?next=%2Fmytrilog%2F')
        assert response.status_code == 200
#       assert b"Please log in to access this page" in response.data
#       assert b"Sign In" in response.data
#       assert b"New User?" in response.data
#       assert b"Forgot Your Password?" in response.data
