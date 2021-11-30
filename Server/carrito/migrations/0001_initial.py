# Generated by Django 3.2.5 on 2021-09-24 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Estacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
                ('ruta', models.JSONField()),
            ],
            options={
                'ordering': ['nombre'],
            },
        ),
    ]
