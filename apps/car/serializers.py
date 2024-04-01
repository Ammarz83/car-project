from rest_framework import serializers


from .models import (
    Brand,
    Car,
    )

from apps.review.serializers import CommentSerializer
class BrandCreateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # 1

    class Meta:
        model = Brand
        exclude = ('slug',)

    def validate(self, attrs):
        brand = attrs.get('name')
        if Brand.objects.filter(name=Brand).exists():
            raise serializers.ValidationError(
                'This Brand already exists'
            )
        user = self.context['request'].user                   # 1
        attrs['user'] = user
        return attrs
    

class BrandListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand 
        fields = ['brand', 'model', 'slug', 'user']  # 2


class BrandRetrieveSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # 3

    class Meta:
        model = Brand
        fields = '__all__'

    def validate(self, attrs):                               # 3
        user = self.context['request'].user
        attrs['user'] = user
        return attrs


class CarCreateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username') # 4
    
    class Meta:
        model = Car
        exclude = ('slug',)

    def validate(self, attrs: dict):
        book = attrs.get('title')
        if Car.objects.filter(name=Car).exists():
            raise serializers.ValidationError(
                'This Car already exists'
            )
        user = self.context['request'].user                 # 4
        attrs['user'] = user
        return attrs
    

class CarListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car  
        fields = ['slug', 'user']       # 5
        

class CarUpdateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # 6

    class Meta:
        model = Car                                          # 6
        fields = ['model', 'brand', 'image', 'year', 'slug','user'] 
    
    def validate(self, attrs):                                 # 6
        user = self.context['request'].user
        attrs['user'] = user
        return attrs


class CarRetrieveSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  

    class Meta:
        model = Car
        fields = '__all__'

    def validate(self, attrs):                                 
        user = self.context['request'].user
        attrs['user'] = user
        return attrs
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep['comments'] = CommentSerializer(
        instance.books_comments.all(), many=True
        ).data

    #     rating = instance.books_ratings.aggregate(Avg('rating'))['rating__avg']   
    #     if rating:
    #         rep['rating'] = round(rating, 1) 
    #     else:
    #         rep['rating'] = 0.0
        
    #     rep['likes'] = instance.books_likes.all().count()
    #     rep['liked_by'] = LikeSerializer(
    #         instance.books_likes.all().only('user'), many=True).data 

        return rep


