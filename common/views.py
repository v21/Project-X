from django.contrib.auth.views import redirect_to_login
from django.template import RequestContext, loader
from django.http import Http404, HttpResponse, HttpResponseRedirect


def access_control(request, owner, callback):
    '''
    This factors out the "is this user allowed to look at this object" code. 
    It would be much neater as a decorator, but sadly we need to pick the object first.
    To use it: use functools.partial, to freeze the view you want called if the user 
    does have permission (like so:  access_control(request, owner, partial(func, arg1, arg2, argn)) )
    Lazy evaluation ftw!
    '''
    if request.user.is_authenticated():
        if request.user.is_active:
            if owner == request.user:
                return callback()
            else:
                raise Http404 #replace with "not authed" page
        else:
            raise Http404 #replace with "not authed" page?
    else:
        return redirect_to_login(request.path)
