from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    SavedCarViewSet,
    CarCommentView,
    RatingView,
    LikeView,
)


router = DefaultRouter()


router.register('saved car',SavedCarViewSet, 'saved car' )
router.register ('car-comment', CarCommentView, 'comment')
router.register( 'car-rating', RatingView, 'rating')
router.register( 'car-like', LikeView, 'like')



urlpatterns = [

]
urlpatterns += router.urls

