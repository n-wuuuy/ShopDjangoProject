from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views
from .views import ClientModelView, RedirectSocial

router = SimpleRouter()
router.register('api/client', ClientModelView)

urlpatterns = [
    path('account/profile/', RedirectSocial.as_view()),

]

urlpatterns += router.urls
