from rest_framework import serializers

from .models import User, UserRole

class UserSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'nickname', 'roles']
    
    def get_roles(self, obj):
        roles = UserRole.objects.filter(user=obj)
        return [{'role': role.role.role} for role in roles]