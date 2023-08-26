from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views
from .views import ClientModelView

router = SimpleRouter()
router.register('api/client', ClientModelView)

urlpatterns = [
]

urlpatterns += router.urls
