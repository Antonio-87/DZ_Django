from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from advertisements.models import Advertisement, Favourite


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""

        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        user = self.context['request'].user
        adv_count = Advertisement.objects.select_related('creator').filter(creator=user, status='OPEN').count()
        if adv_count > 10 and data.get('status', 'OPEN') == 'OPEN':
            raise ValidationError('Колличество открытых объявлений превышено')
        return data


class FavouriteSerializer(serializers.ModelSerializer):
    """Serializer для избранного."""
    
    advertisement = AdvertisementSerializer()
    class Meta:
        model = Favourite
        fields = ['user', 'advertisement']