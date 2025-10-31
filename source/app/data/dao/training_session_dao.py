from librepy.app.data.base_dao import BaseDAO
from librepy.app.data.model import TrainingSession

class TrainingSessionDAO(BaseDAO):

    def __init__(self, logger):
        super().__init__(TrainingSession, logger)

    def _row_to_dict(self, row):
        """Map TrainingSession row to required dict format."""
        try:
            # Peewee row can be model instance or dict-like depending on query
            ts = row
            return {
                'id': getattr(ts, 'session_id', None),
                'date': getattr(ts, 'session_date', None),
                'title': getattr(ts, 'name', None),
                # No explicit status field in model; default to 'scheduled'
                'status': getattr(ts, 'status', 'scheduled') if hasattr(ts, 'status') else 'scheduled',
            }
        except Exception:
            # Fallback minimal dict
            return {
                'id': getattr(row, 'session_id', None),
                'date': getattr(row, 'session_date', None),
                'title': getattr(row, 'name', None),
                'status': 'scheduled',
            }

    def get_sessions_between(self, start_date, end_date):
        """Query TrainingSession rows within [start_date, end_date].

        Returns: List[dict] with keys: id, date (date or 'YYYY-MM-DD'), title, status
        """
        def _query():
            query = (TrainingSession
                     .select()
                     .where((TrainingSession.session_date >= start_date) &
                            (TrainingSession.session_date <= end_date))
                     .order_by(TrainingSession.session_date))
            return [self._row_to_dict(row) for row in query]

        return self.safe_execute('get_sessions_between', _query, default_return=[])

    def get_session_by_id(self, session_id):
        """Fetch one TrainingSession by id.

        Returns: dict with keys: id, date, title, status or None if not found
        """
        def _query():
            row = TrainingSession.get(TrainingSession.session_id == session_id)
            return self._row_to_dict(row)

        return self.safe_execute('get_session_by_id', _query, default_return=None)