from django.urls import include, path
from adminweb import views

urlpatterns = [
    path('', views.index, name ='index'), 
    path('menu/', views.MenuItemView.as_view(), name ='menu'), 
    path('menu/<int:pk>/', views.MenuItemDetailView.as_view(), name ='menu-detail'), 
    path('category/', views.CategoryView.as_view(), name ='category'), 
    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name ='category-detail'), 
    path('employee/', views.EmployeeView.as_view(), name='employee'),
    path('employee/<int:pk>/', views.EmployeeDetailView.as_view(), name='employee-detail'),
]
