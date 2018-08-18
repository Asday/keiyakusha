# Generated by Django 2.1 on 2018-08-18 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('invoices', '0001_initial'),
        ('engagements', '0001_initial'),
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField()),
                ('duration', models.DurationField()),
                ('note', models.CharField(blank=True, max_length=255)),
                ('engagement', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='time_entries', to='engagements.Engagement')),
                ('invoice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='time_entries', to='invoices.Invoice')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='time_entries', to='clients.Task')),
            ],
        ),
    ]
