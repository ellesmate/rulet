from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Waiter, Cashier, Chef, Order, Customer, MenuItem, Foundation, Category
from .serializers import WaiterSerializer, CashierSerializer, ChefSerializer, OrderSerializer, \
    CustomerSerializer, MenuItemSerializer, FoundationSerializer, CategorySerializer


class FoundationViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Foundation.objects.all()
    serializer_class = FoundationSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    # queryset = Category.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CategorySerializer

    def get_queryset(self):
        # fnd_pk = self.request.fnd_pk
        foundation_pk = self.kwargs['foundation_pk']
        # print(a)
        return Category.objects.filter(foundation__pk=foundation_pk)
    
    # def list(self, request, fnd_pk):
    #     qt = Category.objects.all()
    #     serializer = self.get_serializer(qt, many=True)
    #     return Response(serializer.data)



class WaiterViewSet(viewsets.ModelViewSet):
    queryset = Waiter.objects.all()
    serializer_class = WaiterSerializer


class CashierViewSet(viewsets.ModelViewSet):
    queryset = Cashier.objects.all()
    serializer_class = CashierSerializer


class ChefViewSet(viewsets.ModelViewSet):
    queryset = Chef.objects.all()
    serializer_class = ChefSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class MenuItemViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    # queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def list(self, request, *args, **kwargs):
        category = request.query_params.get('category')

        queryset = self.get_queryset()
        if category:
            queryset = queryset.filter(category__pk=category)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serialzier = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    def get_queryset(self):
        foundation_pk = self.kwargs['foundation_pk']
        return MenuItem.objects.filter(foundation__pk=foundation_pk)

