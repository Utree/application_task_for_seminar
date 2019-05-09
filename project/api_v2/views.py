from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
# JSONパーサー&レンダラー
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
# シリアライザ (db操作用のController的な役割)
from api_v1.serializers import UserSerializer, TokenSerializer, ImageSerializer
# パスワードhasher
from django.contrib.auth.hashers import make_password, check_password
# Json形成
from django.utils.six import BytesIO
# ハッシュ化
import hashlib
# タイムスタンプ用
from django.utils import timezone
# ファイル名取得
import os.path
# import for file upload
import os
# 別スレッドで処理する用
import threading

from api_v2.model.style_transfer import style_transfer

import re

# ファイルの保存先のパス
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOADE_DIR = os.path.join(BASE_DIR, 'uploaded_files/api_v1/images')

# Create your views here.
# 画像API
@csrf_exempt
def images(request):
    try:
        # トークンの認証
        if request.META['HTTP_AUTHORIZATION']:
            # Bearerスキームを取り除いて、tokenを認証し、userオブジェクトを得る
            user = TokenSerializer.auth(request.META['HTTP_AUTHORIZATION'].replace("Bearer ", ""))
            # トークンに紐付けられたアカウントが無かった場合
            if not user:
                response = HttpResponse("token is wrong", status=401)
                response["WWW-Authenticate"] = 'realm="The access token was expired", error="invalid_token"'
                return response
        # トークンが空の場合
        else:
            response = HttpResponse("token is empty", status=401)
            response["WWW-Authenticate"] = 'realm="token is empty", error="invalid_token"'
            return response
    except:
        response = HttpResponse("token is empty", status=401)
        response["WWW-Authenticate"] = 'realm="token is empty", error="invalid_token"'
        return response

    # GETメソッド
    if request.method == 'GET':
        # レスポンスをつくる
        response = HttpResponse(ImageSerializer.select(user.id), status=200)
        response['content-type'] = 'application/json; charset=utf-8'
        return response
    # POSTメソッド
    elif request.method == 'POST':
        try:
            # print(re.search(r"C\:\\fakepath\\(?P<name>.*.)", str(request.POST['original_image']).group(2)))
            files = [request.FILES['original_image'], request.FILES['style_image']]
            print(files)
        except Exception as e:
            return HttpResponse("file is empty", status=400)
        # ファイル保存
        for i in range(len(files)):
            # ファイル名と拡張子を別にする
            name, ext = os.path.splitext(str(files[i]))
            # バリデーションを掛ける
            if (ext == '.jpeg') or (ext == '.png') or (ext == '.jpg'):
                # ファイルネームのハッシュ化(URLに使えない文字を消す為)
                name = hashlib.sha1(name.encode('utf-8')).hexdigest()[:10]
                # タイムスタンプを付けて、ファイルのリネーム
                dt = timezone.now()
                file_name = name + dt.strftime('%Y%m%d%H%M%S%f') + ext
                # パスの指定
                path1 = os.path.join(UPLOADE_DIR, file_name)
                # ファイルを保存
                with open(path1, 'wb') as ff:
                    ff.write(files[i].file.read())

                # ファイル名を更新
                files[i] = file_name
            # 画像ファイル以外の拡張子が来た時
            else:
                return HttpResponse("jpeg, jpg, pngのみ対応しています。", status=406)

        # ファイルネームのハッシュ化(URLに使えない文字を消す為)
        name = hashlib.sha1((str(files[0])+str(files[1])).encode('utf-8')).hexdigest()[:10]
        # タイムスタンプを付けて、ファイルのリネーム
        dt = timezone.now()
        file_name = name + dt.strftime('%Y%m%d%H%M%S%f') + ext

        # 画像処理
        t = threading.Thread(target=style_transfer, args=(files[0], files[1], file_name,))
        t.start()

        # データベースに保存
        ImageSerializer.create(file_path=file_name, user_info=user)

        return HttpResponse("Success")

    # その他
    else:
        return HttpResponse("不正なリクエスト", status=400)
