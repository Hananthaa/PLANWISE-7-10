from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field


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


