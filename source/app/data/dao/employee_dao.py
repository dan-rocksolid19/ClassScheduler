from librepy.app.data.base_dao import BaseDAO
from librepy.app.data.model import Employee


class EmployeeDAO(BaseDAO):
    """Data-access for Employee model.

    Provides simple helpers to retrieve employees for grid display.
    """

    def __init__(self, logger):
        super().__init__(Employee, logger)

    def create(self, first_name, last_name, email):
        """Create a new Employee and return the model instance."""
        def _q():
            return Employee.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
            )
        return self.safe_execute('create Employee', _q, default_return=None)

    def update(self, employee_id, first_name=None, last_name=None, email=None):
        """Update fields on Employee and return the model instance."""
        updates = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
        }
        self.update_fields(Employee.employee_id == employee_id, updates, operation_name='update Employee')
        def _fetch():
            return Employee.get(Employee.employee_id == employee_id)
        return self.safe_execute('get Employee after update', _fetch, default_return=None)

    def get_all_employees(self):
        """Return list of dicts for all employees.

        Keys: employee_id, first_name, last_name, email
        """
        return self.get_all_dicts(
            fields=[
                'employee_id',
                'first_name',
                'last_name',
                'email',
            ],
            order_by=Employee.last_name,
            operation_name='get_all_employees'
        )

    def get_all_for_grid(self):
        """Return list of dicts tailored for grid display in Employees tab.

        Keys: id, name, email
        """
        rows = self.get_all_employees() or []
        results = []
        for r in rows:
            fn = (r.get('first_name') or '').strip()
            ln = (r.get('last_name') or '').strip()
            full = f"{fn} {ln}".strip() if (fn or ln) else ''
            results.append({
                'id': r.get('employee_id'),
                'name': full,
                'email': r.get('email') or '',
            })
        return results
