# Generated by Django 5.0.7 on 2024-07-23 10:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_remove_comment_user_alter_comment_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='image',
        ),
        migrations.AddField(
            model_name='post',
            name='image1',
            field=models.ImageField(blank=True, null=True, upload_to='post_images/', verbose_name='Фото 1'),
        ),
        migrations.AddField(
            model_name='post',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to='post_images/', verbose_name='Фото 2'),
        ),
        migrations.AddField(
            model_name='post',
            name='image3',
            field=models.ImageField(blank=True, null=True, upload_to='post_images/', verbose_name='Фото 3'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='user_avatar'),
        ),
        migrations.CreateModel(
            name='PostPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='Post_photo', verbose_name='Фото')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.post', verbose_name='Пост')),
            ],
            options={
                'verbose_name': 'Фото',
                'verbose_name_plural': 'Фотографии',
            },
        ),
    ]
