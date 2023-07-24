from django import template
from django.utils import translation
from icu import Collator, Locale

register = template.Library()


@register.filter()
def sorted_related_lessons(value):
    lang = translation.get_language()
    collator = Collator.createInstance(Locale(lang))
    related_lessons = list(value.related_lessons.all())
    sorted_lessons = sorted(related_lessons, key=lambda x: collator.getSortKey(x.title))
    return list(sorted_lessons)
