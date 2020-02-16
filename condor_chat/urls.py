from django.urls import path, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from chat.views import LoginLanding, condor_chat_logout, index
from rest_framework.routers import SimpleRouter
from chat.views import UserProfileViewset


router = SimpleRouter()

router.register(r'profiles', UserProfileViewset)

urlpatterns = [
    path('', index),
    path('accounts/login/', LoginLanding.as_view(), name="login"),
    path('accounts/logout/', condor_chat_logout, name="logout"),
    path('admin/', admin.site.urls),
    path(r'api/v1/', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
