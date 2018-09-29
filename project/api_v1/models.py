from django.db import models

# Create your models here.
# ユーザーテーブル(ユーザーIDは自動追加)
class User(models.Model):
    # 名前
    account_name = models.CharField(
        max_length=20,
        unique=True,
        null=False,
        blank=False
    )
    # パスワード
    password = models.CharField(
        max_length=50,
        null=False,
        blank=False
    )
    # アカウント作成時のタイムスタンプ
    creation_date = models.DateTimeField(auto_now_add=True)

# トークンテーブル
class Token(models.Model):
    # トークンID
    token_id = models.AutoField(primary_key=True)
    # ユーザーID
    user_id = models.IntegerField(null=False, blank=False)
    # トークン
    token = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        db_index=True
    )
    # トークン生成時のタイムスタンプ
    creation_date = models.DateTimeField(auto_now_add=True)
    
# 画像のURL保存用テーブル
class Image(models.Model):
    # イメージID
    image_id = models.AutoField(primary_key=True)
    # イメージURL
    url = models.ImageField(upload_to="api_v1/images")
    # ユーザーID
    user_id = models.IntegerField(null=False, blank=False)
    # イメージ追加時のタイムスタンプ
    creation_date = models.DateTimeField(auto_now_add=True)
    