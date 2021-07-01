from django.shortcuts import render
from .models import UserProfile
# Create your views here.
def register(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
    
    if request.POST:
        username = request.POST.get('username')

        if username == '' or username is None:
            context['error'] = "Name can't be empty"
        else:
            qs = UserProfile.objects.filter(name = username)
            if qs:
                context['error'] = "User already exists"
            else:
                qs = UserProfile.objects.create(name = username) 
                qs.save()
                context['success'] = "User " + username + " Created"

    # add the dictionary during initialization
         
    return render(request, "register.html", context)