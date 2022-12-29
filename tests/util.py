from flask import url_for

USERNAME_ADMIN = "admin"
EMAIL_ADMIN = "admin@email.com"

USERNAME = "username"
PASSWORD = "fake_password"
FIRST_NAME = "Administrator"
LAST_NAME = "Koneksys"
EMAIL = "user@email.com"
BAD_REQUEST = "Input payload validation failed"

PROJECT_NAME = "Project Name"


def register_user(
    test_client,
    token,
    username=USERNAME,
    first_name=FIRST_NAME,
    last_name=LAST_NAME,
    email=EMAIL,
    enabled=True,
):
    return test_client.post(
        url_for("api.user_list"),
        json={
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "enabled": enabled,
        },
        content_type="application/json",
        headers={"Authorization": "Bearer " + token},
    )
