from django.utils import timezone as tz


def get_actual_time():
    current_time = tz.now()
    current_tz = tz.get_current_timezone()
    local_tz_time = current_time.astimezone(current_tz)
    return local_tz_time