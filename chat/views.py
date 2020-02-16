from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt



class LoginLanding(View):
    """ Login View"""
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        next = request.GET.get('next', '/')
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form, 'next': next})

    def post(self, request, *args, **kwargs):
        next = request.POST.get('next', '/')
        form = AuthenticationForm(None, request.POST)
        if form.is_valid():
            username = request.POST.get('username', False)
            password = request.POST.get('password', False)
            if username and password:
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('/')
                else:
                    messages.warning(request,
                                     'You do not have permission to login out of the intranet. '
                                     'Contact the administrator for any problem.')
        else:
            return render(request, 'login.html', {'form': form, 'next': next})

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginLanding, self).dispatch(request, args, kwargs)


def condor_chat_logout(request):
    logout(request)
    return redirect(reverse('login'))


@login_required
def index(request):
    return render(request, "index.html")