# Generated by Django 4.2.14 on 2024-07-18 14:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('insect_trap', '0002_insecttrap_created_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='InsectTrapResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='atualizado em')),
                ('insect_number', models.PositiveIntegerField(verbose_name='número de insetos')),
                ('observation', models.TextField(blank=True, null=True, verbose_name='observações')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='criado por')),
                ('insect_trap', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='insect_trap.insecttrap', verbose_name='armadilha')),
            ],
            options={
                'verbose_name': 'resultado de armadilha',
                'verbose_name_plural': 'resultados de armadilhas',
                'db_table': 'insect_trap_result',
            },
        ),
    ]
