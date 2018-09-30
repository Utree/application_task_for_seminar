from django.db import models

# ハッシュ化用
from django.utils import timezone
import hashlib

# Create your models here.
# ユーザーテーブル(ユーザーIDは自動追加)
class User(models.Model):
    # 名前 (後につくる、表示名と区別化するために、account_とつけている)
    account_name = models.CharField(
        max_length=20,
        unique=True,
        null=False,
        blank=False
    )
    # パスワード
    password = models.CharField(
        max_length=100,
        null=False,
        blank=False
    )
    # アカウント作成時のタイムスタンプ(デバッグ用)
    creation_date = models.DateTimeField(auto_now_add=True)

# トークンテーブル(複数端末での利用を見越して、Userテーブルと別に作った)
# 現状、1ユーザー1トークン制
class Token(models.Model):
    # トークンID
    token_id = models.AutoField(primary_key=True)
    # ユーザーID
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    # トークン
    token = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        db_index=True
    )
    # トークン生成時のタイムスタンプ(デバッグ用)
    creation_date = models.DateTimeField(auto_now_add=True)
    
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
    
# 画像のURL保存用テーブル
class Image(models.Model):
    # イメージID
    image_id = models.AutoField(primary_key=True)
    # イメージURL
    url = models.ImageField(upload_to="api_v1/images")
    # ユーザーID
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    # イメージ追加時のタイムスタンプ(デバッグ用)
    creation_date = models.DateTimeField(auto_now_add=True)
    