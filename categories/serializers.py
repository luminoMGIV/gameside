from shared.serializers import BaseSerializer


class CategorySerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:
        return {
            'name': instance.name,
            'id': instance.pk,
            'slug': instance.slug,
            'description': instance.description,
            'color': instance.color,
        }
