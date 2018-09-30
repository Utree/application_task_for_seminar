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
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    token = serializers.CharField(required=True, allow_blank=False, max_length=50)

# イメージテーブルのシリアライザ
class ImageSerializer(serializers.Serializer):
    url = serializers.ImageField(required=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    
    # 新規作成
    def create(self, validated_data):
        return Image.objects.create(**validated_data)