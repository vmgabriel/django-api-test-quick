"""
View of Bills
"""

# Libraries
import csv
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings

# Models
from . import models

# Serializers
from . import serializers

# Utils
from .utils import create, get_data_value_bill_user

# Extended Libraries
from . import lib

# Tasks
from . import tasks


class ProductListView(APIView):
    """Views of Product"""
    permission_classes = (IsAuthenticated, )
    model = models.Product
    serializer = serializers.ProductSerializer

    def get(self, request):
        """Get All Data Client"""
        return Response(
            lib.get_all(self.model, self.serializer, request.GET),
            status=status.HTTP_200_OK
        )

    def post(self, request):
        """Save Product"""
        request_data = request.data
        new_product = self.serializer(data=request_data)
        saved_product = create(self.model, new_product)
        serializer = self.serializer(saved_product)
        print(f'saved_product - {saved_product}')
        if 'errors' in saved_product:
            return Response(
                new_product.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({
            'message': 'Done Correctly',
            'data': serializer.data,
        }, status=status.HTTP_201_CREATED)


class ProductDetailView(APIView):
    """Product Detail View Data Api"""
    permission_classes = (IsAuthenticated, )
    model = models.Product
    serializer = serializers.ProductSerializer

    def get(self, request, pk):
        """Get Detail of User"""
        product = lib.get_object(self.model, pk)
        serializer = self.serializer(product)
        return Response({
            'message': 'Done Correctly',
            'data': serializer.data
        })

    def put(self, request, pk):
        """Update all Data with pk"""
        response_update = lib.update_entity(
            self.model,
            self.serializer,
            request.data,
            pk
        )
        return response_update

    def patch(self, request, pk):
        """Update a or few Data with pk"""
        response_update = lib.update_entity(
            self.model,
            self.serializer,
            request.data,
            pk
        )
        return response_update

    def delete(self, request, pk):
        """Delete a data with pk"""
        return lib.delete_entity(self.model, self.serializer, pk)



class ClientListView(APIView):
    """Views of Client"""
    model = models.Client
    serializer = serializers.ClientSerializer

    def get(self, request):
        """Get All Data Client"""
        return Response(
            lib.get_all(self.model, self.serializer, request.GET),
            status=status.HTTP_200_OK
        )

    def post(self, request):
        """Save Client"""
        request_data = request.data
        new_user = self.serializer(data=request_data)
        if new_user.is_valid():
            request_data['id'] = new_user.create(request_data)
            return Response({
                'message': 'Done Correctly',
                'data': request_data,
            }, status=status.HTTP_201_CREATED)
        return Response(new_user.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientDetailView(APIView):
    """Product Detail View Data Api"""
    permission_classes = (IsAuthenticated, )
    model = models.Client
    serializer = serializers.ClientSerializer

    def get(self, request, pk):
        """Get Detail of User"""
        client = lib.get_object(self.model, pk)
        serializer = self.serializer(client)
        return Response({
            'message': 'Done Correctly',
            'data': serializer.data
        })

    def put(self, request, pk):
        """Update all Data with pk"""
        response_update = lib.update_entity(
            self.model,
            self.serializer,
            request.data,
            pk
        )
        return response_update

    def patch(self, request, pk):
        """Update a or few Data with pk"""
        response_update = lib.update_entity(
            self.model,
            self.serializer,
            request.data,
            pk
        )
        return response_update

    def delete(self, request, pk):
        """Delete a data with pk"""
        return lib.delete_entity(self.model, self.serializer, pk)



class BillListView(APIView):
    """Views of Bill"""
    permission_classes = (IsAuthenticated, )
    model = models.Bill
    serializer = serializers.BillSerializer

    def get(self, request):
        """Get All Data Client"""
        return Response(
            lib.get_all(self.model, self.serializer, request.GET),
            status=status.HTTP_200_OK
        )

    def post(self, request):
        """Save Bill"""
        request_data = request.data
        new_bill = self.serializer(data=request_data)
        saved_bill = create(self.model, new_bill)
        if 'errors' in saved_bill:
            return Response(saved_bill)
        return Response({
            'message': 'Done Correctly',
            'data': saved_bill,
        }, status=status.HTTP_201_CREATED)


class BillDetailView(APIView):
    """Bill Detail View Data Api"""
    permission_classes = (IsAuthenticated, )
    model = models.Bill
    serializer = serializers.BillSerializer

    def get(self, request, pk):
        """Get Detail of User"""
        bill = lib.get_object(self.model, pk)
        serializer = self.serializer(bill)
        return Response({
            'message': 'Done Correctly',
            'data': serializer.data
        })

    def put(self, request, pk):
        """Update all Data with pk"""
        response_update = lib.update_entity(
            self.model,
            self.serializer,
            request.data,
            pk
        )
        return response_update

    def patch(self, request, pk):
        """Update a or few Data with pk"""
        response_update = lib.update_entity(
            self.model,
            self.serializer,
            request.data,
            pk
        )
        return response_update

    def delete(self, request, pk):
        """Delete a data with pk"""
        return lib.delete_entity(self.model, self.serializer, pk)


class FileCSVHandlerGetView(APIView):
    """File Csv Handler Configuration"""
    permission_classes = (IsAuthenticated, )
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, pk: any):
        """Get File Sync CSV"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'
        column_format, data = get_data_value_bill_user(pk)
        print('column format - ', column_format)
        print('data - ', data)
        writer = csv.DictWriter(response, fieldnames=column_format)
        writer.writeheader()
        for register in data:
            writer.writerow(register)
        return response


class FileCSVHandlerPostView(APIView):
    """Get Handler Data"""

    def post(self, request, *args, **kwargs):
        """Post COnfiguration for File Serializer"""
        file_serializer = serializers.FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            # Creating Task
            # tasks.create_massive.delay(file_serializer.data.get('file_data'))
            serializer = serializers.ClientSerializer
            with open(f"{settings.BASE_DIR}{file_serializer.data.get('file_data')}", 'r') as f:
                reader = csv.reader(f)
                is_first = True
                columns = []
                for row in reader:
                    if is_first:
                        columns = row
                        is_first = False
                    else:
                        data = dict(zip(columns, row))
                        tasks.create_one_data_later.delay(data)
            return Response(
                file_serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            file_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
