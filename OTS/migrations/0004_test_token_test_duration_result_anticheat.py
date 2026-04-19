from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('OTS', '0003_subject_test_question_test_fk'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='token',
            field=models.UUIDField(default=uuid.uuid4, unique=True, editable=False),
        ),
        migrations.AddField(
            model_name='test',
            name='duration_minutes',
            field=models.IntegerField(default=30),
        ),
        migrations.AddField(
            model_name='test',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='result',
            name='test',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.deletion.CASCADE, to='OTS.test'),
        ),
        migrations.AddField(
            model_name='result',
            name='tab_switches',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='result',
            name='copy_attempts',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='result',
            name='fullscreen_exits',
            field=models.IntegerField(default=0),
        ),
    ]
