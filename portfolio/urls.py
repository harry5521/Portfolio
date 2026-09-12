from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render


# Custom error page handlers
def custom_404(request, exception):
    return render(request, '404.html', status=404)

def custom_500(request):
    return render(request, '500.html', status=500)


urlpatterns = [
    path('admin/portfolio-admin-047/', admin.site.urls),
    path('', include('landing.urls')),
    
    # Error handlers
    path('404/', custom_404, name='error_404'),
    path('500/', custom_500, name='error_500'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    pass