# Generated by Django 2.1.7 on 2020-05-09 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=255)),
                ('photo', models.ImageField(default='defo', upload_to='documents/')),
                ('photo_two', models.ImageField(default='defo', upload_to='documents/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('out_put', models.ImageField(default='defo', upload_to='mosaics/')),
                ('out_put_two', models.ImageField(default='defo', upload_to='mosaics/')),
            ],
        ),
    ]
