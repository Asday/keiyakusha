# Generated by Django 2.1 on 2018-08-18 14:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clients', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Engagement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateField()),
                ('duration', models.DurationField()),
                ('rate', models.DecimalField(decimal_places=2, max_digits=18)),
                ('currency', models.CharField(max_length=3)),
                ('time_per_week', models.DurationField()),
                ('invoice_period_days', models.PositiveIntegerField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='engagements', to='clients.Client')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='engagements', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
