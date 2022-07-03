from django.shortcuts import render
from django.contrib.auth.models import User

def users(request):
    users = User.objects.all()
    username = request.GET.get('search')
    if username:
        users = User.objects.filter(username__icontains=username)
    context = {
        'users': users,
    }
    return render(request, "userapp/users.html", context)
