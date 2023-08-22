from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail import blocks
from wagtail.fields import StreamField
from wagtail.models import Page


class HomePage(Page):
    about_page = models.ForeignKey('wagtailcore.Page', null=True, blank=True, related_name='+', on_delete=models.SET_NULL)
    how_to_page = models.ForeignKey('wagtailcore.Page', null=True, blank=True, related_name='+', on_delete=models.SET_NULL)
    about_page_nl = models.ForeignKey('wagtailcore.Page', null=True, blank=True, related_name='+', on_delete=models.SET_NULL)
    how_to_page_nl = models.ForeignKey('wagtailcore.Page', null=True, blank=True, related_name='+', on_delete=models.SET_NULL)
    about_page_et = models.ForeignKey('wagtailcore.Page', null=True, blank=True, related_name='+', on_delete=models.SET_NULL)
    how_to_page_et = models.ForeignKey('wagtailcore.Page', null=True, blank=True, related_name='+', on_delete=models.SET_NULL)
    about_page_pl = models.ForeignKey('wagtailcore.Page', null=True, blank=True, related_name='+', on_delete=models.SET_NULL)
    how_to_page_pl = models.ForeignKey('wagtailcore.Page', null=True, blank=True, related_name='+', on_delete=models.SET_NULL)
    about_page_sl = models.ForeignKey('wagtailcore.Page', null=True, blank=True, related_name='+', on_delete=models.SET_NULL)
    how_to_page_sl = models.ForeignKey('wagtailcore.Page', null=True, blank=True, related_name='+', on_delete=models.SET_NULL)

    parent_page_types = []

    content_panels = Page.content_panels + [
        FieldPanel("about_page"),
        FieldPanel("how_to_page"),
        FieldPanel("about_page_nl"),
        FieldPanel("how_to_page_nl"),
        FieldPanel("about_page_et"),
        FieldPanel("how_to_page_et"),
        FieldPanel("about_page_pl"),
        FieldPanel("how_to_page_pl"),
        FieldPanel("about_page_sl"),
        FieldPanel("how_to_page_sl"),
    ]


class GenericPage(Page):
    body = StreamField(
        [
            ("paragraph", blocks.RichTextBlock(label="Rich text")),
        ],
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]
