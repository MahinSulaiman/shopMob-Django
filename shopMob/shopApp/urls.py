from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('mobiles/',views.MobView.as_view()),
    path('mobiles/<int:id>/',views.MobView.as_view()),
    path('users/registration/',views.UserManagement.as_view()),
    path('users/login/',views.UserLogin.as_view()),
    path('users/logout/',views.UserLogout.as_view())
]


#to view images
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)