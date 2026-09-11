from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Shop(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="shops",
    )
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True)
    open_time = models.TimeField()
    close_time = models.TimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shops:detail", args=[self.pk])

    def is_open_now(self):
        if not self.is_active:
            return False
        now = timezone.localtime().time()
        if self.open_time <= self.close_time:
            return self.open_time <= now <= self.close_time
        # Overnight hours, e.g. open 20:00 close 02:00
        return now >= self.open_time or now <= self.close_time
