from librepy.app.components.settings.tabs.base_tab import BaseTab


class AttendanceTab(BaseTab):
    """
    """

    def __init__(self, dialog, page, ctx, smgr, logger, session_id=None):
        super().__init__(dialog, page, ctx, smgr, logger)
        self.session_id = session_id
        self.grid_base = None
        self.grid = None

    def build(self):
        # Compute page-relative geometry similar to PeopleTab
        page_width = self.dialog.POS_SIZE[2] - (self.dialog.MARGIN * 2)
        page_height = self.dialog.POS_SIZE[3] - (self.dialog.MARGIN * 3) - self.dialog.BUTTON_HEIGHT + 30
        pad = 5

        titles = [
            ("Name", "name", 220, 1),
            ("Attendance", "attendance", 120, 1),
        ]

        grid_x = pad
        grid_y = pad
        grid_w = page_width - (pad * 2)
        grid_h = max(120, page_height - grid_y - pad)

        self.grid_base, self.grid = self.dialog.add_grid(
            'GridAttendance',
            grid_x, grid_y,
            grid_w, grid_h,
            titles,
            page=self.page,
            ShowRowHeader=False,
        )

        # Start with no rows
        self.grid_base.set_data([], heading='name')

    def commit(self) -> dict:
        # No data contribution yet.
        return {}
