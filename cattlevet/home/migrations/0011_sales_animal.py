# Generated by Django 4.0.3 on 2022-04-02 02:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_alter_sales_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='sales',
            name='animal',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='home.animal'),
        ),
    ]
