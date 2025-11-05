from librepy.pybrex import dialog
from librepy.pybrex.msgbox import msgbox, confirm_action
from librepy.app.data.dao.session_attendee_dao import SessionAttendeeDAO


class AttendeeEntryDialog(dialog.DialogBase):
    """
    Dialog for creating/editing a Session Attendee.
    Mirrors the layout and workflow pattern from TeacherEntryDialog.
    """

    POS_SIZE = 0, 0, 400, 275

    MARGIN = 32
    ROW_SPACING = 10
    LABEL_HEIGHT = 14
    FIELD_HEIGHT = 22
    BUTTON_HEIGHT = 24

    def __init__(self, ctx, parent, logger, **props):
        props['Title'] = props.get('Title', 'Attendee Entry')
        # Optional edit-mode id
        self.attendee_id = props.pop('attendee_id', None)
        # Required session linkage (int id)
        self.session_id = props.pop('session_id', None)

        self.ctx = ctx
        self.parent = parent
        self.logger = logger

        # Controls
        self.lbl_width = None
        self.field_width = None

        super().__init__(ctx, self.parent, **props)

    def _create(self):
        x = self.MARGIN
        y = self.MARGIN // 3

        total_inner_width = self.POS_SIZE[2] - (self.MARGIN * 2)
        self.lbl_width = int(total_inner_width * 0.30)
        self.field_width = total_inner_width - self.lbl_width

        label_kwargs = dict(FontWeight=120, FontHeight=11, VerticalAlign=2)

        # Name
        self.add_label('LblName', x, y, self.lbl_width, self.LABEL_HEIGHT, Label='Name', **label_kwargs)
        self.edt_name = self.add_edit('EdtName', x + self.lbl_width, y - 2, self.field_width, self.FIELD_HEIGHT)
        y += self.FIELD_HEIGHT + self.ROW_SPACING

        # Email
        self.add_label('LblEmail', x, y, self.lbl_width, self.LABEL_HEIGHT, Label='Email', **label_kwargs)
        self.edt_email = self.add_edit('EdtEmail', x + self.lbl_width, y - 2, self.field_width, self.FIELD_HEIGHT)
        y += self.FIELD_HEIGHT + self.ROW_SPACING

        # Phone
        self.add_label('LblPhone', x, y, self.lbl_width, self.LABEL_HEIGHT, Label='Phone', **label_kwargs)
        self.edt_phone = self.add_edit('EdtPhone', x + self.lbl_width, y - 2, self.field_width, self.FIELD_HEIGHT)
        y += self.FIELD_HEIGHT + self.ROW_SPACING

        # Paid
        self.add_label('LblPaid', x, y, self.lbl_width, self.LABEL_HEIGHT, Label='Paid', **label_kwargs)
        self.chk_paid = self.add_check('ChkPaid', x + self.lbl_width, y - 1, 40, self.FIELD_HEIGHT, Label='')
        y += self.FIELD_HEIGHT + self.ROW_SPACING

        # Notes
        self.add_label('LblNotes', x, y, self.lbl_width, self.LABEL_HEIGHT, Label='Notes', **label_kwargs)
        self.edt_notes = self.add_edit('EdtNotes', x + self.lbl_width, y - 2, self.field_width, self.FIELD_HEIGHT)
        y += self.FIELD_HEIGHT + self.ROW_SPACING

        # Buttons based on mode
        if self.attendee_id is None:
            self._create_buttons_normal()
        else:
            self._create_buttons_edit()

    def _create_buttons_normal(self):
        btn_width = 80
        gap = 10
        count = 2
        total_w = count * btn_width + (count - 1) * gap
        dlg_w = self.POS_SIZE[2]
        start_x = (dlg_w - total_w) // 2
        btn_y = self.POS_SIZE[3] - self.MARGIN - self.BUTTON_HEIGHT

        self.add_cancel('BtnCancel', start_x, btn_y, btn_width, self.BUTTON_HEIGHT)
        self.btn_save = self.add_button('BtnSave', start_x + (btn_width + gap), btn_y, btn_width, self.BUTTON_HEIGHT, Label='Save', DefaultButton=False)
        self.add_action_listener(self.btn_save, self._on_save)

    def _create_buttons_edit(self):
        btn_width = 80
        gap = 10
        count = 3
        total_w = count * btn_width + (count - 1) * gap
        dlg_w = self.POS_SIZE[2]
        start_x = (dlg_w - total_w) // 2
        btn_y = self.POS_SIZE[3] - self.MARGIN - self.BUTTON_HEIGHT

        self.btn_delete = self.add_button('BtnDelete', start_x, btn_y, btn_width, self.BUTTON_HEIGHT, Label='Delete')
        self.add_action_listener(self.btn_delete, self._on_delete)
        self.add_cancel('BtnCancel', start_x + (btn_width + gap), btn_y, btn_width, self.BUTTON_HEIGHT)
        self.btn_save = self.add_button('BtnSave', start_x + 2 * (btn_width + gap), btn_y, btn_width, self.BUTTON_HEIGHT, Label='Save', DefaultButton=False)
        self.add_action_listener(self.btn_save, self._on_save)

    def commit(self) -> dict:
        name = self.edt_name.getText().strip()
        email = self.edt_email.getText().strip()
        phone = self.edt_phone.getText().strip()
        notes = self.edt_notes.getText().strip()
        paid = bool(self.chk_paid.State)
        return {
            'attendee_id': self.attendee_id,
            'session': self.session_id,
            'name': name,
            'email': email,
            'phone': phone,
            'paid': paid,
            'notes': notes,
        }

    def _on_save(self, event=None):
        from librepy.app.service.srv_session_attendee import save_session_attendee
        payload = self.commit()
        result = save_session_attendee(payload, context=self)
        if result.get('ok'):
            self.end_execute(1)
        else:
            errors = result.get('errors') or []
            if isinstance(errors, list) and errors:
                lines = []
                for e in errors:
                    fld = e.get('field') if isinstance(e, dict) else None
                    msg = e.get('message') if isinstance(e, dict) else str(e)
                    if fld and fld != '__all__':
                        lines.append(f"{fld}: {msg}")
                    else:
                        lines.append(str(msg))
                body = "\n".join(lines)
            else:
                body = "Invalid input. Please correct the highlighted fields."
            msgbox(body, "Validation Error")

    def _on_delete(self, event=None):
        if self.attendee_id is None:
            return
        from librepy.app.service.srv_session_attendee import delete_session_attendee
        if not confirm_action("Are you sure you want to delete this attendee?", Title="Confirm Delete"):
            return
        res = delete_session_attendee(self.attendee_id, context=self)
        if res.get('ok'):
            self.end_execute(2)
        else:
            self.logger.error("Failed to delete attendee")
            msgbox("Failed to delete the attendee. Please try again.", "Delete Error")

    def _prepare(self):
        if self.attendee_id is None:
            return
        dao = SessionAttendeeDAO(self.logger)
        rec = dao.get_by_id(self.attendee_id)
        if not rec:
            self.logger.info(f"AttendeeEntryDialog._prepare: no record found for id={self.attendee_id}")
            return
        if not isinstance(rec, dict):
            rec = dao.to_dict(rec)
        self.edt_name.setText((rec.get('name') or '').strip())
        self.edt_email.setText((rec.get('email') or '').strip() if rec.get('email') else '')
        self.edt_phone.setText((rec.get('phone') or '').strip() if rec.get('phone') else '')
        self.chk_paid.State = 1 if rec.get('paid') else 0
        self.edt_notes.setText((rec.get('notes') or '').strip() if rec.get('notes') else '')

    def _dispose(self):
        pass

    def _done(self, ret):
        return ret
