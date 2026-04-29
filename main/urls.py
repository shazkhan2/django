from django.contrib import admin
from django.urls import path, include
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('tours/', include('tours.urls')),
    path('', user_views.register_user, name='index'),
]
