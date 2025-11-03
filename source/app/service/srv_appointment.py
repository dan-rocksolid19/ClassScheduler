from typing import Any, Dict

from librepy.app.forms.service_appointment_form import ServiceAppointmentForm


def save_service_appointment(data: Dict[str, Any], context=None) -> Dict[str, Any]:
    """
    Validate and persist a Service Appointment using BaseForm.

    Args:
        data: Dict with keys from UI commit: name, phone, email, date, time, notes; optional service_apt_id.
        context: Optional context object; passed to form for DAO construction/logging.

    Returns:
        - {"ok": False, "errors": [{"field", "message"}, ...]} when validation fails
        - {"ok": True, "result": <model instance>} on success (create/update)
    """
    form = ServiceAppointmentForm(data=data, context=context)
    if not form.is_valid():
        return {"ok": False, "errors": form.errors}
    return form.save()
