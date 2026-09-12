from django import template

register = template.Library()

@register.filter(name='cut')
def cut(value, arg):
    """Remove all occurrences of arg from value"""
    return value.replace(arg, '')