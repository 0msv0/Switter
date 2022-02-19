from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404

from . import forms, models
from django.contrib.auth import login, authenticate
from django.contrib import messages
from Switter import settings


class Index(View):
    def get(self, request):
        return render(request, 'userProfile/index.html')


def myProfile(request):
    profile = models.Profile.objects.get(profileUser=request.user)

    context = {'profile': profile}
    return render(request, 'userProfile/profile.html', context)


@login_required
def homepage(request):
    global posts, postsN, postN
    postsN = []
    posts = models.Post.objects.none()
    friends = request.user.profile.get_friends()
    profiles = models.Profile.objects.all()
    for profile in profiles:
        for friend in friends:
            if profile.profileUser.id == friend.id or \
                    profile.profileUser.id == request.user.id:
                postTmp = profile.get_posts()
                posts = posts | postTmp

    orderedPosts = posts.order_by('-date')

    for post in orderedPosts:
        likeN = 0
        dislikeN = 0
        likes = post.get_likes()

        for like in likes:
            if like.status == 'like':
                likeN += 1
            else:
                dislikeN += 1

        postN = {'post': post,
                 'like': likeN,
                 'dislike': dislikeN}

        postsN.append(postN)

    context = {'posts': postsN}
    return render(request, 'userProfile/homePage.html', context)


def register_request(request):
    if request.method == "POST":
        uform = forms.NewUserForm(request.POST)
        pform = forms.UserProfileForm(request.POST)
        if uform.is_valid():
            user = uform.save()
            profile = pform.save(commit=False)
            profile.profileUser = user
            profile.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('newUser')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = forms.NewUserForm()
    return render(request=request, template_name="registration/register.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("/account/homePage")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="registration/login.html", context={"login_form": form})


def logout_request(request):
    return render(request, 'registration/logged_out.html')


@login_required
def newUser(request):
    if request.method == 'POST':
        user_form = forms.UpdateUserForm(request.POST, instance=request.user)
        profile_form = forms.UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='account')
    else:
        print('error')
        user_form = forms.UpdateUserForm(instance=request.user)
        profile_form = forms.UpdateProfileForm(instance=request.user.profile)

    return render(request, 'registration/newUser.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def send_friend_request(request, userId):
    sender = request.user.profile
    receiver = User.objects.get(id=userId).profile
    friend_request, created = models.Relationship.objects.get_or_create(
        sender=sender, receiver=receiver, status='send')

    context = {'created': created,
               'receiver': receiver}

    return render(request, 'registration/requestMassage.html', context)


@login_required
def delete_friend_request(request, userId):
    sender = request.user.profile
    receiver = User.objects.get(id=userId).profile
    relations = models.Relationship.objects.all()
    global relate
    for relation in relations:
        if relation.sender.id == sender.id and relation.receiver.id == receiver.id:
            relation.status = 'remove'
            relation.save()
            relate = relation

        if relation.sender.id == receiver.id and relation.receiver.id == sender.id:
            relation.status = 'remove'
            relation.save()
            relate = relation

    context = {'relate': relate}
    return render(request, 'registration/remove_request.html', context)


@login_required
def accept_friend_request(request, requestId):
    friend_request = models.Relationship.objects.get(id=requestId)
    if friend_request.receiver == request.user.profile:
        friend_request.status = 'accepted'
        friend_request.save()
        context = {'sender': friend_request.sender}
        return render(request, 'registration/accept_request.html', context)
    else:
        return HttpResponse('friend request not accepted')


@login_required
def reject_friend_request(request, requestId):
    relate = get_object_or_404(models.Relationship, id=requestId)
    sender = relate.sender
    context = {'sender': sender}
    relate.delete()
    return render(request, 'registration/reject_request.html', context)


@login_required
def friend_request_page(request):
    all_users = User.objects.all()
    context = {'all_users': all_users}
    return render(request, 'userProfile/friend_request.html', context)


@login_required
def requestPage(request):
    all_relations = models.Relationship.objects.all()
    profiles = models.Profile.objects.all()

    context = {'all_relations': all_relations,
               'user': request.user,
               'profiles': profiles}

    return render(request, 'userProfile/requestPage.html', context)


@login_required
def friendList(request):
    allFriends = request.user.profile.get_friends()
    context = {'allFriends': allFriends}

    return render(request, 'userProfile/friendlist.html', context)


def userFriendList(request, userId):
    global userProfileN
    profiles = models.Profile.objects.all()
    for profile in profiles:
        if profile.profileUser.id == userId:
            userProfileN = profile

    context = {'allFriends': userProfileN.get_friends(),
               'id': userId}
    return render(request, 'userProfile/userFriendlist.html', context)


def userProfile(request, profileId):
    global userProfileN
    profiles = models.Profile.objects.all()
    for profile in profiles:
        if profile.profileUser.id == profileId:
            userProfileN = profile

    context = {'profile': userProfileN}

    return render(request, 'userProfile/usersProfile.html', context)


@login_required
def create_post(request):
    user = request.user.profile
    if request.method == "POST":
        form = forms.NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.pUser = user
            data.save()
            messages.success(request, f'Posted Successfully')
            return redirect('/account/homePage')
    else:
        form = forms.NewPostForm()
    return render(request, 'posts/newPost.html', {'form': form})


@login_required
def post_delete(request, pk):
    post = models.Post.objects.get(pk=pk)
    if request.user.profile.id == post.pUser.id:
        models.Post.objects.get(pk=pk).delete()
    return redirect('/account/myPosts/')


@login_required
def postsView(request):
    posts = request.user.profile.get_posts()
    global postsN, postN
    postsN = []

    for post in posts:
        likeN = 0
        dislikeN = 0
        likes = post.get_likes()

        for like in likes:
            if like.status == 'like':
                likeN += 1
            else:
                dislikeN += 1

        postN = {'post': post,
                 'like': likeN,
                 'dislike': dislikeN}

        postsN.append(postN)

    context = {'posts': postsN}

    return render(request, 'posts/postsList.html', context)


@login_required
def postDetail(request, pk):
    post = models.Post.objects.get(id=pk)
    comments = post.get_comments()
    postLikes = post.get_likes()

    global likes, dislikes
    likes = 0
    dislikes = 0

    for like in postLikes:
        if like.status == 'like':
            likes += 1
        else:
            dislikes += 1

    context = {'post': post,
               'comments': comments,
               'likes': likes,
               'dislikes': dislikes}

    return render(request, 'posts/postDetail.html', context)


def userPostView(request, userId):
    global posts, username, idN, postsN, postN
    postsN = []
    profiles = models.Profile.objects.all()
    for profile in profiles:
        if profile.profileUser.id == userId:
            posts = profile.get_posts()
            username = profile.profileUser.username
            idN = profile.profileUser.id

            for post in posts:
                likeN = 0
                dislikeN = 0
                likes = post.get_likes()

                for like in likes:
                    if like.status == 'like':
                        likeN += 1
                    else:
                        dislikeN += 1

                postN = {'post': post,
                         'like': likeN,
                         'dislike': dislikeN}

                postsN.append(postN)

    context = {'posts': postsN,
               'username': username,
               'id': idN}
    return render(request, 'posts/userPostList.html', context)


def userPostDetail(request, userId, postId):
    post = models.Post.objects.get(id=postId)
    comments = post.get_comments()
    postLikes = post.get_likes()

    global likes, dislikes
    likes = 0
    dislikes = 0

    for like in postLikes:
        if like.status == 'like':
            likes += 1
        else:
            dislikes += 1

    context = {'post': post,
               'comments': comments,
               'id': userId,
               'likes': likes,
               'dislikes': dislikes}
    return render(request, 'posts/userPostDetail.html', context)


def createComment(request, postId):
    user = request.user.profile
    post = models.Post.objects.get(id=postId)
    if request.method == "POST":
        form = forms.NewCommentForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = user
            data.post = post
            data.save()
            messages.success(request, f'post comment Successfully')
            id = str(postId)
            userId = str(post.pUser.profileUser.id)
            return redirect('/account/hPost/' + userId + '/' + id)
    else:
        form = forms.NewPostForm()

    context = {'form': form,
               'post': post,
               'user': request.user}
    return render(request, 'posts/newComment.html', context)


def createReplies(request, postId, commentId):
    user = request.user.profile
    post = models.Post.objects.get(id=postId)
    comment = models.Comment.objects.get(id=commentId)

    if request.method == "POST":
        form = forms.NewReplyForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = user
            data.motherComment = comment
            data.save()
            messages.success(request, f'post comment Successfully')
            id = str(postId)
            return redirect('/account/myPost/' + id)
    else:
        form = forms.NewPostForm()

    context = {'form': form,
               'post': post,
               'comment': comment,
               'user': request.user}
    return render(request, 'posts/newReply.html', context)


def showReplies(request, commentId):
    comment = models.Comment.objects.get(id=commentId)
    replies = models.Reply.objects.all()
    dir1 = settings.SERVER_URL

    context = {'comment': comment,
               'replies': replies,
               'dir': dir1}
    return render(request, 'posts/showReplies.html', context)


@login_required
def addLike(request, postId):
    post = models.Post.objects.get(id=postId)
    likes = post.get_likes()
    liked = False

    for like in likes:
        if like.user.profileUser.id == request.user.id:
            if like.status == 'like':
                likes.delete()
            else:
                like.status = 'like'
                like.save()

            liked = True

    if not liked:
        like = models.Like()
        like.post = post
        like.user = request.user.profile
        like.status = 'like'
        like.save()
        post.likes.add(like)

    userIdStr = str(post.pUser.id)
    postIdStr = str(postId)
    url = request.META.get('HTTP_REFERER')

    if '/homePage/' in url:
        return redirect('/account/homePage/')
    elif '/post/' in url:
        return redirect('/account/post/' + userIdStr + '/' + postIdStr + '/')
    else:
        return redirect('/account/myPost/' + postIdStr + '/')


@login_required
def addDislike(request, postId):
    post = models.Post.objects.get(id=postId)
    likes = post.get_likes()
    disliked = False

    for like in likes:
        if like.user.profileUser.id == request.user.id:
            if like.status == 'dislike':
                likes.delete()
            else:
                like.status = 'dislike'
                like.save()
            disliked = True

    if not disliked:
        dislike = models.Like()
        dislike.post = post
        dislike.user = request.user.profile
        dislike.status = 'dislike'
        dislike.save()

        post.likes.add(dislike)

    userIdStr = str(post.pUser.id)
    postIdStr = str(postId)
    url = request.META.get('HTTP_REFERER')

    if '/homePage/' in url:
        return redirect('/account/homePage/')
    elif '/post/' in url:
        return redirect('/account/post/' + userIdStr + '/' + postIdStr + '/')
    else:
        return redirect('/account/myPost/' + postIdStr + '/')
