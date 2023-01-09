from django.templatetags.static import static
from django.utils.html import format_html
from wagtail import hooks
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)

from .models import (
    ActivityType,
    Duration,
    InstructionMethod,
    Language,
    Lesson,
    Material,
    ProgramType,
    Theme,
)

# --- MODEL ADMIN


class LessonAdmin(ModelAdmin):
    model = Lesson
    menu_icon = "clipboard-list"
    list_display = ("title", "program_type", "language")
    list_filter = ("program_type", "language")
    search_fields = ("title", "program_type__name", "language__name")


class ProgramTypeAdmin(ModelAdmin):
    model = ProgramType
    menu_icon = "list-ul"
    list_display = ("name",)


class LanguageAdmin(ModelAdmin):
    model = Language
    menu_icon = "list-ul"
    list_display = ("name", "code")


class ThemeAdmin(ModelAdmin):
    model = Theme
    menu_icon = "list-ul"
    list_display = ("name",)


class DurationAdmin(ModelAdmin):
    model = Duration
    menu_icon = "list-ul"
    list_display = ("name",)


class InstructionMethodAdmin(ModelAdmin):
    model = InstructionMethod
    menu_icon = "list-ul"
    list_display = ("name",)


class MaterialAdmin(ModelAdmin):
    model = Material
    menu_icon = "list-ul"
    list_display = ("name",)


class ActivityTypeAdmin(ModelAdmin):
    model = ActivityType
    menu_icon = "list-ul"
    list_display = ("name",)


class LessonsGroup(ModelAdminGroup):
    menu_label = "Lessons"
    menu_icon = "folder-open-inverse"
    menu_order = 200
    items = (
        LessonAdmin,
        ProgramTypeAdmin,
        LanguageAdmin,
        ThemeAdmin,
        DurationAdmin,
        InstructionMethodAdmin,
        MaterialAdmin,
        ActivityTypeAdmin,
    )


modeladmin_register(LessonsGroup)

# --- HOOKS


@hooks.register("insert_global_admin_css")
def global_admin_css():
    return format_html(
        '<link rel="stylesheet" href="{}">', static("css/custom_admin.css")
    )
