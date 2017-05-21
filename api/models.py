"""API Models definition."""
from django.db import models


class Person(models.Model):
    """Model Person."""

    username = models.CharField(max_length=150)
    facebook_id = models.CharField(max_length=150)
    name = models.CharField(max_length=150)
    gender = models.CharField(max_length=50)

    def __str__(self):
        """Representation of Person Model."""
        return self.username

    class Meta:
        """Meta options from Django."""

        ordering = ['-name']
