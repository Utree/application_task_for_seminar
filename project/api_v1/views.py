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
# イメージフィルタ
from api_v1.image_filter.anime import Anime
from api_v1.image_filter.canny import Canny
from api_v1.image_filter.gray import Gray
from api_v1.image_filter.laplacian import Laplacian
from api_v1.image_filter.sobel import Sobel

# ファイルの保存先のパス
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOADE_DIR = os.path.join(BASE_DIR, 'uploaded_files/api_v1/images')


# ユーザー登録API
@csrf_exempt # APIなので、csrf対策を無効にする
def register(request):
    # POST
    if request.method == 'POST':
        # JSONをパース
        data = JSONParser().parse(request)
        # Userモデルに当てはめる
        serializer = UserSerializer(data=data)

        # バリデーションを掛ける(パスワードはハッシュ化するので、空文字判定を先に行う)
       # パスワードが空かを確認する
        if serializer.initial_data["password"] == "":
            return HttpResponse("使用できないパスワードです。", status=403)

        # パスワードをハッシュ化
        serializer.initial_data["password"] = make_password(serializer.initial_data["password"], hasher='argon2')

        # 有効なものかを判断する
        if serializer.is_valid():
            # 保存
            try:
                serializer.save()
                # ユーザーIDを取得
                user = UserSerializer.select(user_name=serializer.initial_data["account_name"])
                # トークン生成
                token = TokenSerializer.create(user)
                # ユーザーにトークンを渡す
                data = '{"token": "' + token +'"}'
                response = HttpResponse(data, status=200)
                response['content-type'] = 'application/json; charset=utf-8'
                return response
            # account_nameがかぶったときなどのエラー処理
            except Exception as e:
                print(e)
                return HttpResponse("ユーザー名が使われています", status=409)
        # 不正なリクエストの場合
        return HttpResponse("不正なリクエスト", status=400)
    else:
        return HttpResponse("不正なリクエスト", status=400)

# ユーザーログインAPI
@csrf_exempt # APIなので、csrf対策を無効にする
def login(request):
    # POST
    if request.method == 'POST':
        # JSONをパース
        data = JSONParser().parse(request)
        # Userモデルに当てはめる
        serializer = UserSerializer(data=data)
        # 有効なものかを判断する
        if serializer.is_valid():
            try:
                # ユーザーを取得
                user = UserSerializer.select(user_name=serializer.initial_data["account_name"])
            except:
                return HttpResponse("ユーザーが存在しません", status=401)

            # ログイン成功時
            if check_password(serializer.data["password"], user.password):
                # トークン生成
                token = TokenSerializer.create(user)
                # ユーザーにトークンを渡す
                data = '{"token": "' + token +'"}'
                response = HttpResponse(data, status=200)
                response['content-type'] = 'application/json; charset=utf-8'
                return response
            # ログイン失敗時
            else:
                return HttpResponse("ログイン失敗", status=401)
        # 不正なリクエスト
        return HttpResponse("不正なリクエスト", status=400)
    else:
        return HttpResponse("不正なリクエスト", status=400)

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
        # ファイルアップロード（複数）
        # ファイルのリストをとる
        try:
            files = request.FILES.getlist('file[]')
            print(files)
        except Exception as e:
            print(e)
            return HttpResponse("file is empty", status=400)
        # 一つづつファイル操作
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


                # ヘッダを確認
                try:
                    # imageFilterを掛ける (別スレッドで実行)
                    if str(request.POST['image_filter']) == 'anime':
                        t = threading.Thread(target=Anime, args=(file_name,))
                        t.start()
                    elif str(request.POST['image_filter']) == 'canny':
                        t = threading.Thread(target=Canny, args=(file_name,))
                        t.start()
                    elif str(request.POST['image_filter']) == 'gray':
                        t = threading.Thread(target=Gray, args=(file_name,))
                        t.start()
                    elif str(request.POST['image_filter']) == 'laplacian':
                        t = threading.Thread(target=Laplacian, args=(file_name,))
                        t.start()
                    elif str(request.POST['image_filter']) == 'sobel':
                        t = threading.Thread(target=Sobel, args=(file_name,))
                        t.start()
                    else:
                        pass
                # ヘッダが無かった場合
                except:
                    pass

                # データベースに保存
                ImageSerializer.create(file_path=file_name, user_info=user)
            # 画像ファイル以外の拡張子が来た時
            else:
                return HttpResponse("jpeg, jpg, pngのみ対応しています。", status=406)

        return HttpResponse("Success")

    # その他
    else:
        return HttpResponse("不正なリクエスト", status=400)




# # api viewer(debug用)
# import django_filters
# from rest_framework import viewsets, filters
# from api_v1.models import User, Token, Image

# # Create your views here.
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# class TokenViewSet(viewsets.ModelViewSet):
#     queryset = Token.objects.all()
#     serializer_class = TokenSerializer

# class ImageViewSet(viewsets.ModelViewSet):
#     queryset = Image.objects.all()
#     serializer_class = ImageSerializer
