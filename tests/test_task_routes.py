from unittest.mock import MagicMock

from fastapi import HTTPException

from task.routes import get_task


def test_task_access_is_tenant_scoped():
    db = MagicMock()

    current_user = MagicMock()
    current_user.tenant_id = 1

    db.query.return_value.join.return_value.filter.return_value.first.return_value = None

    with_error = False

    try:
        get_task(
            task_id=999,
            db=db,
            current_user=current_user
        )
    except HTTPException as error:
        with_error = True

        assert error.status_code == 404
        assert error.detail == "Task not found"

    assert with_error


def test_task_query_uses_project_tenant_filter():
    db = MagicMock()

    current_user = MagicMock()
    current_user.tenant_id = 5

    db.query.return_value.join.return_value.filter.return_value.first.return_value = None

    try:
        get_task(
            task_id=10,
            db=db,
            current_user=current_user
        )
    except HTTPException as error:
        assert error.status_code == 404

    db.query.assert_called_once()
    db.query.return_value.join.assert_called_once()
    db.query.return_value.join.return_value.filter.assert_called_once()
