from django.contrib.admin.utils import quote
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import redirect
from django.templatetags.static import static
from django.urls import re_path, reverse
from django.utils.decorators import method_decorator
from django.utils.html import format_html
from django.utils.text import slugify
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy
from taggit.models import Tag
from wagtail import hooks
from wagtail.admin import messages
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.modeladmin.helpers import ButtonHelper
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)
from wagtail.contrib.modeladmin.views import InstanceSpecificView

from .models import (
    ActivityType,
    Duration,
    InstructionMethod,
    Language,
    Lesson,
    Material,
    ProgramType,
    StudentLevel,
    Theme,
)

# --- HELPERS


class CopyView(InstanceSpecificView):
    page_title = gettext_lazy("Copy")

    def check_action_permitted(self, user):
        return self.permission_helper.user_can_edit_obj(user, self.instance)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not self.check_action_permitted(request.user):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_meta_title(self):
        return _("Confirm copying of %(object)s") % {"object": self.verbose_name}

    def confirmation_message(self):
        return _("Are you sure you want to copy this %(object)s?") % {
            "object": self.verbose_name
        }

    def copy_instance(self):
        return self.model_admin.copy(self.instance)

    def post(self, request, *args, **kwargs):
        msg = _("%(model_name)s '%(object)s' copied.") % {
            "model_name": self.verbose_name,
            "object": self.instance,
        }
        with transaction.atomic():
            new_instance = self.copy_instance()
        messages.success(request, msg)
        return redirect(self.url_helper.get_action_url("edit", quote(new_instance.pk)))

    def get_template_names(self):
        ma = self.model_admin
        if hasattr(ma, "copy_template_name") and ma.copy_template_name:
            return ma.copy_template_name
        return ma.get_templates("copy")


class ModelAdminCopyMixin:
    copy_view_class = CopyView

    def copy(self, instance):
        raise NotImplementedError(
            "The copy() method must be implemented for each model admin"
        )

    def copy_view(self, request, instance_pk):
        kwargs = {"model_admin": self, "instance_pk": instance_pk}
        view_class = self.copy_view_class
        return view_class.as_view(**kwargs)(request)

    def get_admin_urls_for_registration(self, parent=None):
        urls = super().get_admin_urls_for_registration()

        urls = urls + (
            re_path(
                self.url_helper.get_action_url_pattern("copy"),
                self.copy_view,
                name=self.url_helper.get_action_url_name("copy"),
            ),
        )

        return urls


class LessonButtonHelper(ButtonHelper):
    view_button_classnames = ["button", "button-secondary", "button-small"]

    def view_button(self, obj):
        return {
            "url": reverse("lesson", kwargs={"id": obj.id, "slug": slugify(obj.title)}),
            "label": _("View live"),
            "classname": self.finalise_classname(self.view_button_classnames),
            "title": _("View live"),
        }

    def copy_button(self, pk):
        return {
            "url": self.url_helper.get_action_url("copy", quote(pk)),
            "label": _("Copy"),
            "classname": self.finalise_classname(self.view_button_classnames),
            "title": _("Copy this %(object)s") % {"object": self.verbose_name},
        }

    def get_buttons_for_obj(
        self,
        obj,
        exclude=None,
        classnames_add=None,
        classnames_exclude=None,
    ):
        btns = super().get_buttons_for_obj(
            obj,
            exclude,
            classnames_add,
            classnames_exclude,
        )

        ph = self.permission_helper
        usr = self.request.user
        pk = getattr(obj, self.opts.pk.attname)

        if "copy" not in (exclude or []) and ph.user_can_edit_obj(usr, obj):
            btns.append(self.copy_button(pk))

        if "view" not in (exclude or []):
            btns.append(self.view_button(obj))

        return btns


# --- MODEL ADMIN


class LessonAdmin(ModelAdminCopyMixin, ModelAdmin):
    model = Lesson
    menu_icon = "clipboard-list"
    list_display = ("title", "program_type", "language")
    list_filter = ("program_type", "language")
    search_fields = ("title", "program_type__name", "language__name")
    button_helper_class = LessonButtonHelper

    def copy_related_objects(self, instance, related_objects):
        for related in related_objects:
            related.lesson = instance
            related.pk = None
            related.id = None
            related._state.adding = True
            related.save()

    def copy(self, instance):
        # get reverse key relationships and force db query with list
        key_terms = list(instance.key_terms.all())
        activities = list(instance.activities.all())
        further_reading = list(instance.further_reading.all())
        sources = list(instance.sources.all())
        # get m2m fields and force db query with list
        materials = list(instance.materials.all())
        related_lessons = list(instance.related_lessons.all())
        keywords = list(instance.keywords.all())

        # copy instance
        new_instance = instance
        new_instance.title = f"{instance.title} (copy)"
        new_instance.pk = None
        new_instance.id = None
        new_instance._state.adding = True
        new_instance.save()

        # copy reverse key relationships to new instance
        self.copy_related_objects(new_instance, key_terms)
        self.copy_related_objects(new_instance, activities)
        self.copy_related_objects(new_instance, further_reading)
        self.copy_related_objects(new_instance, sources)
        # set m2m fields on new instance
        new_instance.materials.set(materials)
        new_instance.related_lessons.set(related_lessons)
        new_instance.keywords.set(keywords)
        new_instance.save()

        return new_instance


lesson_admin = LessonAdmin()


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


class StudentLevelAdmin(ModelAdmin):
    model = StudentLevel
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


class TagAdmin(ModelAdmin):
    model = Tag
    menu_icon = "tag"
    list_display = ("name", "slug")
    search_fields = ("name",)
    Tag.panels = [FieldPanel("name")]


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
        StudentLevelAdmin,
        MaterialAdmin,
        ActivityTypeAdmin,
        TagAdmin,
    )


modeladmin_register(LessonsGroup)


# --- HOOKS


@hooks.register("insert_global_admin_css")
def global_admin_css():
    return format_html(
        '<link rel="stylesheet" href="{}">', static("css/custom_admin.css")
    )


class UserbarEditLessonItem:
    def render(self, request):
        if "lesson" not in request.resolver_match.url_name:
            return ""

        try:
            lesson_id = request.resolver_match.kwargs["id"]
        except KeyError:
            return ""

        if not lesson_id:
            return ""

        edit_url = lesson_admin.url_helper.get_action_url("edit", lesson_id)
        return format_html(
            """
            <li class="w-userbar__item " role="presentation">
                <a href="{}" target="_parent" role="menuitem" tabindex="-1">
                    <svg class="icon icon-edit w-action-icon" aria-hidden="true"><use href="#icon-edit"></use></svg>
                    Edit this lesson
                </a>
            </li>
            """,
            edit_url,
        )


@hooks.register("construct_wagtail_userbar")
def add_edit_lesson_item(request, items):
    return items.insert(1, UserbarEditLessonItem())
