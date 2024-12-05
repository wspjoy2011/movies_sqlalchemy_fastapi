import pytest
from sqlalchemy import select

from apps.accounts.exceptions import UserAlreadyExists
from database.models.accounts import ActivationToken


@pytest.mark.asyncio
async def test_create_user(accounts_service, user_data, sqlite_session, fake_email_sender):
    """
    Test the create_user method of AccountsService.
    """
    new_user = await accounts_service.create_user(user_data, base_url="http://localhost/")

    assert new_user.username == user_data.username
    assert new_user.email == user_data.email
    assert new_user.first_name == user_data.first_name
    assert new_user.last_name == user_data.last_name

    tokens = await sqlite_session.execute(
        select(ActivationToken).where(ActivationToken.user_id == new_user.id)
    )
    tokens = tokens.scalars().all()
    assert len(tokens) == 1

    assert len(fake_email_sender.sent_emails) == 1
    sent_email = fake_email_sender.sent_emails[0]

    assert sent_email["email"] == user_data.email
    assert "http://localhost/api/v1/accounts/users/activate/" in sent_email["activation_link"]
    assert sent_email["fullname"] == f"{user_data.first_name.capitalize()} {user_data.last_name.capitalize()}"



@pytest.mark.asyncio
async def test_create_user_duplicate(accounts_service, user_data):
    """
    Test that attempting to create a user with duplicate data raises a UserAlreadyExists exception.
    """
    await accounts_service.create_user(user_data, base_url="http://localhost/")

    with pytest.raises(UserAlreadyExists) as exc_info:
        await accounts_service.create_user(user_data, base_url="http://localhost/")

    assert str(exc_info.value) == "Username already exists"
