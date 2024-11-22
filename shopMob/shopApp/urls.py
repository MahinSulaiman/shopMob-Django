from django.urls import path
from . import views

urlpatterns=[
    path('mobiles/',views.MobView.as_view()),
    path('mobiles/<int:id>/',views.MobView.as_view()),
    path('users/registration/',views.UserManagement.as_view()),
    path('users/login/',views.UserLogin.as_view()),
    path('users/logout/',views.UserLogout.as_view())
]