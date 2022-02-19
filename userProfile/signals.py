from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

from .models import Relationship, Post, Comment, Like


@receiver(post_save, sender=Relationship)
def post_save_add_to_friends(sender, created, instance, **kwargs):
    sender_ = instance.sender
    receiver_ = instance.receiver
    if instance.status == 'accepted':
        sender_.userFriends.add(receiver_.profileUser)
        receiver_.userFriends.add(sender_.profileUser)
        sender_.save()
        receiver_.save()


@receiver(post_save, sender=Relationship)
def post_save_remove_friends(sender, created, instance, **kwargs):
    sender_ = instance.sender
    receiver_ = instance.receiver
    if instance.status == 'remove':
        sender_.userFriends.remove(receiver_.profileUser)
        receiver_.userFriends.remove(sender_.profileUser)
        sender_.save()
        receiver_.save()

        relate = get_object_or_404(Relationship, id=instance.id)
        relate.delete()


@receiver(post_save, sender=Post)
def post_save_add_post(sender, created, instance, **kwargs):
    profile = instance.pUser
    profile.userPosts.add(instance)


@receiver(post_save, sender=Comment)
def post_save_add_Comment(sender, created, instance, **kwargs):
    post = instance.post
    post.comments.add(instance)
