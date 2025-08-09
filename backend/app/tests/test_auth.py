def test_user_registration_and_login(client):
    # Create user
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "Test@1234"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

    # Login with correct creds
    login_data = {
        "username": "testuser",
        "password": "Test@1234"
    }
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    json_response = response.json()
    assert "access_token" in json_response
    assert json_response["token_type"] == "bearer"

    # Login with wrong creds
    login_data["password"] = "wrongpassword"
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 401
