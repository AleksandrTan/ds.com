from django import template

register = template.Library()

def strint(value, arg):
    try:
        return value[arg]
    except IndexError:
        return None

def strtoint(value):
    return int(value)

register.filter('strint', strint)
register.filter('strtoint', strtoint)