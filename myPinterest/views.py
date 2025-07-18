import requests
from urllib.parse import urlparse
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from myPinterest.models import Pin, SavedPin,Likes,Comments,Following


def signin_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not User.objects.filter(email=email).exists():
            messages.error(request, "Account not found!")
            return redirect('signin')

        user = authenticate(username=email, password=password)
        if not user:
            messages.error(request, "Incorrect password!")
            return redirect("signin")

        login(request, user)
        # messages.success(request, "Login successfully")
        return redirect("home")

    return render(request, 'project/index.html')


def signup_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered!")
            return redirect('signup')

        user = User.objects.create_user(
            username=email, email=email, password=password)
        messages.success(request, "Account created successfully!")
        return redirect('signin')

    return render(request, 'project/signup.html')


def logout_view(request):
    logout(request)
    messages.success(request, "Successfully Logout !")
    return redirect('signin')


@login_required(login_url='signin')
def home_view(request):
    uploader = User.objects.get(email='ravikiran123223@gmail.com')
    pins = Pin.objects.filter(uploaded_by=uploader).order_by('?')
    username = request.user.username if request.user.is_authenticated else None
    first_letter = username[0].upper()
    return render(request, 'project/home.html', {'pins': pins, 'letter': first_letter})


@login_required(login_url='signin')
def specific_view(request, pin_id):
    pin = Pin.objects.get(id=pin_id)
    related_pins = Pin.objects.filter(
        category=pin.category).exclude(id=pin.id).order_by("?")
    username = request.user.username if request.user.is_authenticated else None
    first_letter = username[0].upper()
    saved_pin_ids = list(
        request.user.savedpin_set.values_list('pin_id', flat=True)
    )
    
    likes = Likes.objects.filter(pin=pin).count()
    user_liked = Likes.objects.filter(user=request.user, pin=pin).exists()

    comments = Comments.objects.filter(pin=pin).select_related('user')
    comment_count = comments.count()
    return render(request, 'project/single.html', {
        'pin': pin,
        'related_pins': related_pins,
        'letter': first_letter,
        'saved_pin_ids': saved_pin_ids,
        'likes': likes,
        'user_liked': user_liked,
        'comments': comments,
        'comment_count': comment_count,
    })


@login_required(login_url='signin')
def user_view(request):
    user = request.user
    username = request.user.username if request.user.is_authenticated else None
    first_letter = username[0].upper()
    email = request.user.email
    saved_pins = SavedPin.objects.filter(user=request.user).order_by('-id')
    pins = [saved.pin for saved in saved_pins]
    created_pins = Pin.objects.filter(uploaded_by=user).order_by('-created_at')

    following_count = user.following_set.count()
    return render(request, 'project/user_details.html', {'letter': first_letter,
                                                         'email': email,
                                                         'saved_pins': pins,
                                                         'created_pins': created_pins,
                                                         'following_count': following_count, })


@login_required(login_url="signin")
def toggle_save(request, pin_id):
    if request.method == "POST":
        pin = get_object_or_404(Pin, id=pin_id)
        saved_pin, created = SavedPin.objects.get_or_create(
            user=request.user, pin=pin)

        if not created:
            saved_pin.delete()
        return redirect('specific', pin_id=pin.id)


@login_required(login_url='signin')
def likes_view(request, pin_id):
    if request.method == "POST":
        pin = get_object_or_404(Pin, id=pin_id)
        user = request.user
        like = Likes.objects.filter(user=user, pin=pin).first()
        if like:
            like.delete()
        else:
            Likes.objects.create(user=user, pin=pin)

        return redirect('specific', pin_id=pin.id)


def comments_view(request, pin_id):
    pin = get_object_or_404(Pin, id=pin_id)
    if request.method == "POST":
        comment_text = request.POST.get("comment")
        if comment_text:
            Comments.objects.create(
                user=request.user,
                pin=pin,
                text=comment_text
            )
        return redirect('specific', pin_id=pin.id)


def create_view(request):
    if request.method == "POST":
        title = request.POST.get("title")
        image_url = request.POST.get("image_url")
        category = request.POST.get("category")
        try:
            response = requests.head(
                image_url, allow_redirects=True, timeout=5)
            content_type = response.headers.get('Content-Type', '')
            if not content_type.startswith('image/'):
                messages.error(
                    request, "Invalid image URL. URL must point to an image.")
                return render(request, 'project/createPost.html', {
                    'title': title,
                    'image_url': image_url,
                    'category': category
                })
        except requests.RequestException:
            messages.error(request, "Image URL is not accessible.")
            return render(request, 'project/createPost.html', {
                'title': title,
                'image_url': image_url,
                'category': category
            })
        Pin.objects.create(
            title=title,
            image_url=image_url,
            category=category,
            uploaded_by=request.user
        )
        messages.success(request, "Pin created successfully!")
        return redirect('create-post')

    return render(request, 'project/createPost.html')


def download_pin(request):
    image_url = request.GET.get('url')
    if not image_url:
        return HttpResponse("No image URL provided", status=400)

    response = requests.get(image_url)
    if response.status_code != 200:
        return HttpResponse("Failed to fetch image", status=500)

    
    parsed_url = urlparse(image_url)
    filename = os.path.basename(parsed_url.path)

    download_response = HttpResponse(
        response.content, content_type=response.headers['Content-Type'])
    download_response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return download_response


@login_required
def follow_view(request):
    followed_users = Following.objects.filter(follower=request.user).values_list('following', flat=True)
    users = User.objects.exclude(id__in=followed_users).exclude(id=request.user.id)
    return render(request, 'project/follow.html', {"users": users})


@login_required
def follow_user(request, user_id):
    if request.method == "POST":
        to_follow = User.objects.get(id=user_id)
        if to_follow != request.user:
            Following.objects.get_or_create(follower=request.user, following=to_follow)
    return redirect('follow')
