from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Page


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
