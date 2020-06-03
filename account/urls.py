from django.urls import include, path, re_path
from rest_framework import routers
from account import views
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register(r'users', views.AccountViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # path('', include(router.urls)),
    path('me/', views.me_view),
    # re_path(r'^signup/$', views.signup, name='signup'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('', views.index, name ='index'), 
    path('menu/', views.MenuItemView.as_view(), name ='menu'), 
    path('menu/<int:pk>/', views.MenuItemDetailView.as_view(), name ='menu-detail'), 
    path('category/', views.CategoryView.as_view(), name ='category'), 
    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name ='category-detail'), 
    path('employee/', views.EmployeeView.as_view(), name='employee'),
    path('employee/<int:pk>/', views.EmployeeDetailView.as_view(), name='employee-detail'),
]
