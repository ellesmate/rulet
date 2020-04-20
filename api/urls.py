from django.urls import path, include
from rest_framework import routers

from . import views


# router = routers.DefaultRouter()
# router.register(r'foundations', views.FoundationViewSet)
# router.register(r'chefs', views.ChefViewSet)
# router.register(r'cashiers', views.CashierViewSet)
# router.register(r'customers', views.CustomerViewSet)
# router.register(r'orders', views.OrderViewSet)
# router.register(r'menuitems', views.MenuItemViewSet)
# router.register(r'waiters', views.WaiterViewSet)
# router.register(r'category', views.CategoryViewSet)

foundation_list = views.FoundationViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

foundation_detail = views.FoundationViewSet.as_view({
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
    path('foundations/', foundation_list, name='foundation-list'),
    path('foundations/<int:pk>/', foundation_detail, name='foundation-detail'),
    path('foundations/<int:foundation_pk>/categories/', category_list, name='category-list'),
    path('foundations/<int:foundation_pk>/menuitems/', menuitem_list, name='menuitem-list'),
    path('foundations/<int:foundation_pk>/menuitems/<int:pk>/', menuitem_detail, name='menuitem-detail'),
    path('foundations/<int:foundation_pk>/orders/', order_list, name='order-list'),
    path('foundations/<int:foundation_pk>/orders/<int:pk>/', order_detail, name='order-detail'),
]
