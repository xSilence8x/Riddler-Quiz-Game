from django import template

register = template.Library()

@register.filter
def convert_sec_to_min(seconds):
    if seconds:
        min = seconds // 60
        sec = seconds % 60
        return "{:02}:{:02}".format(int(min), int(sec))
    else:
        return "00:00"