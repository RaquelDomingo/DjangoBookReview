from django import template
register = template.Library()

@register.filter
def range_maker(value):
    return range(value)