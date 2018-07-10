# Generated by Django 2.0.7 on 2018-07-10 16:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CallRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('call_id', models.IntegerField()),
                ('phone_source', models.CharField(blank=True, max_length=11, null=True, validators=[django.core.validators.RegexValidator(regex='^((10)|([1-9][1-9]))\\d{8,9}$')])),
                ('phone_destination', models.CharField(blank=True, max_length=11, null=True, validators=[django.core.validators.RegexValidator(regex='^((10)|([1-9][1-9]))\\d{8,9}$')])),
                ('record_type', models.CharField(max_length=5)),
                ('record_timestamp', models.DateTimeField()),
            ],
        ),
    ]