# 画像投稿サイト

### APIドキュメント
https://qiita.com/yuuki_sekiya/private/a6a0d87917425227abf4

### DB ER図
![](https://d2mxuefqeaa7sj.cloudfront.net/s_F5BD2AC707D626C6F3286771CE0C236A048149558DDB7F75DEFC080E81A03A17_1538567298724_+2018-10-03+20.47.34.png)

## 環境構築
```
$ python3 -m venv penv
$ source penv/bin/activate
$ pip install  -r requirements.txt
```

## 使い方
```
cd project/
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
