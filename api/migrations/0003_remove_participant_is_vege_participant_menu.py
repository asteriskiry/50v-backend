# Generated by Django 4.0 on 2022-07-11 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_participant_is_invited'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participant',
            name='is_vege',
        ),
        migrations.AddField(
            model_name='participant',
            name='menu',
            field=models.CharField(choices=[('VG', 'Kasvis'), ('LI', 'Liha'), ('KA', 'Kala')], default='LI', max_length=2, verbose_name='Menu'),
        ),
    ]