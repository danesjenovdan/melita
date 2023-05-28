# Generated by Django 4.1.7 on 2023-05-28 20:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0008_studentlevel"),
    ]

    operations = [
        migrations.AddField(
            model_name="lesson",
            name="student_level",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="home.studentlevel",
            ),
        ),
    ]