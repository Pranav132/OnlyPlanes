# Generated by Django 4.0 on 2021-12-31 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Segment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('segment_id', models.TextField()),
                ('flightNumber', models.TextField()),
                ('origin', models.TextField()),
                ('originTerminal', models.TextField()),
                ('departureTime', models.TextField()),
                ('destination', models.TextField()),
                ('destinationTerminal', models.TextField()),
                ('arrivalTime', models.TextField()),
                ('duration', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ReturnLeg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('segments', models.ManyToManyField(to='home.Segment')),
            ],
        ),
        migrations.CreateModel(
            name='OutboundLeg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('segments', models.ManyToManyField(to='home.Segment')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seats_available', models.TextField()),
                ('price', models.TextField()),
                ('travelClass', models.TextField()),
                ('outboundLeg', models.ManyToManyField(to='home.OutboundLeg')),
                ('returnLeg', models.ManyToManyField(to='home.ReturnLeg')),
            ],
        ),
    ]
