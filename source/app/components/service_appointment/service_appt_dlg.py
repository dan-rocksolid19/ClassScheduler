from librepy.pybrex import dialog


class ServiceAppointmentDialog(dialog.DialogBase):
    """
    Minimal dialog container for creating/editing a Service Appointment.

    Requirements (no functionality yet):
    - Fields with labels: name, phone #, email, date, time, notes
    - Buttons: Cancel (left), Save (right)
    - All labels the same width
    - All fields the same width
    """

    # x, y, width, height
    POS_SIZE = 0, 0, 520, 300

    # Layout constants
    MARGIN = 16
    ROW_SPACING = 10
    LABEL_HEIGHT = 14
    FIELD_HEIGHT = 22
    BUTTON_HEIGHT = 24

    def __init__(self, parent, ctx, smgr, frame, ps, **props):
        # Basic dialog appearance
        props['Title'] = props.get('Title', 'Service Appointment')
        props['BackgroundColor'] = props.get('BackgroundColor', 0xFFFFFF)

        self.ctx = ctx
        self.parent = parent
        self.smgr = smgr
        self.frame = frame
        self.ps = ps
        self.logger = getattr(parent, 'logger', None)

        # Controls (optional references)
        self.lbl_width = None
        self.field_width = None

        # Pass the parent window (frame.window) to DialogBase for ownership/centering when available
        parent_window = getattr(self.frame, 'window', None) if self.frame is not None else None
        super().__init__(ctx, self.parent, parent_window, **props)

    def _create(self):
        """Create the static UI controls with equal label/field widths."""
        x = self.MARGIN
        y = self.MARGIN

        # Compute equal widths for labels and fields
        total_inner_width = self.POS_SIZE[2] - (self.MARGIN * 2)
        # 30% labels, 70% fields (rounded to integers)
        self.lbl_width = int(total_inner_width * 0.30)
        self.field_width = total_inner_width - self.lbl_width

        label_kwargs = dict(FontWeight=120, FontHeight=11, VerticalAlign=2, Align=2)
        # Align=2 makes label text right-aligned to create a neat column

        # name
        self.add_label('LblName', x, y, self.lbl_width, self.LABEL_HEIGHT, Label='Name', **label_kwargs)
        self.edt_name = self.add_edit('EdtName', x + self.lbl_width, y - 2, self.field_width, self.FIELD_HEIGHT)
        y += self.FIELD_HEIGHT + self.ROW_SPACING

        # phone #
        self.add_label('LblPhone', x, y, self.lbl_width, self.LABEL_HEIGHT, Label='Phone #', **label_kwargs)
        self.edt_phone = self.add_edit('EdtPhone', x + self.lbl_width, y - 2, self.field_width, self.FIELD_HEIGHT)
        y += self.FIELD_HEIGHT + self.ROW_SPACING

        # email
        self.add_label('LblEmail', x, y, self.lbl_width, self.LABEL_HEIGHT, Label='Email', **label_kwargs)
        self.edt_email = self.add_edit('EdtEmail', x + self.lbl_width, y - 2, self.field_width, self.FIELD_HEIGHT)
        y += self.FIELD_HEIGHT + self.ROW_SPACING

        # date
        self.add_label('LblDate', x, y, self.lbl_width, self.LABEL_HEIGHT, Label='Date', **label_kwargs)
        self.edt_date = self.add_date('EdtDate', x + self.lbl_width, y - 2, self.field_width, self.FIELD_HEIGHT)
        y += self.FIELD_HEIGHT + self.ROW_SPACING

        # time
        self.add_label('LblTime', x, y, self.lbl_width, self.LABEL_HEIGHT, Label='Time', **label_kwargs)
        self.edt_time = self.add_time('EdtTime', x + self.lbl_width, y - 2, self.field_width, self.FIELD_HEIGHT)
        y += self.FIELD_HEIGHT + self.ROW_SPACING

        # notes (multi-line)
        notes_height = 70
        self.add_label('LblNotes', x, y, self.lbl_width, self.LABEL_HEIGHT, Label='Notes', **label_kwargs)
        self.edt_notes = self.add_edit('EdtNotes', x + self.lbl_width, y - 2, self.field_width, notes_height, MultiLine=True)
        y += notes_height + self.ROW_SPACING

        btn_y = self.POS_SIZE[3] - self.MARGIN - self.BUTTON_HEIGHT
        btn_width = 80

        # Cancel on the left
        self.add_cancel('BtnCancel', x, btn_y, btn_width, self.BUTTON_HEIGHT)

        # Save on the right
        self.btn_save = self.add_button(
            'BtnSave',
            self.POS_SIZE[2] - self.MARGIN - btn_width,
            btn_y,
            btn_width,
            self.BUTTON_HEIGHT,
            Label='Save',
            DefaultButton=False,
        )
        self.add_action_listener(self.btn_save, self._on_save)

    def commit(self):
        """Collect all field values into a dictionary and log it.
        Returns the dictionary. This does not perform any persistence.
        """
        def _txt(ctrl):
            try:
                return ctrl.getText().strip()
            except Exception:
                return ''
        data = {
            'name': _txt(self.edt_name),
            'phone': _txt(self.edt_phone),
            'email': _txt(self.edt_email),
            'date': _txt(self.edt_date),
            'time': _txt(self.edt_time),
            'notes': _txt(self.edt_notes)
        }
        self.logger.info(f"ServiceAppointmentDialog.commit -> {data}")
        return data

    def _on_save(self, event=None):
        """Action listener for Save button: call commit to gather inputs and log them.
        Keeps the dialog open; does not persist or close.
        """
        try:
            self.commit()
        except Exception as e:
            self.logger.error(f"ServiceAppointmentDialog._on_save error: {e}")

    def _prepare(self):
        pass

    def _dispose(self):
        pass

    def _done(self, ret):
        # No custom behavior yet; just return the result code
        return ret
