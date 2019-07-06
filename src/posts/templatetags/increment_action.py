from django import template

register = template.Library()

@register.filter(name='increment')
def increment(val = 0):
    val = val + 1
    return val
