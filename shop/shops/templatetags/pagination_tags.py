from django import template

register = template.Library()

@register.filter
def times(number):
    return range(int(number))

@register.filter
def div(value, arg):
    try:
        return int(value) // int(arg)
    except (ValueError, ZeroDivisionError):
        return 0