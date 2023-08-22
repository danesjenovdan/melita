from django import template
from django.utils import translation
from wagtail.models import Site

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


@register.simple_tag(takes_context=True)
def page_for_lang(context, page_name):
    lang = translation.get_language()
    page_attr = page_name if lang == "en" else f"{page_name}_{lang}"
    site = Site.find_for_request(context['request'])
    home_page = site.root_page.specific
    page = getattr(home_page, page_attr)
    return page
