from datetime import datetime, timedelta
from django.http import HttpResponseForbidden


class TimerTamperingMiddleware:
    """
    TimerTamperingMiddleware checks if user modifies JavaScript timer. 
    User's browser is blocked for desired time to not connect to the site.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time_str = request.session.get('timer_tampering_attempt')
        
        if start_time_str:
            start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")

            # modify time for blocking access
            expected_end_time = start_time + timedelta(hours=24)
            if datetime.now() < expected_end_time:
                return HttpResponseForbidden("Přístup zamítnut: Nepovolená manipulace s časovačem.")
        
        response = self.get_response(request)
        return response