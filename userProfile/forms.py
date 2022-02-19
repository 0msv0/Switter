from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . import models


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ('bio',)


class UpdateProfileForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = models.Profile
        fields = ('bio',)


class NewPostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['text']


class NewCommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['text']


class NewReplyForm(forms.ModelForm):
    class Meta:
        model = models.Reply
        fields = ['text']
