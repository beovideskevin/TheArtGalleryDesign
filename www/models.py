from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

class Artwork(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    category = models.ManyToManyField(
        Category,
        blank=False,
        related_name="post"
    )
    url = models.CharField(max_length=200, blank=True, null=True)
    thumbnail = models.CharField(max_length=200, blank=True, null=True)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    alt = models.CharField(max_length=200, blank=True, null=True, default="")
    index = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
