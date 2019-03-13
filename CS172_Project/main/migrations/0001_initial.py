# Generated by Django 2.1.7 on 2019-03-10 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tweets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash_tag', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('tweet_id', models.IntegerField()),
                ('retweet_count', models.IntegerField()),
                ('user_name', models.CharField(max_length=200)),
                ('tweet_text', models.TextField()),
                ('favorite_count', models.IntegerField()),
            ],
        ),
    ]