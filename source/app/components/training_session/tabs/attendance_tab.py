from librepy.app.components.settings.tabs.base_tab import BaseTab


class AttendanceTab(BaseTab):
    """Attendance tab placeholder.

    For now this tab is intentionally empty. It follows the same wiring pattern as
    existing tabs so future fields or grids can be added without changing the dialog.
    """

    def __init__(self, dialog, page, ctx, smgr, logger, session_id=None):
        super().__init__(dialog, page, ctx, smgr, logger)
        self.session_id = session_id

    def build(self):
        # Minimal placeholder UI element so the tab has some content.
        page_width = self.dialog.POS_SIZE[2] - (self.dialog.MARGIN * 2)
        page_height = self.dialog.POS_SIZE[3] - (self.dialog.MARGIN * 3) - self.dialog.BUTTON_HEIGHT + 30
        x = 10
        y = 10
        w = page_width - 20
        h = 12
        self.dialog.add_label(
            'LblAttendancePlaceholder', x, y, w, h,
            Label='Attendance tab content will go here.',
            page=self.page,
            FontHeight=11,
        )

    def commit(self) -> dict:
        # No data contribution yet.
        return {}
