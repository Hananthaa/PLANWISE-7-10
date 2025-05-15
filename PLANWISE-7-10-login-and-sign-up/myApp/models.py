from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Login(models.Model):
    name = models.CharField(max_length=400)
    price = models.FloatField(default=0.0)
    image = models.ImageField(null=True, blank=True, upload_to="login/", default="login/login-default.png")
    description = CKEditor5Field(null=True, blank=True)  # Changed to CKEditor5Field
    slug = models.SlugField(unique=True, null=True, max_length=400)
    create_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('login-detail', kwargs={'pk': self.pk, 'slug': self.slug})

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return '%s - %s' % (self.name, self.create_at)
