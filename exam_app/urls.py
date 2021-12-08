from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('add_group', views.add_group),
    path('<int:group_id>', views.group_details),
    path('leave_group/<int:group_id>', views.leave),
    path('join_group/<int:group_id>', views.join),
    path('remove/<int:group_id>', views.remove)
]