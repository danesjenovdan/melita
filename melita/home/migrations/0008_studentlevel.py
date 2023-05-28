# Generated by Django 4.1.7 on 2023-05-28 20:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0007_instructionmethod_name_et_instructionmethod_name_nl_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="StudentLevel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, default="", max_length=50)),
                ("name_nl", models.CharField(blank=True, default="", max_length=50)),
                ("name_et", models.CharField(blank=True, default="", max_length=50)),
                ("name_pl", models.CharField(blank=True, default="", max_length=50)),
                ("name_sl", models.CharField(blank=True, default="", max_length=50)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
