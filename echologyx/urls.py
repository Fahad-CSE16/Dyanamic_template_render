from django.contrib import admin
from django.urls import path, include
from echologyx.settings import DEBUG
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('userapp.urls')),
    path('blogpost/', include('blogpost.urls')),
    path('html_management/', include('html_management.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if DEBUG:
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]
