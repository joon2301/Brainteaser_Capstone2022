# Generated by Django 4.0.4 on 2022-05-19 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0002_board_boardcontents_teaseranswer_delete_itboard'),
    ]

    operations = [
        migrations.CreateModel(
            name='Community',
            fields=[
                ('PostID', models.IntegerField(primary_key=True, serialize=False, verbose_name='번호')),
                ('Title', models.CharField(max_length=50, verbose_name='제목')),
                ('Category', models.CharField(max_length=15)),
                ('AccID', models.CharField(max_length=15, verbose_name='작성자')),
                ('Date', models.DateTimeField(auto_now_add=True, verbose_name='작성일')),
                ('Clicked', models.IntegerField(verbose_name='조회수')),
            ],
            options={
                'db_table': 'community',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='FinalAnswer',
            fields=[
                ('AnswerID', models.IntegerField(primary_key=True, serialize=False, verbose_name='번호')),
                ('AccID', models.CharField(max_length=15, verbose_name='작성자')),
                ('Answer', models.CharField(max_length=100, verbose_name='댓글')),
                ('Date', models.DateTimeField(auto_now_add=True, verbose_name='작성일')),
                ('TeaserID', models.IntegerField(verbose_name='번호')),
                ('Likes', models.IntegerField(verbose_name='추천')),
            ],
            options={
                'db_table': 'final_Answer',
                'managed': False,
            },
        ),
        migrations.AlterModelOptions(
            name='teaseranswer',
            options={'managed': False},
        ),
    ]
