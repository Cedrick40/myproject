from django.db import models
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    CATEGORY_CHOICES = [
        ("technology", "Technology"),
        ("sports", "Sports"),
        ("politics", "Politics"),
        ("education", "Education"),
        ("business", "Business"),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)  # new
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="technology")

    views = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.name}"
