from typing import Any, Dict

from librepy.app.forms.base_form import BaseForm
from librepy.app.data.dao.employee_dao import EmployeeDAO


class EmployeeForm(BaseForm):
    class Meta(BaseForm.Meta):
        dao = None
        dao_factory = staticmethod(lambda context: EmployeeDAO(getattr(context, "logger", context)))
        create_fn = "create"
        update_fn = "update"
        pk_field = "employee_id"

    def clean(self) -> None:
        employee_id = self.get("employee_id")
        first_name_in = self.require("first_name")
        last_name_in = self.require("last_name")
        email_in = self.get("email")

        cleaned: Dict[str, Any] = {}

        # PK passthrough for updates
        if employee_id is not None:
            try:
                cleaned["employee_id"] = int(employee_id) if str(employee_id).strip() != "" else None
            except (TypeError, ValueError):
                self.add_error("employee_id", "Invalid employee id")

        # first_name
        if (first_name_in is not None) or not self.partial:
            fn = (str(first_name_in or "")).strip()
            if len(fn) > 45:
                self.add_error("first_name", "First name cannot exceed 45 characters")
            else:
                cleaned["first_name"] = fn

        # last_name
        if (last_name_in is not None) or not self.partial:
            ln = (str(last_name_in or "")).strip()
            if len(ln) > 45:
                self.add_error("last_name", "Last name cannot exceed 45 characters")
            else:
                cleaned["last_name"] = ln

        # email optional: if None or empty -> None; otherwise must contain '@'
        em_raw = email_in
        em = None if em_raw is None else str(em_raw).strip()
        if em is None or em == "":
            cleaned["email"] = None
        else:
            if "@" not in em:
                self.add_error("email", "Invalid email address")
            else:
                cleaned["email"] = em

        # Assign
        self.cleaned_data.update(cleaned)
