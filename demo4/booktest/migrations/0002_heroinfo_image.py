# Generated by Django 3.1.6 on 2021-02-15 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booktest', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='heroinfo',
            name='image',
            field=models.ImageField(null=True, upload_to='books', verbose_name='图片'),
        ),
    ]
