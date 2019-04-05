from django.db import models


class test(models.Model):
    name = models.CharField(max_length=16)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

