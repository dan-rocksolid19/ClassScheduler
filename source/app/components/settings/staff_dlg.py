from librepy.pybrex import dialog


class StaffDialog(dialog.DialogBase):
    """
    Empty dialog for future Staff management. For now, it only provides OK/Cancel
    buttons positioned at the lower-right corner.
    """

    POS_SIZE = 0, 0, 420, 260
    MARGIN = 12
    BUTTON_HEIGHT = 22

    def __init__(self, ctx, parent, logger, **props):
        props['Title'] = props.get('Title', 'Staff')
        self.ctx = ctx
        self.parent = parent
        self.logger = logger
        super().__init__(ctx, self.parent, **props)

    def _create(self):
        # Optional placeholder content area
        x = self.MARGIN
        y = self.MARGIN
        w = self.POS_SIZE[2] - (self.MARGIN * 2)
        h = self.POS_SIZE[3] - (self.MARGIN * 3) - self.BUTTON_HEIGHT

        btn_width = 70
        gap = 8
        btn_y = self.POS_SIZE[3] - self.MARGIN - self.BUTTON_HEIGHT
        ok_x = self.POS_SIZE[2] - self.MARGIN - btn_width
        cancel_x = ok_x - gap - btn_width

        # Cancel
        self.add_cancel('BtnCancel', cancel_x, btn_y, btn_width, self.BUTTON_HEIGHT)
        # OK
        self.add_button('BtnOK', ok_x, btn_y, btn_width, self.BUTTON_HEIGHT, Label='OK', PushButtonType=1, DefaultButton=True)

    def _prepare(self):
        pass

    def _dispose(self):
        pass

    def _done(self, ret):
        return ret
