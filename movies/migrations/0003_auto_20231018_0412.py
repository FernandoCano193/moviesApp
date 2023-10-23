# Generated by Django 3.2.12 on 2023-10-18 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_person_biography_person_birth_date_person_character_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='biography',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='place_birth',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]