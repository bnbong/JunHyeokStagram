from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager


class TimeStampedModel(models.Model):

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        abstract = True


class Image(TimeStampedModel):

    file = models.ImageField()
    location = models.CharField(
        max_length=140,
    )
    caption = models.TextField()
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        related_name='images',
        on_delete=models.CASCADE
    )
    tags = TaggableManager()

    @property
    def like_count(self):
        return self.likes.all().count()

    @property
    def comment_count(self):
        return self.comments.all().count()

    def __str__(self):
        return '{} - {}'.format(self.location, self.caption)

    class Meta:
        ordering = ['-created_at']


class Comment(TimeStampedModel):
    message = models.TextField()
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.CASCADE
    )
    image = models.ForeignKey(
        Image,
        null=True,
        related_name='comments',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.message


class Like(TimeStampedModel):

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.CASCADE
    )
    image = models.ForeignKey(
        Image,
        null=True,
        related_name='likes',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return 'User : {} - Image Caption : {}'.format(self.creator.username, self.image.caption)
