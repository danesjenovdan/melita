# Generated by Django 4.1.7 on 2023-07-24 15:28

from django.db import migrations, models
import wagtail.fields


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0012_alter_activity_aim"),
    ]

    operations = [
        migrations.AlterField(
            model_name="activity",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="activity",
            name="duration",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="activity",
            name="text",
            field=wagtail.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="activity",
            name="type",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
