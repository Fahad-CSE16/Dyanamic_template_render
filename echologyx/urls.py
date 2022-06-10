from django.contrib import admin
from django.urls import path, include
from echologyx.settings import DEBUG
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from django.urls.conf import re_path

from rest_framework.authtoken import views
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Echologyx API",
      default_version='v1.0',
      description="Api description",
      contact=openapi.Contact(email="mdfahadhossain71@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=False,
   permission_classes=(permissions.IsAuthenticated,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    #  API for Getting Token for Authentication
    path('token-login/', views.obtain_auth_token),

    # Api for JWT Token Authentication
    path('token/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include('userapp.urls')),
    path('blogpost/', include('blogpost.urls')),
    path('api/blogpost/', include('blogpost.api.urls')),
    path('html_management/', include('html_management.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if DEBUG:
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]
    urlpatterns += [
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]