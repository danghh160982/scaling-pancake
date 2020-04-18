# Generated by Django 3.0.4 on 2020-04-18 06:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('clients', '0001_initial'),
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False,
                                                     help_text='Designates that this user has all permissions without \
                                                     explicitly assigning them.',
                                                     verbose_name='superuser status')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('tel', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=False)),
                ('role',
                 models.SmallIntegerField(choices=[(0, 'USER'), (1, 'ADMIN'), (2, 'SUPER_ADMIN'), (3, 'SYSTEM_ADMIN')],
                                          default=0)),
                ('change_init_password', models.BooleanField(default=False)),
                ('reset_password_token', models.CharField(max_length=255)),
                ('reset_password_token_expired_at', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('client',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users',
                                   to='clients.Client')),
                ('groups', models.ManyToManyField(blank=True,
                                                  help_text='The groups this user belongs to. A user will get all \
                                                  permissions granted to each of their groups.',
                                                  related_name='user_set', related_query_name='user', to='auth.Group',
                                                  verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.',
                                                            related_name='user_set', related_query_name='user',
                                                            to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]