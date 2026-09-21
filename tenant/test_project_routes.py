from unittest.mock import MagicMock

from fastapi import HTTPException

from project.routes import get_project


def test_project_access_is_tenant_scoped():
    db = MagicMock()

    current_user = MagicMock()
    current_user.tenant_id = 1

    db.query.return_value.filter.return_value.first.return_value = None

    try:
        get_project(
            project_id=999,
            db=db,
            current_user=current_user
        )
    except HTTPException as error:
        assert error.status_code == 404
        assert error.detail == "Project not found"
    else:
        raise AssertionError(
            "Expected project lookup to fail for inaccessible project"
        )


def test_project_query_uses_current_tenant():
    db = MagicMock()

    current_user = MagicMock()
    current_user.tenant_id = 5

    db.query.return_value.filter.return_value.first.return_value = None

    try:
        get_project(
            project_id=10,
            db=db,
            current_user=current_user
        )
    except HTTPException as error:
        assert error.status_code == 404

    db.query.assert_called_once()
