from django import template

register = template.Library()

# Using Decorators instead of register.filter('cut', cut)
@register.filter(name='cut')

def cut(value, arg):
    """
    This is custom template filter that cuts
    all values of "arg" from the string!
    """
    return replace(arg, '')

# register.filter('cut', cut)