from django.utils import timezone as tz


def get_actual_time():
    current_time = tz.now() # datetime.datetime(2024, 4, 20, 12, 24, 49, 148401, tzinfo=datetime.timezone.utc)
    current_tz = tz.get_current_timezone() # zoneinfo.ZoneInfo(key='Europe/Prague')
    local_tz_time = current_time.astimezone(current_tz) # datetime.datetime(2024, 4, 20, 14, 24, 49, 148401, tzinfo=zoneinfo.ZoneInfo(key='Europe/Prague'))
    
    return local_tz_time