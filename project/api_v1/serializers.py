# serializers.pyはpythonのモデルとveiws.pyとのクッション的役割
# DB(sqlite)を操作、パース等をする
from rest_framework import serializers
from api_v1.models import User, Token, Image

# ハッシュ化用
from django.utils import timezone
import hashlib

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
    # バリデーションをかける
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    token = serializers.CharField(required=True, allow_blank=False, max_length=50)
    
    # トークン付与
    @staticmethod # インスタンス変数、インスタンスメソッドにアクセスしない時(selfを使わない時につけるデコレータ)
    def create(user):
        # ユーザーの既存のトークンを取得
        if Token.objects.filter(user_id=user.id).count():
            Token.objects.filter(user_id=user.id).delete()
        
        # トークン生成
        dt = timezone.now()
        str = user.account_name + user.password + dt.strftime('%Y%m%d%H%M%S%f')
        hash = hashlib.sha1(str.encode('utf-8')).hexdigest()
        
        # トークンをデータベースに追加
        token = Token.objects.create(
            user_id = user,
            token = hash
        )
        return hash
    
    # トークン認証
    @staticmethod # インスタンス変数、インスタンスメソッドにアクセスしない時(selfを使わない時につけるデコレータ)
    def auth(token_key):
        if Token.objects.filter(token=token_key).count():
            return Token.objects.filter(token=token_key).first().user_id
        else:
            return None

# イメージテーブルのシリアライザ
class ImageSerializer(serializers.Serializer):
    # バリデーションをかける
    url = serializers.ImageField()
    
    # 新規作成
    def create(self, validated_data):
        return Image.objects.create(**validated_data)