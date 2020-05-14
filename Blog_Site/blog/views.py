from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy

#MODEL-VIEWS
from django.views.generic import (TemplateView,CreateView,
                                  UpdateView,DeleteView,ListView,
                                  View)
#MODELS
from .models import Post,Comment

#FORMS
from .forms import PostForm,CommentForm,RegistrationForm

#LOGIN
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect

from django.db.models import Q

# Create your views here.

##################################  CBV #######################################

class Home(ListView):
    context_object_name = 'posts'
    template_name = 'blog/index.html'
    model = Post

    def get_queryset(self):
        return Post.objects.order_by('published_date').reverse()

class AboutUser(ListView):
    template_name = 'auth/about.html'
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = len(Post.objects.filter(author = self.request.user).filter(published_date__isnull = False))
        context['drafts'] = len(Post.objects.filter(author = self.request.user).filter(published_date = None))
        return context


class CreatePost(LoginRequiredMixin,CreateView):

    login_url = '/login/'
    redirect_field_name = 'blog/post-form.html'
    template_name = 'blog/post-form.html'
    form_class = PostForm
    model = Post

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        if obj.published_date is not None:
            return redirect('list-posts')
        return redirect('drafts')

class ListPost(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/list-post.html'
    context_object_name = 'posts'
    template_name = 'blog/my-post.html'
    model = Post

    def get_queryset(self):

        obj = Post.objects.filter(author = self.request.user)
        obj = obj.filter(published_date__isnull = False)
        return obj.order_by('published_date').reverse()
       # return Post.objects.filter(author = self.request.user).order_by('published_date').reverse()

        #return Post.objects.order_by('published_date').reverse()

class DraftList(LoginRequiredMixin,ListView):

    login_url = '/login/'
    redirect_field_name = 'blog/drafts.html'
    context_object_name = 'drafts'
    template_name = 'blog/drafts.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(author = self.request.user).filter(published_date = None).order_by('created_date').reverse()

class UpdatePost(LoginRequiredMixin,UpdateView):

    login_url = '/login/'
    redirect_field_name = 'blog/update-post.html'
    template_name = 'blog/update-post.html'
    form_class = PostForm
    model = Post

    def get_success_url(self):
        if 'from' in self.request.GET:
            return reverse("drafts")
        return reverse("post-detail",kwargs={'pk':self.request.GET['pk']})


class DeletePost(LoginRequiredMixin,DeleteView):
    template_name = 'blog/delete-post.html'
    context_object_name = 'post_to_delete'
    model = Post
    def get_success_url(self):
        print("******************************",self.request)
        if 'from' in self.request.GET:
            return reverse_lazy('drafts')
        else:
            return reverse_lazy('list-posts')

class PostDetail(DeleteView):

    context_object_name = 'post'
    template_name = 'blog/my-post-detail.html'
    model = Post

class PublicPostDetail(DeleteView):

    context_object_name = 'post'
    template_name = 'blog/public-post-detail.html'
    model = Post

class UnAppovedComments(ListView):
    context_object_name = 'comments'
    template_name = 'blog/unapproved-comments.html'
    model = Comment

    def get_queryset(self):

        obj = Comment.objects.filter(approved_comment = False)
        obj = obj.filter(post__author = self.request.user)
        return obj


##################################  FBV #######################################


def comment_list(request,pk):
    post = get_object_or_404(Post,pk=pk)
    return render(request,'blog/comment-list.html',{'post':post})

def comment_approve(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()
    if 'from' in request.GET:
        return redirect('comments-to-approve')
    return redirect('comment-list',pk=comment.post.pk)

def comment_delete(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    if 'from' in request.GET:
        return redirect('comments-to-approve')
    return redirect('comment-list',pk=post_pk)

def publish_post(request,pk):

    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('list-posts')


############################ ADDING COMMENT ###########################
@login_required
def add_comment(request,pk):

    post = get_object_or_404(Post,pk=pk)

    pk = request.GET.get('pk', '')
    title = Post.objects.get(pk=pk).title

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            cmt = form.save(commit=False)
            #name = request.user.first_name + ' ' + request.user.last_name
            cmt.author = request.user
            cmt.post = post
            if post.author == cmt.author:
                cmt.approved_comment = True
            cmt.save()
            return redirect('public-post-detail', pk=pk)
            #return redirect('home')
    else:
        form = CommentForm()

    return render(request,'blog/add-comment.html',{'form':form,'post':title})


########################### USER REGISTRATION ######################################3

def user_registration(request):

    registered = False

    if request.method == 'POST':

        registration_form = RegistrationForm(data=request.POST)

        if registration_form.is_valid():

            user = registration_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print("Some error occured!")
    else:
        registration_form = RegistrationForm()

    return render(request,'auth/register.html',{'form': registration_form,'registered': registered})


################################## USER LOGIN ############################################

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pwd')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse("Account Not Active!")
        else:
            return render(request, 'auth/login.html', {'warning':'INVALID  LOGIN CREDENTIALS!'})
    else:
        return render(request,'auth/login.html',{})

@login_required
def user_edit(request):

    if request.method == 'POST':
        #username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('pwd')

        user = authenticate(username=request.user,password=password)

        if user:
            if user.is_active:
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                return HttpResponseRedirect(reverse('about'))
            else:
                return HttpResponse("Account Not Active!")
        else:
            return render(request, 'auth/edit-user.html', {'warning':'WRONG PASSWORD!'})
    else:
        return render(request,'auth/edit-user.html',{})



@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))