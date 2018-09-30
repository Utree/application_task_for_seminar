from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from api_v1.models import User, Token, Image
from api_v1.serializers import UserSerializer, TokenSerializer, ImageSerializer
# パスワードhasher
from django.contrib.auth.hashers import make_password


@csrf_exempt
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
                # トークン生成
                # トークン保存
                # トークン付与
                return HttpResponse("登録完了", status=201)
            # account_nameがかぶったときなどのエラー処理
            except:
                return HttpResponse("ユーザー名が使われています", status=400)
        # 不正なリクエストの場合
        return HttpResponse("不正なリクエスト", status=400)
    else:
        return HttpResponse("不正なリクエスト", status=405)

# @csrf_exempt
# def login(request):
#     # POST
#     if request.method == 'POST':
#         # JSONをパース
#         data = JSONParser().parse(request)
#         # Userモデルに当てはめる
#         serializer = UserSerializer(data=data)
#         if serializer.is_valid()
            

@csrf_exempt
def user_detail(request, pk):
    try:
        users = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = UserSerializer(users)
        return JsonResponse(serializer.data)
    
    return HttpResponse(status=405)

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