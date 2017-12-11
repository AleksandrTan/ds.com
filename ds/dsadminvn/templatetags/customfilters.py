from django import template

register = template.Library()

def strint(value, arg):
    return value[arg]

register.filter('strint', strint)