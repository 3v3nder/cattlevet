# Generated by Django 4.0.3 on 2022-04-02 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_appointment_doctorphone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sales',
            name='date',
            field=models.DateField(),
        ),
    ]