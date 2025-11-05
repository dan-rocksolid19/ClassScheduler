from librepy.app.forms.session_attendee_form import SessionAttendeeForm
from librepy.app.data.dao.session_attendee_dao import SessionAttendeeDAO


def save_session_attendee(data: dict, context=None) -> dict:
    """
    Validate and persist a SessionAttendee using BaseForm.

    Args:
        data: Dict with keys from UI commit: session, name, email, phone, paid, notes; optional attendee_id.
        context: Optional context object; passed to form for DAO construction/logging.

    Returns:
        - {"ok": False, "errors": [{"field", "message"}, ...]} when validation fails
        - {"ok": True, "result": <model instance>} on success (create/update)
    """
    form = SessionAttendeeForm(data=data, context=context)
    if not form.is_valid():
        return {"ok": False, "errors": form.errors}
    return form.save()


def delete_session_attendee(attendee_id: int, context=None) -> dict:
    """Delete a SessionAttendee by id.

    Returns: {"ok": True, "deleted": n} when n > 0, else {"ok": False}
    """
    dao = SessionAttendeeDAO(getattr(context, "logger", context))
    n = dao.delete_where(dao.model_class.attendee_id == attendee_id, operation_name='delete SessionAttendee by id')
    return {"ok": bool(n and n > 0), "deleted": n or 0}
