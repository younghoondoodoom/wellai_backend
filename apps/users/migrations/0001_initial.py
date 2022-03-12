# Generated by Django 4.0.3 on 2022-03-12 01:27

import apps.users.models
import apps.users.utils
import apps.users.validators
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='생성 날짜')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='수정 날짜')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='삭제 상태')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='삭제 날짜')),
                ('email', models.EmailField(max_length=254, unique=True, validators=[django.core.validators.EmailValidator()], verbose_name='이메일')),
                ('password', models.CharField(max_length=128, validators=[apps.users.validators.PasswordValidator()], verbose_name='password')),
                ('nickname', models.CharField(default=apps.users.utils.get_nickname, max_length=64, unique=True, verbose_name='닉네임')),
                ('is_staff', models.BooleanField(default=False, verbose_name='관리자여부')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', apps.users.models.CustomUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='생성 날짜')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='수정 날짜')),
                ('gender', models.CharField(blank=True, choices=[(None, ''), ('F', '여'), ('M', '남')], default=None, max_length=1, null=True, verbose_name='성별')),
                ('height', models.PositiveSmallIntegerField(default=0, verbose_name='키')),
                ('weight', models.PositiveSmallIntegerField(default=0, verbose_name='몸무게')),
                ('is_stand', models.BooleanField(default=False, verbose_name='서서')),
                ('is_sit', models.BooleanField(default=False, verbose_name='앉아서')),
                ('is_balance', models.BooleanField(default=False, verbose_name='밸런스')),
                ('is_core', models.BooleanField(default=False, verbose_name='코어')),
                ('is_leg', models.BooleanField(default=False, verbose_name='다리')),
                ('is_back', models.BooleanField(default=False, verbose_name='등')),
                ('user_id', models.OneToOneField(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, related_name='option', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserDailyRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='생성 날짜')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='수정 날짜')),
                ('exercise_date', models.DateField(verbose_name='운동 날짜')),
                ('exercise_week', models.PositiveSmallIntegerField(default=10, editable=False, verbose_name='주차')),
                ('exercise_duration', models.PositiveSmallIntegerField(default=0, verbose_name='일별 총 운동시간')),
                ('calories_total', models.PositiveSmallIntegerField(default=0, verbose_name='일별 총 소모칼로리')),
                ('user_id', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, related_name='daily_record', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='userdailyrecord',
            constraint=models.UniqueConstraint(fields=('user_id', 'exercise_date'), name='users_userdaily_history'),
        ),
    ]
