# Generated by Django 4.0.3 on 2022-05-28 06:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_community_finalanswer_alter_teaseranswer_options'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='teaseranswer',
            table='teaserAnswer',
        ),
    ]
