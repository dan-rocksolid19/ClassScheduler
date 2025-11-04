from .base_tab import BaseTab
from librepy.app.data.dao.employee_dao import EmployeeDAO


class EmployeesTab(BaseTab):
    def __init__(self, dialog, page, ctx, smgr, logger):
        super().__init__(dialog, page, ctx, smgr, logger)
        self.grid_base = None
        self.grid = None

    def build(self):
        # Define grid columns: (Title, field_key, width, stretch)
        titles = [
            ("ID", "id", 70, 1),
            ("Name", "name", 220, 1),
            ("Email", "email", 220, 1),
        ]
        # Create grid within the tab page
        self.grid_base, self.grid = self.dialog.add_grid(
            'GridEmployees',
            10, 10,
            460, 300,
            titles,
            page=self.page,
            ShowRowHeader=False,
        )
        # Load data initially
        self.load_data()

    def load_data(self):
        try:
            dao = EmployeeDAO(self.logger)
            rows = dao.get_all_for_grid() or []
            self.grid_base.set_data(rows, heading='id')
        except Exception as e:
            self.logger.error(f"EmployeesTab.load_data error: {e}")
