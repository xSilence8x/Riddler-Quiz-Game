from datetime import datetime, timedelta
from django.http import HttpResponseForbidden


class TimerTamperingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time_str = request.session.get('timer_tampering_attempt')
        print(f"{start_time_str}")
        
        if start_time_str:
            start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")

            # modify time for blocking access
            expected_end_time = start_time + timedelta(minutes=1)
            print(f"expected{expected_end_time}")
            if datetime.now() < expected_end_time:
                print("condition true")
                return HttpResponseForbidden("Přístup zamítnut: Nepovolená manipulace s časovačem.")
        
        response = self.get_response(request)
        return response