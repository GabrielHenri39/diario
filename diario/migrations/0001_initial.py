# Generated by Django 5.1.4 on 2025-01-11 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pessoa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('foto', models.ImageField(upload_to='foto')),
            ],
        ),
        migrations.CreateModel(
            name='Diario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('tags', models.TextField()),
                ('texto', models.TextField()),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('pessoas', models.ManyToManyField(to='diario.pessoa')),
            ],
        ),
    ]
