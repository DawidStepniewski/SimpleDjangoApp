from django.db import models


class Books(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=200)
    create_time = models.DateTimeField('create time')
    last_edit_time = models.DateTimeField('last edit time')
