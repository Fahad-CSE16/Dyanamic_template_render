from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from html_management.models import PostListTemplate

@login_required(login_url='login')
def html_templates_list(request):
    if request.user.is_staff:
        template_name = 'html_management/list.html'
        context={
            'items':PostListTemplate.objects.all()
        }
        return render(request, template_name, context)
    else:
        raise PermissionError

@login_required(login_url='login')
def html_template_activate(request, pk):
    if request.user.is_staff:
        obj = PostListTemplate.objects.get(pk=pk)
        with transaction.atomic():
            others_obj = PostListTemplate.objects.exclude(pk=pk).update(is_active=False)
            obj.is_active = True
            obj.save()
        messages.success(request, "Successfully Activated!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        raise PermissionError
