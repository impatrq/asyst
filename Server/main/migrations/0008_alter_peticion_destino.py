# Generated by Django 3.2.5 on 2021-10-26 15:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carrito', '0005_alter_carrito_rumbo'),
        ('main', '0007_alter_peticion_destino'),
    ]

    operations = [
        migrations.AlterField(
            model_name='peticion',
            name='destino',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='destino', to='carrito.estacion'),
        ),
    ]