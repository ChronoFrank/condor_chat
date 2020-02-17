from django.urls import path, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from chat.views import LoginLanding, condor_chat_logout, index, update_avatar
from rest_framework.routers import SimpleRouter
from chat.views import UserProfileViewset
from rest_framework_simplejwt import views as jwt_views


router = SimpleRouter()

router.register(r'profiles', UserProfileViewset)

urlpatterns = [
    path('', index, name='index'),
    path('update_avatar/', update_avatar, name='update_avatar'),
    path('accounts/login/', LoginLanding.as_view(), name="login"),
    path('accounts/logout/', condor_chat_logout, name="logout"),
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/access_token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/refresh_token/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
