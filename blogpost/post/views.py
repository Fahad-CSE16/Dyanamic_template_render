import json
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect, HttpResponseRedirect
from django.views import generic
from django.urls import reverse_lazy
from django.http.response import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from blogpost.models import BlogPost, PostComment
from blogpost.post.forms import BlogPostForm, PostCommentForm
from blogpost.views import *


class BlogPostCreateView(CommonMixin, generic.CreateView):
    permission_required = 'blogpost.create_blogpost'
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blogpost/post/form.html'
    success_message = "Post added successfully"
    title = "Add BlogPost"
    success_url = reverse_lazy("home")

    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        with transaction.atomic():
            self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class BlogPostUpdateView(CommonMixin, generic.UpdateView):
    permission_required = 'blogpost.update_blogpost'
    model = BlogPost
    context_object_name = 'instance'
    form_class = BlogPostForm
    template_name = 'blogpost/post/form.html'
    success_message = "Post updated successfully"
    title = "Update Blog post"
    success_url = reverse_lazy("home")
    
    def form_valid(self, form, *args, **kwargs):
        self.object = form.save(commit=False)
        self.object.updated_by = self.request.user
        with transaction.atomic():
            self.object.save()
        return HttpResponseRedirect(self.get_success_url())
    

def post_detail(request, pk):
    template_name = 'blogpost/post/detail.html'
    item = BlogPost.objects.get(pk=pk)
    context = {
        'item': item, 
        'comments':item.postcomment_set.filter(is_active=True)
    }
    return render(request, template_name, context)

def delete_blog_post(request, pk):
    obj = get_object_or_404(BlogPost, pk=pk)
    if obj.created_by == request.user:
        obj.delete()
        messages.success(request, "Successfully Deleted!")
    else:
        raise PermissionError
    return redirect('home')
    # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class PostCommentCreateView(CommonMixin, generic.CreateView):
    permission_required = 'blogpost.create_postcomment'
    model = PostComment
    form_class = PostCommentForm
    success_message = "Comment added successfully"

    def get_success_url(self, **kwargs):  
        return reverse_lazy("blogpost_detail", kwargs = {'pk': self.blog_post.id})

    def form_valid(self, form, *args, **kwargs):
        pk = self.kwargs.get('pk')
        self.blog_post = BlogPost.objects.get(pk=pk)
        self.object = form.save(commit=False)
        self.object.post = self.blog_post
        self.object.created_by = self.request.user
        with transaction.atomic():
            self.object.save()
        return HttpResponseRedirect(self.get_success_url())

def delete_blog_comment(request, pk):
    obj = get_object_or_404(PostComment, pk=pk)
    obj.delete()
    messages.success(request, "Successfully Deleted!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))