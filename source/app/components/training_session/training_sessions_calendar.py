from librepy.app.components.calendar.calendar_view import Calendar
from librepy.app.data.dao.training_session_dao import TrainingSessionDAO
import calendar as py_calendar
import traceback


class TrainingSessionsCalendar(Calendar):
    """
    Calendar specialized for training sessions.

    Implements data loading and entry rendering hooks to display training-session
    pills within the base month grid and scrolling mechanics provided by Calendar.
    """

    # Keep the same component name so route/screen stays unchanged
    component_name = 'calendar'

    def __init__(self, parent, ctx, smgr, frame, ps):
        super().__init__(parent, ctx, smgr, frame, ps, title="Training Sessions")

    # ------------------------------
    # Hook implementations
    # ------------------------------
    def on_print(self, event):
        """Subclass callback for Print button (placeholder)."""
        self.logger.info("Print requested (TrainingSessionsCalendar) - not implemented yet")

    def on_new_entry(self, event):
        """Subclass callback for New Entry button (placeholder)."""
        self.logger.info("New Entry requested (TrainingSessionsCalendar) - not implemented yet")

    def load_calendar_data(self):
        """Load training sessions for the visible month into self.calendar_data.

        Populates: self.calendar_data = { 'YYYY-MM-DD': [ {id, date, title, status}, ... ] }
        """
        try:
            cal = py_calendar.Calendar(6)  # Sunday-first
            dates_iter = list(cal.itermonthdates(self.current_date.year, self.current_date.month))
            if not dates_iter:
                self.calendar_data = {}
                return

            start_day = dates_iter[0]
            end_day = dates_iter[-1]

            dao = TrainingSessionDAO(self.logger)
            sessions = dao.get_sessions_between(start_day, end_day)

            grouped = {}
            for s in sessions or []:
                dt = s.get('date')
                if hasattr(dt, 'strftime'):
                    date_key = dt.strftime('%Y-%m-%d')
                elif isinstance(dt, str):
                    date_key = dt
                else:
                    # Skip invalid
                    continue
                s_norm = {
                    'id': s.get('id'),
                    'date': date_key,
                    'title': s.get('title'),
                    'status': s.get('status'),
                    'color': 0x72ab8a,
                }
                grouped.setdefault(date_key, []).append(s_norm)

            self.calendar_data = grouped
        except Exception as e:
            self.logger.error(f"Error loading training sessions: {e}")
            self.logger.error(traceback.format_exc())
            self.calendar_data = {}

