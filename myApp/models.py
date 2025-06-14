from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
from django.db import models
from django.contrib.auth.models import User

#pet timer
class Pet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    pet = models.CharField(max_length=200)

    def __str__(self):
        return self.pet

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender} to {self.receiver} at {self.timestamp}"


class Exam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.CharField(max_length=100)
    exam_date = models.DateField()
    mark = models.IntegerField(null=True, blank=True)  # Optional field for marks

    def __str__(self):
        return self.subject


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_tasks')  # Owner of the task
    shared_with = models.ManyToManyField(User, related_name='shared_tasks', blank=True)  # Users the task is shared with

    def __str__(self):
        return self.title

class HabitRecord(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('task', 'date')

    def __str__(self):
        return f"{self.task.title} - {self.date}"

class Login(models.Model):
    name = models.CharField(max_length=400)
    price = models.FloatField(default=0.0)
    image = models.ImageField(null=True, blank=True, upload_to="login/", default="login/login-default.png")
    description = CKEditor5Field(null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, max_length=400)
    create_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('login-detail', kwargs={'pk': self.pk, 'slug': self.slug})

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} - {self.create_at}'


class ForumPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='forum_images/', null=True, blank=True)  # new
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



class Comment(models.Model):
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.title}'

#tracker
class Subject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.CharField(max_length=100)
    exam_date = models.DateField()

    def __str__(self):
        return self.subject
    
class Topic(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    topiccomplete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} (under {self.subject.subject})"

class DailyNote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"

