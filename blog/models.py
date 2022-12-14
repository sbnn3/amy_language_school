from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()

class Author(models.Model):
    """
    Blog Post Author
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    """
    Blog Post Category
    """
    title = models.CharField(max_length=20)
    subtitle = models.CharField(max_length=20)
    slug = models.SlugField()
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.title

    
class Post(models.Model):
    """
    Blog Post Model
    """
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    categories = models.ManyToManyField(Category)
    featured = models.BooleanField()

    def __str__(self):
        return self.title
