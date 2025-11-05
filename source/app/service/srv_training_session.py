from librepy.app.forms.training_session_form import TrainingSessionForm
from librepy.app.data.dao.teacher_dao import TeacherDAO


def save_training_session(data: dict, context=None) -> dict:
    """
    Validate and persist a Training Session using BaseForm.

    Args:
        data: Dict with keys: name, teacher (teacher_id), session_date,
              session_time, price; optional session_id for updates.
        context: Optional context object for DAO construction/logging.

    Returns:
        - {"ok": False, "errors": [{"field", "message"}, ...]} on validation failure
        - {"ok": True, "result": <model instance>} on success
    """
    form = TrainingSessionForm(data=data, context=context)
    if not form.is_valid():
        return {"ok": False, "errors": form.errors}
    return form.save()




def load_teacher_pairs(context=None):
    """
    Return list of (id, label) pairs for teacher list controls.
    Replicates the Employee Contract dialog pattern.
    """
    dao = TeacherDAO(getattr(context, "logger", context))
    rows = dao.get_all_for_grid() or []  # [{id, name, email}]
    return [(r.get('id'), r.get('name') or '') for r in rows]
