from django import template

register = template.Library()

def strint(value, arg):
    try:
        return value[arg]
    except IndexError:
        return None

register.filter('strint', strint)