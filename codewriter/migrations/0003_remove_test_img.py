# Generated by Django 4.0.5 on 2022-06-04 04:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codewriter', '0002_test_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test',
            name='img',
        ),
    ]