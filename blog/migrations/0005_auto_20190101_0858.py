# Generated by Django 2.0 on 2019-01-01 08:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_like'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='post',
        ),
        migrations.DeleteModel(
            name='Like',
        ),
    ]
