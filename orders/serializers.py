from games.serializers import GameSerializer
from shared.serializers import BaseSerializer
from users.serializers import UserSerializer

from .models import Order


class OrderSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'status': instance.get_status_display(),
            'key': instance.key if instance.status == Order.Status.PAID else None,
            'user': UserSerializer(instance.user).serialize(),
            'games': GameSerializer(instance.games.all(), request=self.request).serialize(),
            'created_at': instance.created_at,
            'updated_at': instance.updated_at,
            'price': instance.price,
        }
