from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .serializers import UserProfileSerializer, UserProfileAvatarSerializer


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
    return render(request, "index.html", {'site_url': settings.SITE_URL, 'media_url': settings.MEDIA_URL})


class UserProfileViewset(ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    @action(detail=False, methods=['GET'])
    def get_available_users(self, request, *args, **kwargs):
        queryset = self.queryset.exclude(id=request.user.id)
        full_name = self.request.query_params.get('full_name', None)
        if full_name:
            queryset = queryset.filter(Q(username__icontains=full_name)
                                       | Q(first_name__icontains=full_name)
                                       | Q(last_name__icontains=full_name))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
