# Generated by Django 4.0.3 on 2022-03-12 08:18

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BookMark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='생성 날짜')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='수정 날짜')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=50, unique=True, verbose_name='코스 이름')),
                ('img_url', models.CharField(max_length=350, unique=True)),
                ('avg_rating', models.FloatField(default=0, verbose_name='평균 평점')),
                ('count_review', models.IntegerField(default=0, verbose_name='리뷰 개수')),
                ('description', models.TextField(blank=True, max_length=1000, verbose_name='코스 설명')),
                ('stand_count', models.PositiveSmallIntegerField(default=0, verbose_name='서서 개수')),
                ('sit_count', models.PositiveSmallIntegerField(default=0, verbose_name='앉아서 개수')),
                ('balance_count', models.PositiveSmallIntegerField(default=0, verbose_name='밸런스 개수')),
                ('core_count', models.PositiveSmallIntegerField(default=0, verbose_name='코어 개수')),
                ('arm_count', models.PositiveSmallIntegerField(default=0, verbose_name='팔 개수')),
                ('recline_count', models.PositiveSmallIntegerField(default=0, verbose_name='누워서 개수')),
            ],
            options={
                'ordering': ['avg_rating', 'course_name'],
            },
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exercise_name', models.CharField(max_length=50, unique=True, verbose_name='운동 이름')),
                ('youtube_key', models.CharField(blank=True, max_length=200, unique=True, verbose_name='유트브 키값')),
                ('youtube_start', models.PositiveSmallIntegerField(blank=True, verbose_name='유트브 시작 초')),
                ('youtube_end', models.PositiveSmallIntegerField(blank=True, verbose_name='유튜브 끝 초')),
                ('exercise_type', models.CharField(max_length=50, verbose_name='운동 타입')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=30, unique=True, verbose_name='해시태그')),
            ],
        ),
        migrations.CreateModel(
            name='CourseReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='생성 날짜')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='수정 날짜')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='삭제 상태')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='삭제 날짜')),
                ('content', models.TextField(max_length=300, verbose_name='내용')),
                ('rating', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='평점')),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review', to='courses.course', verbose_name='코스')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
