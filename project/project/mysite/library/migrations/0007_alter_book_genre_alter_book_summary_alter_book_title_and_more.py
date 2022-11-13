# Generated by Django 4.1.2 on 2022-11-13 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0006_alter_genre_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='genre',
            field=models.ManyToManyField(help_text='Išsirinkite projekto etapą(us)', to='library.genre'),
        ),
        migrations.AlterField(
            model_name='book',
            name='summary',
            field=models.TextField(help_text='Trumpas projekto aprašymas', max_length=1000, verbose_name='Aprašymas'),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Projekto kodas'),
        ),
        migrations.AlterField(
            model_name='bookinstance',
            name='status',
            field=models.CharField(blank=True, choices=[('a', 'Projektas nepradėtas'), ('p', 'Projekto laikas eina į pabaigą'), ('g', 'Projektas baigtas'), ('r', 'Dirbama')], default='a', help_text='Statusas', max_length=1),
        ),
    ]
