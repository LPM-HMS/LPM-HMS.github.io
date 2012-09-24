from django import template
from django.core.urlresolvers import reverse
import time
from django.core.validators import ValidationError

register = template.Library()

@register.simple_tag
def navactive(request, name):
    if name=='home' and request.path=='/':
        return 'active'
    elif name in request.path.split('/'):
        return "active"
    return ""

@register.simple_tag
def status2csstype(status):
    d = {'failed':'danger',
     'successful':'success',
     'no_attempt':'info',
     'in_progress':'warning'}
    return d[status]

@register.filter
def mult(value, arg):
    "Multiplies the arg and the value"
    return int(value) * int(arg)

@register.filter
def format_time(seconds):
    if not seconds:
        seconds =0
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    if d:
        return "%dd:%02d:%02d:%02d" % (d, h, m, s)
    else:
        return "%d:%02d:%02d" % (h, m, s)
        