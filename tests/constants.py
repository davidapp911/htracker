import datetime

DEFAULT_TEST_USER_PASSWORD = "secret123"
HABIT_UPDATE_DATA = {"name": "new_name", "frequency": "monthly"}
COMPLETION_TODAY = {"logged_at": datetime.date.today().isoformat()}
GARBAGE_TOKEN_HEADER = {"Authorization": "Bearer Th1s1s4g4rBaGeT0KeNsTr1nG"}
NOT_FOUND_ID = 999999
APP_LOCAL_URL = "http://localhost:5173"
HABIT_DATA = {"name": "Run 30 miles", "frequency": "weekdays", "completions": "0", "streak": "0"}
API_LOCAL_URL = "http://localhost:8000"
