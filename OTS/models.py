from django.db import models
import uuid


class Candidate(models.Model):
    username = models.CharField(primary_key=True, max_length=20)
    password = models.CharField(null=False, max_length=20)
    name = models.CharField(null=False, max_length=30)
    testattemped = models.IntegerField(default=0)
    points = models.FloatField(default=0.0)


class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Test(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    duration_minutes = models.IntegerField(default=30)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    qid = models.BigAutoField(primary_key=True, auto_created=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    que = models.TextField()
    a = models.CharField(max_length=255)
    b = models.CharField(max_length=255)
    c = models.CharField(max_length=255)
    d = models.CharField(max_length=255)
    ans = models.CharField(max_length=2)


class Result(models.Model):
    resultid = models.BigAutoField(primary_key=True, auto_created=True)
    username = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, null=True, blank=True)
    teacher = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)
    attempt = models.IntegerField()
    right = models.IntegerField()
    wrong = models.IntegerField()
    points = models.FloatField()
    tab_switches = models.IntegerField(default=0)
    copy_attempts = models.IntegerField(default=0)
    fullscreen_exits = models.IntegerField(default=0)

    class Meta:
        ordering = ['-points', 'date']
