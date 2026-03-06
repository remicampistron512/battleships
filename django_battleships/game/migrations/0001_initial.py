from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='GameSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grid_size', models.PositiveSmallIntegerField(default=10)),
                ('water_color', models.CharField(default='#0369a1', max_length=7)),
                ('grid_line_color', models.CharField(default='#7dd3fc', max_length=7)),
                ('hit_color', models.CharField(default='#ef4444', max_length=7)),
                ('miss_color', models.CharField(default='#f8fafc', max_length=7)),
                ('ship_color', models.CharField(default='#22c55e', max_length=7)),
            ],
            options={'verbose_name_plural': 'Game settings'},
        )
    ]
