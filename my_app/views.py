import datetime

from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from .models import ChargePoint
from .serializers import ChargePointSerializer

# Create your views here.


@api_view(['GET', 'POST'])
def list_or_create_charge_point(request):

    if request.method == 'GET':  # List charge points
        charge_points = ChargePoint.objects.all()
        charge_points_serializer = ChargePointSerializer(charge_points, many=True)
        return Response(charge_points_serializer.data)

    if request.method == 'POST':  # Create charge point
        charge_point_serializer = ChargePointSerializer(data=request.data)
        if charge_point_serializer.is_valid():
            charge_point_serializer.save()
            return Response({'message': 'Charge point created', 'data': charge_point_serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response(charge_point_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def get_update_or_delete_charge_point(request, pk):
    charge_point = get_object_or_404(ChargePoint, pk=pk, deleted_at=None)

    if request.method == 'GET':  # Get charge point
        charge_point_serializer = ChargePointSerializer(charge_point)
        return Response(charge_point_serializer.data)

    if request.method == 'PUT':  # Update charge point
        charge_point_serializer = ChargePointSerializer(charge_point, data=request.data, partial=True)
        if charge_point_serializer.is_valid():
            charge_point_serializer.save()
            return Response({'message': 'Charge point updated', 'data': charge_point_serializer.data})
        return Response(charge_point_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':  # Delete charge point
        charge_point_serializer = ChargePointSerializer(charge_point,
                                                        data={'deleted_at': datetime.datetime.now()},
                                                        partial=True)
        if charge_point_serializer.is_valid():
            charge_point_serializer.save()
            return Response({'message': 'Charge point deleted', 'data': charge_point_serializer.data})
        return Response(charge_point_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
