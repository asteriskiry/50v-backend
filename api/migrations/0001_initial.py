# Generated by Django 4.0 on 2022-05-29 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ctime', models.DateTimeField(auto_now_add=True, verbose_name='Ilmoittautuminen tehty')),
                ('mtime', models.DateTimeField(auto_now=True, verbose_name='Ilmoittautumista muokattu')),
                ('first_name', models.CharField(max_length=255, verbose_name='Etunimi')),
                ('last_name', models.CharField(max_length=255, verbose_name='Sukunimi')),
                ('starting_year', models.IntegerField(null=True, verbose_name='Opintojen aloitusvuosi')),
                ('email', models.CharField(max_length=255, verbose_name='Email')),
                ('is_asteriski_member', models.BooleanField(verbose_name='Asteriskin jäsen')),
                ('is_alcohol_free', models.BooleanField(verbose_name='Alkoholiton')),
                ('is_vege', models.BooleanField(verbose_name='Lihaton')),
                ('excretory_diets', models.CharField(blank=True, max_length=1024, verbose_name='Eritysruokavaliot ja allergiat')),
                ('is_attending_sillis', models.BooleanField(verbose_name='Osallistuu silliasiaamiaiselle')),
                ('avecs_name', models.CharField(blank=True, max_length=255, verbose_name='Avecin nimi')),
                ('other_info', models.CharField(blank=True, max_length=1024, verbose_name='Pöytäseuruetoiveet ja muut terveiset')),
                ('is_in_reserve', models.BooleanField(default=False, verbose_name='Varasijalla')),
                ('dont_show_name', models.BooleanField(default=False, verbose_name='Ei halua nimen näkyvän listalla')),
                ('is_greeting', models.BooleanField(default=False, verbose_name='Esittää tervehdyksen')),
                ('party_representing', models.CharField(blank=True, max_length=255, verbose_name='Tervehdyksessä edustetut tahot')),
                ('is_consenting', models.BooleanField(verbose_name='Hyväksyy tietosuojaselosteen yms.')),
            ],
            options={
                'verbose_name': 'Ilmoittautuja',
                'verbose_name_plural': 'Ilmoittautuneet',
            },
        ),
    ]