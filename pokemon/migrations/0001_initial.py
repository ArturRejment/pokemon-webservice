# Generated by Django 3.2.6 on 2021-08-15 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pokemon',
            fields=[
                ('pokemon_id', models.PositiveIntegerField(primary_key=True, serialize=False, unique=True)),
            ],
        ),
    ]
