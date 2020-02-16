from django.urls import path
from django.contrib import admin
from chat.views import LoginLanding, condor_chat_logout, index

urlpatterns = [
    path('', index),
    path('accounts/login/', LoginLanding.as_view(), name="login"),
    path('accounts/logout/', condor_chat_logout, name="logout"),
    path('admin/', admin.site.urls),
]