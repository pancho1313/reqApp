from django import template

register = template.Library()

@register.filter(name="my_filter")
def myFilter(obj, arg):
    return "lala (:"
