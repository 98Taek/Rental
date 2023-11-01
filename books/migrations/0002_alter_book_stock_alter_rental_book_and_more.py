# Generated by Django 4.2.4 on 2023-09-16 13:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("books", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="stock",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="rental",
            name="book",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="books",
                to="books.book",
            ),
        ),
        migrations.AlterField(
            model_name="rental",
            name="return_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name="Rating",
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
                (
                    "rating",
                    models.DecimalField(decimal_places=1, max_digits=2, null=True),
                ),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="books.book"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
