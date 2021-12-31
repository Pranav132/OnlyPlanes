# Generated by Django 4.0 on 2021-12-31 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='outboundLeg',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='returnLeg',
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
        migrations.AddField(
            model_name='booking',
            name='outboundLeg',
            field=models.ManyToManyField(to='home.OutboundLeg'),
        ),
        migrations.AddField(
            model_name='booking',
            name='returnLeg',
            field=models.ManyToManyField(to='home.ReturnLeg'),
        ),
    ]
