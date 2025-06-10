from database.db_utils import log_event

def log(event_type):
    print(f"[EVENT] {event_type}")
    log_event(event_type)