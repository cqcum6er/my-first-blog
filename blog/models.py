from django.db import models
from django.utils import timezone

class Post(models.Model):  #Defines our model (Post is an object)
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):  #publish is a function/method.
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title #Get a text (string) with a Post title