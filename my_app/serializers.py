from datetime import datetime

from rest_framework import serializers
from .models import ChargePoint


class ChargePointSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargePoint
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name': instance.name,
            'status': instance.get_status_display(),
            'created_at': instance.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'deleted_at': instance.deleted_at.strftime("%Y-%m-%d %H:%M:%S") if instance.deleted_at else None
        }
