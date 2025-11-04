from librepy.pybrex import dialog


class TeacherEntryDialog(dialog.DialogBase):
    """
    Minimal placeholder dialog for creating/editing a Teacher entry.
    For now it only shows a title label and OK/Cancel buttons.
    """

    POS_SIZE = 0, 0, 360, 200

    def __init__(self, ctx, parent, logger, **props):
        props['Title'] = props.get('Title', 'Teacher Entry')
        self.ctx = ctx
        self.parent = parent
        self.logger = logger
        super().__init__(ctx, self.parent, **props)

    def _create(self):
        margin = 12
        content_w = self.POS_SIZE[2] - (margin * 2)

        # Placeholder label
        self.add_label(
            'LblTeacherEntryPlaceholder',
            margin, margin,
            content_w, 14,
            Label='Teacher Entry (Empty Placeholder)',
            FontWeight=150,
        )

        # Buttons at bottom-right
        btn_width = 70
        btn_height = 22
        btn_y = self.POS_SIZE[3] - margin - btn_height
        ok_x = self.POS_SIZE[2] - margin - (btn_width * 2) - 8
        cancel_x = self.POS_SIZE[2] - margin - btn_width

        self.add_button('BtnOK', ok_x, btn_y, btn_width, btn_height, Label='OK', PushButtonType=1, DefaultButton=True)
        self.add_button('BtnCancel', cancel_x, btn_y, btn_width, btn_height, Label='Cancel', PushButtonType=2)

    def _prepare(self):
        pass

    def _dispose(self):
        pass

    def _done(self, ret):
        return ret
