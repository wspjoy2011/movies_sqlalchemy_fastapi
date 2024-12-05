import pytest


@pytest.mark.asyncio
async def test_create_user_endpoint(test_client, override_accounts_service, user_data):
    """
    Testing endpoint for user creation with service substitution.
    """
    client = test_client

    response = client.post("/api/v1/accounts/users", json=user_data.model_dump())

    assert response.status_code == 201
    response_data = response.json()
    assert response_data["user"]["username"] == user_data.username
    assert f"Check {user_data.email} email for activation link" in response_data["message"]
