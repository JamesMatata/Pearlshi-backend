from django.contrib import admin
from django.urls import path, include

admin.site.site_title = 'Admin | Pearlshi Caterers ans Event Planners'
admin.site.site_header = 'Admin | Pearlshi Caterers ans Event Planners'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls', namespace='core')),
]
