from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.db.models import Prefetch
from html_management.models import PostListTemplate
from userapp.forms import RegisterForm
from blogpost.models import BlogPost, PostComment
from userapp.decorators import unauthenticated_user
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
User = get_user_model()



def post_list(request):
    

    template_name = 'blogpost/dynamic.html'
    try:
        template = PostListTemplate.objects.filter(is_active=True).first().template
    except:
        template = "<h1>NO Template has been Selected to Render!</h1>"
    with open('templates/blogpost/dynamic.html', 'w') as f:
        f.write(template)
        f.close()
    posts=BlogPost.objects.all().order_by('-created_at').prefetch_related(
        Prefetch('postcomment_set', queryset=PostComment.objects.filter()))
    page=request.GET.get('page', 1)
    paginator=Paginator(posts, 5)
    try:
        posts=paginator.page(page)
    except PageNotAnInteger:
        posts=paginator.page(1)
    except EmptyPage:
        posts=paginator.page(paginator.num_pages)
    context = {
        'posts': posts,
        'template':template
    }
    return render(request, template_name, context)

@unauthenticated_user
def handleSignup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('userapp/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.info(
                request, 'Please confirm From your email address to complete the registration and Then you can login')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'userapp/register.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.info(
            request, f"Thank you for your email confirmation.  Now you can login your account. {user}")
        return redirect('login')
    else:
        messages.warning(request, 'Activation link is invalid!')
        return redirect('signup')

@unauthenticated_user
def handleLogin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"You are now logged in as {user.email}")
            return redirect('home')
        else:
            messages.error(request, "Invalid email or password.")
    return render(request=request, template_name="userapp/login.html")

@login_required(login_url='login')
def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out!")
    return redirect('home')