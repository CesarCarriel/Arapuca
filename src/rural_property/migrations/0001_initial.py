# Generated by Django 4.2.14 on 2024-07-17 21:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RuralProperty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='atualizado em')),
                ('code', models.CharField(db_index=True, max_length=20, unique=True, verbose_name='código')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='nome')),
            ],
            options={
                'verbose_name': 'propriedade',
                'db_table': 'rural_property',
            },
        ),
        migrations.CreateModel(
            name='Tract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='atualizado em')),
                ('code', models.CharField(max_length=20, verbose_name='código')),
                ('rural_property', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='rural_property.ruralproperty', verbose_name='propriedade')),
            ],
            options={
                'verbose_name': 'gleba',
                'db_table': 'tract',
            },
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='atualizado em')),
                ('code', models.CharField(max_length=20, verbose_name='código')),
                ('tract', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='rural_property.tract', verbose_name='gleba')),
            ],
            options={
                'verbose_name': 'talhão',
                'verbose_name_plural': 'talhões',
                'db_table': 'field',
            },
        ),
    ]
