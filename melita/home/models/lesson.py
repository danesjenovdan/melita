from django import forms
from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.models import ClusterableModel, ParentalKey, ParentalManyToManyField
from taggit.models import TaggedItemBase
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import RichTextField
from wagtail.models import Orderable
from wagtailautocomplete.edit_handlers import AutocompletePanel


class TranslatableName(models.Model):
    name = models.CharField(max_length=255, default="", blank=True)
    name_nl = models.CharField(max_length=255, default="", blank=True)
    name_et = models.CharField(max_length=255, default="", blank=True)
    name_pl = models.CharField(max_length=255, default="", blank=True)
    name_sl = models.CharField(max_length=255, default="", blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        abstract = True


class ProgramType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


class Language(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.code})"


class KeyTerm(Orderable):
    lesson = ParentalKey("Lesson", on_delete=models.CASCADE, related_name="key_terms")

    term = models.CharField(max_length=50)
    definition = models.TextField()
    source_description = models.CharField(max_length=200, blank=True, null=True)
    source_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.term}"


class Theme(TranslatableName):
    pass


class Duration(TranslatableName):
    pass


class InstructionMethod(TranslatableName):
    pass


class StudentLevel(TranslatableName):
    pass


class PrepTime(models.IntegerChoices):
    ONE = 1, "*"
    TWO = 2, "**"
    THREE = 3, "***"
    # FOUR = 4, "****"
    # FIVE = 5, "*****"


class Material(TranslatableName):
    pass


class ActivityType(TranslatableName):
    color = models.CharField(
        max_length=30,
        help_text="Any valid CSS color format (e.g. #fff, #ffffff, rgb(255, 255, 255), ...)",
    )

    def __str__(self):
        return f"{self.name}"


class Activity(Orderable):
    lesson = ParentalKey("Lesson", on_delete=models.CASCADE, related_name="activities")

    activity_type = models.ForeignKey(ActivityType, on_delete=models.PROTECT)
    duration = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    aim = models.TextField(blank=True, null=True)
    text = RichTextField(
        features=[
            "h3",
            "h4",
            "ul",
            "ol",
            "bold",
            "italic",
            "link",
            "document-link",
            "image",
            "embed",
        ],
        blank=True,
        null=True,
    )


class LessonTag(TaggedItemBase):
    content_object = ParentalKey(
        "Lesson", on_delete=models.CASCADE, related_name="tagged_items"
    )


class FurtherReading(Orderable):
    lesson = ParentalKey(
        "Lesson", on_delete=models.CASCADE, related_name="further_reading"
    )

    source_description = models.CharField(max_length=200, blank=True, null=True)
    source_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.source_description}"


class Source(Orderable):
    lesson = ParentalKey("Lesson", on_delete=models.CASCADE, related_name="sources")

    source_description = models.CharField(max_length=200, blank=True, null=True)
    source_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.source_description}"


class Lesson(ClusterableModel):
    program_type = models.ForeignKey(ProgramType, on_delete=models.PROTECT)
    language = models.ForeignKey(Language, on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    description = RichTextField(features=["ul"])
    lesson_file = models.ForeignKey(
        "wagtaildocs.Document",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="+",
    )
    slides_file = models.ForeignKey(
        "wagtaildocs.Document",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="+",
    )
    worksheets_file = models.ForeignKey(
        "wagtaildocs.Document",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="+",
    )
    theme = models.ForeignKey(Theme, on_delete=models.PROTECT)
    duration = models.ForeignKey(Duration, on_delete=models.PROTECT)
    instruction_method = models.ForeignKey(InstructionMethod, on_delete=models.PROTECT)
    student_level = models.ForeignKey(StudentLevel, on_delete=models.PROTECT, null=True)
    prep_time = models.IntegerField(choices=PrepTime.choices)
    materials = ParentalManyToManyField(Material, blank=True)
    goals = RichTextField(features=["ul"], blank=True, null=True)
    keywords = ClusterTaggableManager(
        through=LessonTag, blank=True, verbose_name="Keywords"
    )
    pedagogical_tips_and_recommendations = RichTextField(
        features=["ul"], blank=True, null=True
    )
    related_lessons = ParentalManyToManyField("self", blank=True)

    panels = [
        FieldPanel("program_type"),
        FieldPanel("language"),
        FieldPanel("title"),
        InlinePanel("key_terms", heading="Key terms", label="Key term"),
        FieldPanel("description"),
        FieldPanel("lesson_file"),
        FieldPanel("slides_file"),
        FieldPanel("worksheets_file"),
        FieldPanel("theme"),
        FieldPanel("duration"),
        FieldPanel("instruction_method"),
        FieldPanel("student_level"),
        FieldPanel("prep_time"),
        FieldPanel("materials", widget=forms.CheckboxSelectMultiple),
        FieldPanel("goals"),
        InlinePanel("activities", heading="Activities", label="Activity"),
        FieldPanel("keywords"),
        FieldPanel("pedagogical_tips_and_recommendations"),
        InlinePanel(
            "further_reading", heading="Further reading", label="Further reading"
        ),
        InlinePanel("sources", heading="Sources", label="Source"),
        AutocompletePanel("related_lessons"),
    ]

    def __str__(self):
        return f"{self.title} - {self.program_type} - {self.language}"
