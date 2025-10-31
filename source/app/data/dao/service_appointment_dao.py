from librepy.app.data.base_dao import BaseDAO
from librepy.app.data.model import ServiceAppointment


class ServiceAppointmentDAO(BaseDAO):

    def __init__(self, logger):
        super().__init__(ServiceAppointment, logger)

    def _row_to_dict(self, row):
        """Map ServiceAppointment row to required dict format."""
        try:
            sa = row
            return {
                'id': getattr(sa, 'service_apt_id', None),
                'date': getattr(sa, 'appointment_date', None),
                'title': getattr(sa, 'name', None),
                # No explicit status field; default to 'scheduled'
                'status': getattr(sa, 'status', 'scheduled') if hasattr(sa, 'status') else 'scheduled',
                'time': getattr(sa, 'appointment_time', None),
                'phone': getattr(sa, 'phone_number', None),
                'email': getattr(sa, 'email', None),
                'notes': getattr(sa, 'notes', None),
            }
        except Exception:
            # Fallback minimal dict
            return {
                'id': getattr(row, 'service_apt_id', None),
                'date': getattr(row, 'appointment_date', None),
                'title': getattr(row, 'name', None),
                'status': 'scheduled',
            }

    def get_appointments_between(self, start_date, end_date):
        """Query ServiceAppointment rows within [start_date, end_date].

        Returns: List[dict] with keys: id, date (date or 'YYYY-MM-DD'), title, status
        """
        def _query():
            query = (ServiceAppointment
                     .select()
                     .where((ServiceAppointment.appointment_date >= start_date) &
                            (ServiceAppointment.appointment_date <= end_date))
                     .order_by(ServiceAppointment.appointment_date))
            return [self._row_to_dict(row) for row in query]

        return self.safe_execute('get_appointments_between', _query, default_return=[])

    def get_appointment_by_id(self, appointment_id):
        """Fetch one ServiceAppointment by id.

        Returns: dict with keys: id, date, title, status or None if not found
        """
        def _query():
            row = ServiceAppointment.get(ServiceAppointment.service_apt_id == appointment_id)
            return self._row_to_dict(row)

        return self.safe_execute('get_appointment_by_id', _query, default_return=None)
