from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from account.views import UserProfileApi, RegisterApiView, LoginView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf import settings

schema_view = get_schema_view(
    openapi.Info(
        title="Referral project",
        default_version='v1',),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account.urls')),
    path('api/users/', UserProfileApi.as_view({'get': 'list'}), name='users'),
    path('api/register/', RegisterApiView.as_view(), name='user-registration'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0),name='schema-swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)