from typing import Any, Dict, Optional

from librepy.app.forms.base_form import BaseForm
from librepy.app.data.dao.session_attendee_dao import SessionAttendeeDAO


class SessionAttendeeForm(BaseForm):
    class Meta(BaseForm.Meta):
        dao = None
        dao_factory = staticmethod(lambda context: SessionAttendeeDAO(getattr(context, "logger", context)))
        create_fn = "create"
        update_fn = "update"
        pk_field = "attendee_id"

    def clean(self) -> None:
        attendee_id = self.get("attendee_id")
        session_in = self.require("session")
        name_in = self.require("name")
        email_in = self.get("email")
        phone_in = self.get("phone")
        paid_in = self.get("paid", False)
        notes_in = self.get("notes")

        cleaned: Dict[str, Any] = {}

        # PK passthrough
        if attendee_id is not None:
            try:
                cleaned["attendee_id"] = int(attendee_id) if str(attendee_id).strip() != "" else None
            except (TypeError, ValueError):
                self.add_error("attendee_id", "Invalid attendee id")

        # session (required, int)
        if (session_in is not None) or not self.partial:
            try:
                sess_id = int(session_in) if session_in is not None and str(session_in).strip() != "" else None
            except (TypeError, ValueError):
                sess_id = None
            if not sess_id or sess_id <= 0:
                self.add_error("session", "Valid session id is required")
            else:
                cleaned["session"] = sess_id

        # name (required)
        if (name_in is not None) or not self.partial:
            nm = (str(name_in or "")).strip()
            if not nm:
                self.add_error("name", "Name is required")
            elif len(nm) > 80:
                self.add_error("name", "Name cannot exceed 80 characters")
            else:
                cleaned["name"] = nm

        # email (optional)
        em = None if email_in is None else str(email_in).strip()
        if em is None or em == "":
            cleaned["email"] = None
        else:
            if "@" not in em:
                self.add_error("email", "Invalid email address")
            else:
                cleaned["email"] = em

        # phone (optional, trim)
        ph = None if phone_in is None else str(phone_in).strip()
        if ph is None or ph == "":
            cleaned["phone"] = None
        else:
            if len(ph) > 20:
                self.add_error("phone", "Phone cannot exceed 20 characters")
            else:
                cleaned["phone"] = ph

        # paid (bool)
        cleaned["paid"] = bool(paid_in)

        # notes (optional)
        nt = None if notes_in is None else str(notes_in).strip()
        cleaned["notes"] = None if (nt is None or nt == "") else nt

        self.cleaned_data.update(cleaned)
