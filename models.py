from django.db import models


class Task(models.Model):
    date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return self.description
        return self.date

