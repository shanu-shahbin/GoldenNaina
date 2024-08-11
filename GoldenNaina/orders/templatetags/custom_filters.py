from django import template
import datetime

register = template.Library()

@register.filter(name='format_date')
def format_date(value):
    if isinstance(value, datetime.datetime):
        return value.strftime('%a, %d %b %Y')
    return value
