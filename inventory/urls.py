from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path(
        'medicines/',
        views.medicine_list,
        name='medicine_list'
    ),

    path(
        'add/',
        views.add_medicine,
        name='add_medicine'
    ),

    path(
        'edit/<int:id>/',
        views.edit_medicine,
        name='edit_medicine'
    ),

    path(
        'delete/<int:id>/',
        views.delete_medicine,
        name='delete_medicine'
    ),
]