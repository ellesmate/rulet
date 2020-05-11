from rest_framework import viewsets, permissions, views
from rest_framework.response import Response
from . import serializers, models

# from .models import Waiter, Cashier, Chef, Order, Customer, MenuItem, Entity, Category


class EntityViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = models.Entity.objects.all()
    serializer_class = serializers.EntitySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    # queryset = Category.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.CategorySerializer

    def get_queryset(self):
        # fnd_pk = self.request.fnd_pk
        entity_pk = self.kwargs['entity_pk']
        # print(a)
        return models.Category.objects.filter(entity__pk=entity_pk)
    
    # def list(self, request, fnd_pk):
    #     qt = Category.objects.all()
    #     serializer = self.get_serializer(qt, many=True)
    #     return Response(serializer.data)



class WaiterViewSet(viewsets.ModelViewSet):
    queryset = models.Waiter.objects.all()
    serializer_class = serializers.WaiterSerializer


class CashierViewSet(viewsets.ModelViewSet):
    queryset = models.Cashier.objects.all()
    serializer_class = serializers.CashierSerializer


class ChefViewSet(viewsets.ModelViewSet):
    queryset = models.Chef.objects.all()
    serializer_class = serializers.ChefSerializer


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = models.Order.objects.all()
    # serializer_class = serializers.OrderSerializer

    def create(self, request, *args, **kwargs):
        # print(dir(request))
        # print(request.user)
        # print(dir(request.user))
        request.data['customer'] = request.user
        request.data['entity'] = kwargs['entity_pk']
        
        return super().create(request, *args, **kwargs)


    def get_serializer_class(self):
        if self.request.method == "POST":
            return serializers.CreateOrderSerializer
        return serializers.OrderSerializer
    
    def get_queryset(self):
        entity_pk = self.kwargs['entity_pk']
        
        status = self.request.query_params.get('status')
        # if (status == 'active'):
        #     return models.Order.objects.filter(entity__pk=entity_pk, status="DONE")

        return models.Order.objects.filter(entity__pk=entity_pk)


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = models.Customer.objects.all()
    serializer_class = serializers.CustomerSerializer


class MenuItemViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.MenuItemSerializer

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
        entity_pk = self.kwargs['entity_pk']
        return models.MenuItem.objects.filter(entity__pk=entity_pk)
