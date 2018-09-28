from django.shortcuts import render
from django.http.response import HttpResponse
# import for file upload
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOADE_DIR = os.path.join(BASE_DIR, 'static/seminar/uploaded')

# Create your views here.
def index(request):
    return render(request, 'index.html')

# Create your views here.
def form(request):
    # POSTメソッドでない場合は404ページに飛ばす
    if request.method != 'POST':
        return render(request, '404.html')

    # ファイルアップロード（複数）
    # ファイルのリストをとる
    files = request.FILES.getlist('file[]')

    # 一つづつファイル操作
    for i in range(len(files)):
        # パスの指定
        path1 = os.path.join(UPLOADE_DIR, str(files[i]))
        # ファイルを保存
        with open(path1, 'wb') as ff:
         ff.write(files[i].file.read())

        # # データベースに保存
        # insert_data = FileNameModel(file_name = str(files[i]))
        # insert_data.save()

    # # # PDFをつくる
    # # make(title, files)

    # # return redirect('/static/files/python.pdf')
    
    # # そのままつくったPDFを投げる
    # response = HttpResponse(status=200, content_type='application/pdf')
    # response['Content-Disposition'] = 'filename="static/python.pdf"'
    
    # # PDFをつくる
    # make(title, files, response)
    return HttpResponse("Success")