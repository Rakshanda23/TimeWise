# Generated by Django 4.1.4 on 2023-08-05 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generator', '0002_class_author_lecture_author_subject_author_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='classes',
            field=models.JSONField(null=True),
        ),
    ]
