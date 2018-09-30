from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from api_v1.models import User, Token, Image
from api_v1.serializers import UserSerializer, TokenSerializer, ImageSerializer
# パスワードhasher
from django.contrib.auth.hashers import make_password, check_password
# Json形成
from django.utils.six import BytesIO


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
            return HttpResponse("使用できないパスワードです。", status=400)
        
        # パスワードをハッシュ化
        serializer.initial_data["password"] = make_password(serializer.initial_data["password"], hasher='argon2')
        
        # 有効なものかを判断する
        if serializer.is_valid():
            # 保存
            try:
                serializer.save()
                # ユーザーIDを取得
                user = User.objects.get(account_name=serializer.data["account_name"])
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
                return HttpResponse("ユーザー名が使われています", status=400)
        # 不正なリクエストの場合
        return HttpResponse("不正なリクエスト", status=400)
    else:
        return HttpResponse("不正なリクエスト", status=405)

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
                user = User.objects.get(account_name=serializer.initial_data["account_name"])
            except:
                return HttpResponse("ユーザーが存在しません", status=400)
            
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
                return HttpResponse("ログイン失敗", status=400)
        # 不正なリクエスト
        return HttpResponse("不正なリクエスト", status=400)
    else:
        return HttpResponse("不正なリクエスト", status=405)
            
# 画像API
@csrf_exempt
def images(request):
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
    
    # GETメソッド
    if request.method == 'GET':
        url_list = []
        for i in Image.objects.filter(user_id=user.id):
            url_list.append(str(i.url))
        data = ("{'image_url': " + str(url_list) + "}").replace("'", '"')
        response = HttpResponse(data, status=200)
        response['content-type'] = 'application/json; charset=utf-8'
        return response
    # POSTメソッド
    elif request.method == 'POST':
        return HttpResponse("post", status=200)
    # その他
    else:
        return HttpResponse("不正なリクエスト", status=405)




# api viewer
import django_filters
from rest_framework import viewsets, filters

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class TokenViewSet(viewsets.ModelViewSet):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer