from rest_framework.serializers import ModelSerializer

from users_app.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'last_login', 'is_superuser', 'username', 'email',
            'date_joined', 'is_active', 'is_staff', 'is_verified', 'id')
