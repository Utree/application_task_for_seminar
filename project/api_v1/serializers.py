from rest_framework import serializers
from api_v1.models import User, Token, Image
# ユーザーテーブルのシリアライザ
class UserSerializer(serializers.Serializer):
    # バリデーションをかける
    account_name = serializers.CharField(required=True, allow_blank=False, max_length=25)
    password = serializers.CharField(required=True, allow_blank=False, max_length=95)
    
    # 新規作成
    def create(self, validated_data):
        return User.objects.create(**validated_data)
        
# トークンテーブルのシリアライザ
class TokenSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    token = serializers.CharField(required=True, allow_blank=False, max_length=50)
    # 新規作成
    def create(self, validated_data):
        return Token.objects.create(**validated_data)
    
    # 更新
    def update(self, instance, validated_data):
        instance.user_id = validated_data.get("user_id", instance.user_id)
        instance.token = validated_data.get("token", instance.token)
        instance.save()
        return instance
    
    # 削除

# イメージテーブルのシリアライザ
class ImageSerializer(serializers.Serializer):
    url = serializers.ImageField(required=True)
    user_id = serializers.IntegerField(required=True)
    
    # 新規作成
    def create(self, validated_data):
        return Image.objects.create(**validated_data)