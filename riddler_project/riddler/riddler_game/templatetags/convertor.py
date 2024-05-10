from django import template

register = template.Library()

@register.filter
def convert_sec_to_min(seconds):
    """
    This custom filter converts elapsed time of a quiz from seconds to minutes.
    It returns the time in a format mm:ss
    """
    if seconds:
        min = seconds // 60
        sec = seconds % 60
        return "{:02}:{:02}".format(int(min), int(sec))
    else:
        return "00:00"