# Generated by Django 4.1.4 on 2023-04-05 11:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0008_delete_userinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birthDate', models.DateField()),
                ('AuthToken', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('favorites', models.ManyToManyField(related_name='FavoritesMovies', to='api.movie')),
                ('userAccount', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('watched', models.ManyToManyField(related_name='WatchedMovies', to='api.movie')),
            ],
        ),
    ]