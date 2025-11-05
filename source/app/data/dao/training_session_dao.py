from librepy.app.data.base_dao import BaseDAO
from librepy.app.data.model import TrainingSession, Teacher
from datetime import time, date

class TrainingSessionDAO(BaseDAO):

    def __init__(self, logger):
        super().__init__(TrainingSession, logger)

    def _row_to_dict(self, row):
        """Map TrainingSession row to minimal dict for calendar usage."""
        ts = row
        return {
            'id': getattr(ts, 'session_id', None),
            'date': getattr(ts, 'session_date', None),
            'title': getattr(ts, 'name', None),
        }

    def create(self, name, teacher, session_date, session_time, price):
        """Create a new TrainingSession and return the model instance.
        """
        def _q():
            return TrainingSession.create(
                name=name,
                teacher=teacher,
                session_date=session_date,
                session_time=session_time,
                price=price,
            )
        return self.safe_execute('create TrainingSession', _q, default_return=None)

    def update(self, session_id, name=None, teacher=None, session_date=None, 
               session_time=None, price=None):
        """Update fields on TrainingSession and return the model instance."""
        updates = {
            'name': name,
            'teacher': teacher,
            'session_date': session_date,
            'session_time': session_time,
            'price': price,
        }
        self.update_fields(
            TrainingSession.session_id == session_id, 
            updates, 
            operation_name='update TrainingSession'
        )
        def _fetch():
            return TrainingSession.get(TrainingSession.session_id == session_id)
        return self.safe_execute('get TrainingSession after update', _fetch, default_return=None)

    def get_sessions_between(self, start_date, end_date):
        """Query TrainingSession rows within [start_date, end_date].

        Returns: List[dict] with keys: id, date (date or 'YYYY-MM-DD'), title
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

        Returns: dict with keys: id, date, title or None if not found
        """
        def _query():
            row = TrainingSession.get(TrainingSession.session_id == session_id)
            return self._row_to_dict(row)

        return self.safe_execute('get_session_by_id', _query, default_return=None)

    def get_training_sessions(self):
        """Return list of sessions joined to teachers for grid display.

        Each dict contains: id, name, teacher_name, session_date, session_time, price
        session_date is formatted as 'YYYY-MM-DD'; session_time as 'HH:MM'.
        """
        def _norm_time(v):
            try:
                if isinstance(v, time):
                    return v.strftime('%H:%M')
                s = str(v) if v is not None else ''
                if len(s) >= 5 and ':' in s:
                    return s[:5]
                return s
            except Exception:
                return str(v) if v is not None else ''

        def _norm_date(v):
            try:
                if isinstance(v, date):
                    return v.strftime('%Y-%m-%d')
                return str(v) if v is not None else ''
            except Exception:
                return str(v) if v is not None else ''

        def _query():
            # Build ORM query using Peewee models, no raw SQL
            query = (
                TrainingSession
                .select(TrainingSession, Teacher)
                .join(Teacher)
                .order_by(TrainingSession.session_date, TrainingSession.session_time)
            )
            results = []
            for ts in query:
                teacher = getattr(ts, 'teacher', None)
                t_first = getattr(teacher, 'first_name', '') or ''
                t_last = getattr(teacher, 'last_name', '') or ''
                teacher_name = f"{t_first} {t_last}".strip()
                rec = {
                    'id': getattr(ts, 'session_id', None),
                    'name': getattr(ts, 'name', ''),
                    'teacher_name': teacher_name,
                    'session_date': _norm_date(getattr(ts, 'session_date', None)),
                    'session_time': _norm_time(getattr(ts, 'session_time', None)),
                    'price': float(getattr(ts, 'price', 0)) if getattr(ts, 'price', None) is not None else None,
                }
                results.append(rec)
            return results

        return self.safe_execute('get_training_sessions', _query, default_return=[]) 