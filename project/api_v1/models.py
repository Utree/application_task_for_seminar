# models.pyはDB(sqlite)とpythonのモデルとのクッション的役割
# ここで、テーブルやカラムを作ったり、カラムに制限を掛ける
from django.db import models

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
    # トークン生成時のタイムスタンプ(tokenに有効期限をつけることを見越して、作った。)
    creation_date = models.DateTimeField(auto_now_add=True)


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

# 投稿された内容を管理するテーブル
class Post(models.Model):
    # ユーザID(Userが削除されるとこのレコードも削除される)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    # 投稿した日時
    date = models.DateTimeField(auto_now_add=True)
    # 投稿するテキスト
    text = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        )
    # 投稿する画像(１つの投稿につき１画像)
    img_url = models.ImageField(upload_to="api_v1/images/")
    # 緯度
    map_lat = models.DecimalField(u'緯度', max_digits=20, decimal_places=10, default=0);
    # 経度
    map_lon = models.DecimalField(u'経度', max_digits=20, decimal_places=10, default=0);

    # いいねの数
    like_cnt = models.IntegerField()


# どのユーザがどの投稿にいいねしたかを管理するテーブル
class Favorite(models.Model):
    # ユーザID(Userが削除されるとこのレコードも削除される)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    # 投稿ID（Postが削除されるとこのレコードも削除される）
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    # タイムスタンプ
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together=(("user_id","post_id"))
