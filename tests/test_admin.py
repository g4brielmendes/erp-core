from fastapi import HTTPException
from app.core.admin import admin_required


class FakeAdmin:
    role = "admin"


class FakeUser:
    role = "user"


def test_admin_required_success():

    user = FakeAdmin()

    result = admin_required(user)

    assert result.role == "admin"


def test_admin_required_fail():

    user = FakeUser()

    try:

        admin_required(user)

    except HTTPException as e:

        assert e.status_code == 403
        assert e.detail == "Acesso negado"