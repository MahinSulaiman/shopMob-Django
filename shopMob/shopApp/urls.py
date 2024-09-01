from django.urls import path
from . import views

urlpatterns=[
    path('mobiles/',views.MobView.as_view()),
    path('mobiles/<int:id>/',views.MobView.as_view()),
]