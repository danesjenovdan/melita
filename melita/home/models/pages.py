from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail import blocks
from wagtail.fields import StreamField
from wagtail.models import Page


class HomePage(Page):
    parent_page_types = []


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
