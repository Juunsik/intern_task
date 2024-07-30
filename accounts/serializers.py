from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "nickname",
        )

    def validate(self, attrs):
        username = attrs.get("username")
        nickname = attrs.get("nickname")

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {"username": "이미 존재하는 username입니다."}
            )
        if User.objects.filter(nickname=nickname).exists():
            raise serializers.ValidationError(
                {"nickname": "이미 존재하는 nickname입니다."}
            )

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["roles"] = [{"role": instance.role}]
        return representation
