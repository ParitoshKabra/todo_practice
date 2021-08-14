from django.contrib import admin
from django.urls import path, include
from Todo_Application import views



urlpatterns = [
    path('',views.index, name='index'),    
    path('add_item/<int:list_id>/',views.add_item, name='add_item'),    
    path('update/<int:list_id>/',views.update, name='update'),    
    path('delete/<int:list_id>/',views.delete, name='delete'),
    path('delitem/<int:id>', views.delete_item, name='delitem'),    
    path('create/',views.create, name='create')    
]