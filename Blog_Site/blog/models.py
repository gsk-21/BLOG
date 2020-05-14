from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.

class Post(models.Model):

    author = models.ForeignKey('auth.User',on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True,null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approved_comment(self):
        return self.comments.filter(approved_comment = True)

    def get_absolute_url(self):
        if self.published_date is not None:
            return reverse('list-posts')
        else:
            return reverse('drafts')

    def __str__(self):
        return self.title

class Comment(models.Model):

    post = models.ForeignKey('blog.Post',related_name='comments',on_delete=models.CASCADE,null=True)
    author = models.ForeignKey('auth.User',related_name='authors',on_delete=models.CASCADE,null=True)
    #author = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    text = models.TextField()
    approved_comment = models.BooleanField(default=False,null=True)

    def approve(self):
        self.approved_comment = True
        self.save()


    def get_absolute_url(self):
        return reverse('home')

    def __str__(self):
        return self.text


class Profile(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    #picture = models.ImageField(upload_to='profile_pics',blank=True)

    def __str__(self):
        return self.user.username
