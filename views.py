from django.views.generic.simple import direct_to_template
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

def profile(request, **kwargs):
    if kwargs.has_key('username'):
        user = get_object_or_404(User, username__exact=kwargs['username'])
    else:
        user = request.user
    return direct_to_template(request, template="profile.html", extra_context={"userprofile":user})

def new_user(request):
    
    pass
    #stub
