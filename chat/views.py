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
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import parsers
from .serializers import UserProfileSerializer, UserProfileAvatarSerializer
from .serializers import MessageSerializer, RoomSerializer
from .forms import UserProfileForm
from .models import Message, Room


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


@login_required
def update_avatar(request):
    user_profile = request.user.userprofile
    if request.method == "POST":
        print(request.POST)
        update_profile_form = UserProfileForm(data=request.POST, instance=user_profile)
        if update_profile_form.is_valid():
            if 'avatar' in request.FILES:
                user_profile.avatar = request.FILES['avatar']
                user_profile.save()

    else:
        update_profile_form = UserProfileForm(instance=user_profile)

    return render(request, 'update_avatar.html',
                  {'update_profile_form': update_profile_form,
                   'site_url': settings.SITE_URL, 'media_url': settings.MEDIA_URL})


class UserProfileViewset(ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, ]

    @action(detail=False, methods=['GET'])
    def get_available_users(self, request, *args, **kwargs):
        queryset = self.queryset.exclude(id=request.user.id)
        full_name = self.request.query_params.get('full_name', None)
        email = self.request.query_params.get('email', None)
        if full_name:
            queryset = queryset.filter(Q(username__icontains=full_name)
                                       | Q(first_name__icontains=full_name)
                                       | Q(last_name__icontains=full_name))

        if email:
            queryset = queryset.filter(email__icontains=email)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['PUT'], serializer_class=UserProfileAvatarSerializer,
            parser_classes=[parsers.MultiPartParser])
    def pic(self, request, pk):
        obj = self.get_object()

        serializer = self.serializer_class(obj.userprofile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class MessageViewSet(ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    permission_classes = [IsAuthenticated, ]


class RoomViewSet(ModelViewSet):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()
    permission_classes = [IsAuthenticated, ]


class SendMessageToUserView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        sender = request.user
        user_id = request.data.get('user_id')
        message = request.data.get('message')
        if not user_id or not message:
            return Response({'error': "invalid payload to send messages"}, status=status.HTTP_400_BAD_REQUEST)

        if int(user_id) == sender.id:
            return Response({'error': "the sender and the receiver "
                                      "can not be the same for new messages"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=int(user_id))
        except User.DoesNotExist:
            return Response({'error': "invalid user to chat with"}, status=status.HTTP_400_BAD_REQUEST)

        rooms = Room.objects.filter(participants__in=[sender.id, user.id], is_goup=False).distinct()
        msg = Message.objects.create(sender=sender, content=message)
        for room in rooms:
            ids = list(room.participants.values_list('id', flat=True))
            if sender.id in ids and user.id in ids:
                # create new message for the existing 2 people room
                room.messages.add(msg)
                serializer = RoomSerializer(instance=room)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        # create new room to send message
        room_name = u'{0} - {1}'.format(sender.username, user.username)
        room = Room.objects.create(title=room_name)
        room.participants.add(sender)
        room.participants.add(user)
        room.messages.add(msg)
        serializer = RoomSerializer(instance=room)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SendMessageToRoomView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        sender = request.user
        group_id = request.data.get('group_id')
        message = request.data.get('message')
        if not group_id or not message:
            return Response({'error': "invalid payload to send messages"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            room = Room.objects.get(id=int(group_id), participants__in=[sender.id], is_goup=True)
        except Room.DoesNotExist:
            return Response({'error': "the room you are trying to "
                                      "reaching does not exists or you are not "
                                      " part of it"}, status=status.HTTP_400_BAD_REQUEST)

        msg = Message.objects.create(sender=sender, content=message)
        room.messages.add(msg)
        serializer = RoomSerializer(instance=room)
        return Response(serializer.data, status=status.HTTP_201_CREATED)