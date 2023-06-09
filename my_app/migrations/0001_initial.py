# Generated by Django 4.2.1 on 2023-05-09 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChargePoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
                ('status', models.IntegerField(choices=[(1, 'Ready'), (2, 'Charging'), (3, 'Waiting'), (4, 'Error')], default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
