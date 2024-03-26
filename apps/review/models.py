from django.db import models
from django.contrib.auth import get_user_model
# from django.urls import reverse


from apps. car. models import Car


User = get_user_model()


class CarComment (models.Model):
    user = models. ForeignKey (
        to=User,
        on_delete=models. CASCADE,
        related_name='comments'
    )
    car = models. ForeignKey(
        to=Car,
        on_delete=models.CASCADE,
        related_name= 'cars_comments'
    )
    comment_text = models. TextField ()
    created_at = models. DateTimeField (auto_now_add=True)
    
    def str(self) :
        return f'Comment from {self.user.username} to {self.car.title}'
    

class CarRating (models.Model) :
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE =5
    RATING_CHOICES = (
        (ONE,'1'),
        (TWO, '2'),
        (THREE, '3'),
        (FOUR,'4'),
        (FIVE, '5')
    )

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE, 
        related_name='ratings'
    )
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, blank=True, null=True)
    car = models. ForeignKey (
        to=Car, 
        on_delete=models.CASCADE, 
        related_name= 'cars_ratings'
    )

    def _str_ (self) -> str:
        return f'{self.rating} points to {self.car.title}'
    
    class Meta:
        unique_together = ['user', 'car', 'rating']

    
class CarLike(models.Model):
    user = models.ForeignKey(
        to=User, 
        on_delete=models.CASCADE, 
        related_name= 'likes'
    )
    car = models.ForeignKey(
    to=Car, 
    on_delete=models.CASCADE, 
    related_name= 'cars_likes'
    )

    def _str__(self) :
        return f'Liked by {self.user. username}'
    

class SavedCar(models.Model):
    user = models.ForeignKey(
        to=User, 
        on_delete=models.CASCADE,
    )
    car = models. ForeignKey (
    to=Car, 
    on_delete=models. CASCADE,
    )
