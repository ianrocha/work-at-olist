# Generated by Django 2.0.7 on 2018-07-10 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telephone_bill', '0002_remove_telephonebill_period'),
    ]

    operations = [
        migrations.AddField(
            model_name='telephonebill',
            name='period',
            field=models.DateField(default='2018-07-10'),
            preserve_default=False,
        ),
    ]