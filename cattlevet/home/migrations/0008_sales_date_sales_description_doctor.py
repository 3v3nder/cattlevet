# Generated by Django 4.0.3 on 2022-04-02 01:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0007_animal_book_client_book'),
    ]

    operations = [
        migrations.AddField(
            model_name='sales',
            name='date',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='sales',
            name='description',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('speciality', models.CharField(max_length=200, null=True)),
                ('clientType', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.client')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
