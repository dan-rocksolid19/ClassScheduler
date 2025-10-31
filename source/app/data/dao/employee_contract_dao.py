from librepy.app.data.base_dao import BaseDAO
from librepy.app.data.model import EmployeeContract, Employee
from datetime import date


class EmployeeContractDAO(BaseDAO):

    def __init__(self, logger):
        super().__init__(EmployeeContract, logger)

    def _row_to_dict(self, row):
        """Map EmployeeContract row to required dict format.
        
        Returns keys:
        - id: contract_id
        - employee_id
        - employee_name: 'First Last' if available
        - start_date
        - end_date
        - time_in, time_out
        - title: display title for calendar entries (defaults to employee_name or 'Contract <id>')
        - status: defaults to 'active'
        """
        try:
            ec = row
            # Try to resolve employee fields whether joined or lazy attribute
            emp = getattr(ec, 'employee', None)
            first = getattr(emp, 'first_name', None) if emp is not None else None
            last = getattr(emp, 'last_name', None) if emp is not None else None
            employee_name = None
            if first or last:
                employee_name = f"{first or ''} {last or ''}".strip()

            title = employee_name or f"Contract {getattr(ec, 'contract_id', '')}"

            return {
                'id': getattr(ec, 'contract_id', None),
                'employee_id': getattr(emp, 'employee_id', None) if emp is not None else None,
                'employee_name': employee_name,
                'start_date': getattr(ec, 'start_date', None),
                'end_date': getattr(ec, 'end_date', None),
                'time_in': getattr(ec, 'time_in', None),
                'time_out': getattr(ec, 'time_out', None),
                'title': title,
                'status': getattr(ec, 'status', 'active') if hasattr(ec, 'status') else 'active',
            }
        except Exception:
            # Fallback minimal dict
            return {
                'id': getattr(row, 'contract_id', None),
                'start_date': getattr(row, 'start_date', None),
                'end_date': getattr(row, 'end_date', None),
                'title': f"Contract {getattr(row, 'contract_id', '')}",
                'status': 'active',
            }

    def get_contracts_between(self, start_date, end_date):
        """Query EmployeeContract rows that overlap the [start_date, end_date] range.

        Overlap condition: end_date >= start_date AND start_date <= end_date
        Returns: List[dict]
        """
        def _query():
            # Join employee to get names (optional)
            query = (EmployeeContract
                     .select(EmployeeContract, Employee)
                     .join(Employee)
                     .where((EmployeeContract.end_date >= start_date) &
                            (EmployeeContract.start_date <= end_date))
                     .order_by(EmployeeContract.start_date))
            return [self._row_to_dict(row) for row in query]

        return self.safe_execute('get_contracts_between', _query, default_return=[])
