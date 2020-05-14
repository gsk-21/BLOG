from .models import Comment,Post
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def base_context(request):
    if request.user.is_authenticated:

        notifications = Comment.objects.filter(approved_comment=False).filter(post__author=request.user)
        notifications_cnt = len(notifications)

        if(notifications_cnt):
            notification_count = notifications_cnt
        else:
            notification_count = ''

        drafts = Post.objects.filter(author = request.user).filter(published_date = None).order_by('created_date').reverse()
        drafts_cnt = len(drafts)
        if (drafts_cnt):
            draft_count = drafts_cnt
        else:
            draft_count = ''

        return {'notification_count': notification_count,'draft_count':draft_count}
    else:
        return {}
    #return {'count':count}