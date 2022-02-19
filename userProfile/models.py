from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Profile(models.Model):
    profileUser = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=500, blank=True)
    userFriends = models.ManyToManyField(User, related_name='friends', blank=True)
    userPosts = models.ManyToManyField('Post', blank=True)

    def get_friends(self):
        return self.userFriends.all()

    def get_friends_no(self):
        return self.userFriends.all().count()

    def get_posts(self):
        return self.userPosts.all()

    def get_posts_no(self):
        return self.userPosts.all().count()

    def __str__(self):
        return self.profileUser.username


STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted'),
    ('remove', 'remove')
)


class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}, {self.receiver}, {self.status}"


class Post(models.Model):
    pUser = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.CharField(max_length=600, help_text='Enter your post:')
    date = models.DateTimeField(default=timezone.now)
    comments = models.ManyToManyField('comment', blank=True, related_name='comments')
    likes = models.ManyToManyField('Like', blank=True, related_name='like')

    def get_likes(self):
        return self.likes.all()

    def get_comments(self):
        return self.comments.all()

    def __str__(self):
        return self.text


class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.CharField(max_length=600, help_text='Enter your comment: ')
    createDate = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text


class Reply(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.CharField(max_length=600, help_text='Enter your comment: ')
    motherComment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    createDate = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text


LIKE_CHOICES = (
    ('like', 'like'),
    ('dislike', 'dislike')
)


class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    status = models.CharField(max_length=8, choices=LIKE_CHOICES)

    def __str__(self):
        return f"{self.user.profileUser.username},{self.post.id},{self.status}"
