from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.files import File


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatar_files/', blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        default_img = '%s%s' % (settings.STATICFILES_DIRS[0], '/images/default_avatar.jpeg')
        user_profile = UserProfile.objects.create(user=instance)
        user_profile.avatar.save('default_img.png', File(open(default_img, 'rb')))


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '{0}-{1}-"{2}"'.format(self.sender.username, self.timestamp, self.content)


class Room(models.Model):
    """
    A room for people to chat in.
    """
    title = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    messages = models.ManyToManyField(Message, blank=True)
    participants = models.ManyToManyField(User, related_name='rooms', blank=True)

    def __unicode__(self):
        return '{0}'.format(self.title)

    @property
    def group_name(self):
        """
        Returns the Channels Group name that sockets should subscribe to to get sent
        messages as they are generated.
        """
        return "room-%s" % self.id
