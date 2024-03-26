from rest_framework.routers import DefaultRouter
from .views import (
    BrandViewSet,
    CarViewSet
)

router = DefaultRouter()
router.register('brand', BrandViewSet)  # , base
router.register('car', CarViewSet)


urlpatterns = [

]

urlpatterns +=  router.urls