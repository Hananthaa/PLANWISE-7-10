from django.db import models

class Exam(models.Model):
    subject = models.CharField(max_length=100)
    exam_date = models.DateField()

    def __str__(self):
        return self.subject