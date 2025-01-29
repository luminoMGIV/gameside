# from users.serializers import UserSerializer
from shared.serializers import BaseSerializer


class GameSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'title': instance.title,
            'slug': instance.slug,
            'description': instance.description,
            'cover': self.build_url(instance.cover.url),
            'price': instance.price,
            'stock': instance.stock,
            'released_at': instance.released_at,
            'pegi': instance.get_pegi_display(),
            # 'category': CategorySerializer(instance.category),
            # 'platforms': PlatformSerializer(instance.platforms),
        }


class ReviewSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'rating': instance.rating,
            'comment': instance.comment,
            # 'game': GameSerializer(instance.game),
            # 'user': UserSerializer(instance.user),
            'created_at': instance.created_at,
            'updated_at': instance.updated_at,
        }
