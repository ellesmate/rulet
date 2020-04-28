from django.urls import path, include
from rest_framework import routers

from . import views


# router = routers.DefaultRouter()
# router.register(r'entitys', views.EntityViewSet)
# router.register(r'chefs', views.ChefViewSet)
# router.register(r'cashiers', views.CashierViewSet)
# router.register(r'customers', views.CustomerViewSet)
# router.register(r'orders', views.OrderViewSet)
# router.register(r'menuitems', views.MenuItemViewSet)
# router.register(r'waiters', views.WaiterViewSet)
# router.register(r'category', views.CategoryViewSet)

entity_list = views.EntityViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

entity_detail = views.EntityViewSet.as_view({
    'get': 'retrieve',
})

category_list = views.CategoryViewSet.as_view({
    'get': 'list',
})

menuitem_list = views.MenuItemViewSet.as_view({
    'get': 'list',
})

menuitem_detail = views.MenuItemViewSet.as_view({
    'get': 'retrieve',
})

order_list = views.OrderViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

order_detail = views.OrderViewSet.as_view({
    'get': 'retrieve',
})



urlpatterns = [
    # path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('entity/', entity_list, name='entity-list'),
    path('entity/<int:pk>/', entity_detail, name='entity-detail'),
    path('entity/<int:entity_pk>/categories/', category_list, name='category-list'),
    path('entity/<int:entity_pk>/menuitems/', menuitem_list, name='menuitem-list'),
    path('entity/<int:entity_pk>/menuitems/<int:pk>/', menuitem_detail, name='menuitem-detail'),
    path('entity/<int:entity_pk>/orders/', order_list, name='order-list'),
    path('entity/<int:entity_pk>/orders/<int:pk>/', order_detail, name='order-detail'),
]
