# Generated by Django 4.1.7 on 2023-08-11 15:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0013_alter_activity_description_alter_activity_duration_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="activitytype",
            name="name_et",
            field=models.CharField(blank=True, default="", max_length=255),
        ),
        migrations.AddField(
            model_name="activitytype",
            name="name_nl",
            field=models.CharField(blank=True, default="", max_length=255),
        ),
        migrations.AddField(
            model_name="activitytype",
            name="name_pl",
            field=models.CharField(blank=True, default="", max_length=255),
        ),
        migrations.AddField(
            model_name="activitytype",
            name="name_sl",
            field=models.CharField(blank=True, default="", max_length=255),
        ),
        migrations.AlterField(
            model_name="activitytype",
            name="name",
            field=models.CharField(blank=True, default="", max_length=255),
        ),
    ]
