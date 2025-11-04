from librepy.app.forms.employee_form import EmployeeForm
from librepy.app.data.dao.employee_dao import EmployeeDAO


def save_employee(data: dict, context=None) -> dict:
    """
    Validate and persist an Employee using BaseForm.

    Args:
        data: Dict with keys from UI commit: first_name, last_name, email; optional employee_id.
        context: Optional context object; passed to form for DAO construction/logging.

    Returns:
        - {"ok": False, "errors": [{"field", "message"}, ...]} when validation fails
        - {"ok": True, "result": <model instance>} on success (create/update)
    """
    form = EmployeeForm(data=data, context=context)
    if not form.is_valid():
        return {"ok": False, "errors": form.errors}
    return form.save()


def delete_employee(employee_id: int, context=None) -> dict:
    """Delete an Employee by id.

    Returns: {"ok": True, "deleted": n} when n > 0, else {"ok": False}
    """
    dao = EmployeeDAO(getattr(context, "logger", context))
    n = dao.delete_where(dao.model_class.employee_id == employee_id, operation_name='delete Employee by id')
    return {"ok": bool(n and n > 0), "deleted": n or 0}
