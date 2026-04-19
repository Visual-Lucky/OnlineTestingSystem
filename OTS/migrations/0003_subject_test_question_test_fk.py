# Generated manually — models had Subject/Test/Question.test but migrations did not.

import django.db.models.deletion
from django.db import migrations, models


def assign_default_test(apps, schema_editor):
    Subject = apps.get_model("OTS", "Subject")
    Test = apps.get_model("OTS", "Test")
    Question = apps.get_model("OTS", "Question")

    subj = Subject.objects.first()
    if subj is None:
        subj = Subject.objects.create(name="General")
    test = Test.objects.filter(subject=subj).first()
    if test is None:
        test = Test.objects.create(subject=subj, name="Default Test")
    Question.objects.filter(test__isnull=True).update(test=test)


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("OTS", "0002_alter_candidate_points_alter_candidate_testattemped"),
    ]

    operations = [
        migrations.CreateModel(
            name="Subject",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Test",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                (
                    "subject",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="OTS.subject"),
                ),
            ],
        ),
        migrations.AddField(
            model_name="question",
            name="test",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="OTS.test",
            ),
        ),
        migrations.RunPython(assign_default_test, noop_reverse),
        migrations.AlterField(
            model_name="question",
            name="test",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="OTS.test",
            ),
        ),
    ]
