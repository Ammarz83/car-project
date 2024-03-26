from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import (
    CarComment,
    CarRating,
    CarLike,
    SavedCar,
)


User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        default=serializers.CurrentUserDefault(),
        source='user.username'
    )

    class Meta:
        model = CarComment
        exclude = ['id']


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = CarLike
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        car = self.context.get('car')
        like = CarLike.objects.filter(user=user, car=car).first()
        if like:
            raise serializers.ValidationError('already liked')
        return super().create(validated_data)

    def unlike(self):
        user = self.context.get('request').user
        car = self.context.get('car')
        like = CarLike.objects.filter(user=user, car=car).first()
        if like:
            like.delete()
        else:
            raise serializers.ValidationError('not liked yet')


class RatingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = CarRating
        fields = ('rating', 'user', 'car')

    def validate(self, attrs):
        user = self.context.get('request').user
        attrs['user'] = user
        rating = attrs.get('rating') 
        if rating not in (1, 2, 3, 4, 5):
            raise serializers.ValidationError('Incorrect value. The rating should be between 1 and 5.')
        # if rating:
        #     raise serializers.ValidationError('already exists')
        return attrs

    def update(self, instance, validated_data):
        instance.rating = validated_data.get('rating')
        instance.save()
        return super().update(instance, validated_data)


class SavedCarSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = SavedCar
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        request = self.context.get('request').data
        car = request.get('car')
        favorite = SavedCar.objects.filter(user=user, car=car).first()
        if not favorite:
            return super().create(validated_data)
        raise serializers.ValidationError('This car has been saved')

    def del_favorite(self, validated_data):
        user = self.context.get('request').user
        request = self.context.get('request').data
        car = request.get('car').slug
        favorite = SavedCar.objects.filter(user=user, car=car).first()
        if favorite:
            favorite.delete()
        else:
            raise serializers.ValidationError('This car has not been saved')