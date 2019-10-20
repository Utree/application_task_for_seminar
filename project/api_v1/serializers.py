# serializers.pyはpythonのモデルとveiws.pyとのクッション的役割
# DB(sqlite)を操作、パース等をする
from rest_framework import serializers
from api_v1.models import User, Token, Image, Post, Favorite

# ハッシュ化用
from django.utils import timezone
import hashlib

# ユーザーテーブルのシリアライザ
class UserSerializer(serializers.Serializer):
    # 出力項目を設定
    account_name = serializers.CharField(required=True, allow_blank=False, max_length=25)
    password = serializers.CharField(required=True, allow_blank=False, max_length=95)

    # 新規作成
    def create(self, validated_data):
        return User.objects.create(**validated_data)

    # ユーザー情報の取得
    @staticmethod
    def select(user_name):
        return User.objects.get(account_name=user_name)

# トークンテーブルのシリアライザ
class TokenSerializer(serializers.Serializer):
    # 出力項目を設定
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
    # 出力項目を設定
    url = serializers.ImageField()

    # 所有画像をリストにして、返す
    @staticmethod
    def select(id):
        # 画像URLをリストにする
        url_list = []
        for i in Image.objects.filter(user_id=id):
            url_list.append(str(i.url))
        # json形式に変換して、返す
        return ("{'image_url': " + str(url_list) + "}").replace("'", '"')

    # 画像URLの登録
    @staticmethod
    def create(file_path, user_info):
        insert_data = Image(url="api_v1/images/" + file_path, user_id=user_info)
        insert_data.save()

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'user_id', 'date', 'text', 'img_url', 'map_lat', 'map_lon', 'like_cnt')

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('id', 'user_id', 'post_id', 'create_time')

class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'user_id', 'date', 'text', 'img_url', 'like_cnt')
