from django import template
from django.utils import translation

register = template.Library()


@register.filter()
def name_for_lang(value):
    if not value:
        return ""
    lang = translation.get_language()
    name_attr = "name" if lang == "en" else f"name_{lang}"
    return getattr(value, name_attr)


@register.filter()
def joined_names_for_lang(values, joiner=", "):
    if not values or not len(values):
        return ""
    lang = translation.get_language()
    name_attr = "name" if lang == "en" else f"name_{lang}"
    names = list(map(lambda o: getattr(o, name_attr), values))
    return joiner.join(names)
