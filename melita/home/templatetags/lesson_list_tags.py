from django import template

register = template.Library()


@register.simple_tag
def query_string_replace(request, field, value):
    copied_get = request.GET.copy()
    copied_get[field] = value
    return copied_get.urlencode()
