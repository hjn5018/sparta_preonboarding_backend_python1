from typing import Any, Dict, List
from rest_framework import serializers

from .models import User, UserRole

class SignupResponseSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'nickname', 'roles']
    
    def get_roles(self, obj: Any) -> List[Dict[str, str]]:
        roles = UserRole.objects.filter(user=obj)
        return [{'role': role.role.role} for role in roles]
    
class SignupRequestSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'nickname']