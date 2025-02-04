from categories.serializers import CategorySerializer
from platforms.serializers import PlatformSerializer
from shared.serializers import BaseSerializer
from users.serializers import UserSerializer


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
            'price': float(instance.price),
            'stock': instance.stock,
            'released_at': instance.released_at.isoformat(),
            'pegi': instance.get_pegi_display(),
            'category': BaseSerializer.to_json(CategorySerializer(instance.category)),
            'platforms': BaseSerializer.to_json(PlatformSerializer(instance.platforms.all())),
        }


class ReviewSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'rating': instance.rating,
            'comment': instance.comment,
            'game': BaseSerializer.to_json(GameSerializer(instance.game)),
            'author': BaseSerializer.to_json(UserSerializer(instance.author)),
            'created_at': instance.created_at,
            'updated_at': instance.updated_at,
        }
