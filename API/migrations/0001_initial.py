# Generated by Django 3.1.5 on 2021-02-03 09:42

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isResolve', models.BooleanField(default=False, verbose_name='是否解决')),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '会话',
                'verbose_name_plural': '会话',
                'db_table': 'Conversation',
                'ordering': ('-created_time',),
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='标题')),
                ('describe', models.TextField(verbose_name='描述')),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='发表时间')),
            ],
            options={
                'verbose_name': '问题',
                'verbose_name_plural': '问题',
                'db_table': 'Question',
                'ordering': ('-created_time',),
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('openID', models.CharField(max_length=50, unique=True, verbose_name='用户标识符')),
                ('nickName', models.CharField(max_length=30, verbose_name='昵称')),
                ('gender', models.CharField(choices=[('M', '男'), ('F', '女')], default=('M', '男'), max_length=5, verbose_name='性别')),
                ('city', models.CharField(blank=True, max_length=20, verbose_name='城市')),
                ('province', models.CharField(blank=True, max_length=20, verbose_name='省份')),
                ('country', models.CharField(blank=True, max_length=20, verbose_name='国家')),
                ('avatarUrl', models.URLField(blank=True, verbose_name='头像地址')),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='注册时间')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
                'db_table': 'User',
                'ordering': ('-created_time',),
            },
        ),
        migrations.CreateModel(
            name='QuestionImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='question/%Y/%m/%d', verbose_name='图片')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.question', verbose_name='关联问题')),
            ],
            options={
                'verbose_name': '问题图片',
                'verbose_name_plural': '问题图片',
                'db_table': 'QuestionImage',
            },
        ),
        migrations.AddField(
            model_name='question',
            name='questioner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.user', verbose_name='提问者'),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(verbose_name='消息')),
                ('mark', models.CharField(choices=[('text', '文本'), ('image', '图片')], default=('text', '文本'), max_length=20, verbose_name='消息类型')),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('conversation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.conversation', verbose_name='关联会话')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.user', verbose_name='发送者')),
            ],
            options={
                'verbose_name': '消息',
                'verbose_name_plural': '消息',
                'db_table': 'Message',
                'ordering': ('-created_time',),
            },
        ),
        migrations.AddField(
            model_name='conversation',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.question', verbose_name='关联问题'),
        ),
        migrations.AddField(
            model_name='conversation',
            name='solvers',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.user', verbose_name='答疑者'),
        ),
    ]