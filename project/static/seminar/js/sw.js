// ServiceWorker処理：https://developers.google.com/web/fundamentals/primers/service-workers/?hl=ja

// キャッシュ名とキャッシュファイルの指定
var CACHE_NAME = 'seminar-caches-v1';
var urlsToCache = [
	'/login',
	'/register',
	'/home',
	'/add',
	'/static/seminar/js/home_style.js',
	'/static/seminar/js/offline_style.js',
	'/static/seminar/js/sw.js',
	'/static/seminar/img/icon.png',
	'/static/seminar/img/no_image.png',
	'/static/seminar/css/home_style.css',
	'/static/seminar/css/loading_animation.css',
	'/static/seminar/css/modify_form_items.css',
	'/static/seminar/css/offline_style.css',
	'/manifest.json',
	'https://fonts.googleapis.com/css?family=Roboto:300,400,500,700|Material+Icons',
	'https://unpkg.com/bootstrap-material-design@4.1.1/dist/css/bootstrap-material-design.min.css',
	'https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js',
	'https://unpkg.com/popper.js@1.12.6/dist/umd/popper.js',
	'https://unpkg.com/bootstrap-material-design@4.1.1/dist/js/bootstrap-material-design.js',
	'https://use.fontawesome.com/releases/v5.3.1/css/all.css',
	'https://fonts.googleapis.com/css?family=Open+Sans:300italic,400italic,600italic,700italic,800italic,400,300,600,700,800',
	'https://fonts.googleapis.com/css?family=Merriweather:400,300,300italic,400italic,700,700italic,900,900italic',
	'https://blackrockdigital.github.io/startbootstrap-creative/vendor/magnific-popup/magnific-popup.css',
	'https://fonts.googleapis.com/icon?family=Material+Icons',
	'https://blackrockdigital.github.io/startbootstrap-creative/vendor/jquery/jquery.min.js',
	'https://blackrockdigital.github.io/startbootstrap-creative/vendor/jquery-easing/jquery.easing.min.js',
	'https://blackrockdigital.github.io/startbootstrap-creative/vendor/scrollreveal/scrollreveal.min.js',
	'https://blackrockdigital.github.io/startbootstrap-creative/vendor/magnific-popup/jquery.magnific-popup.min.js',
	'https://blackrockdigital.github.io/startbootstrap-creative/js/creative.min.js'
];

// インストール(≒ファイルをキャッシュする)処理
self.addEventListener('install', function(event) {
	event.waitUntil(
		// キャッシュをopenして、キャッシュファイルのパスのリストをaddAllしている
		caches
			.open(CACHE_NAME)
			.then(function(cache) {
				console.log('ローカルにデータをキャッシュします');
				return cache.addAll(urlsToCache);
			})
	);
});

// リソースフェッチ時のキャッシュロード(≒キャッシュを返す)処理
self.addEventListener('fetch', function(event) {
	event.respondWith(
		caches
			.match(event.request)
			.then(function(response) {
				if(response) {
					console.log('サーバーからのデータを表示します');
					return response;
				} else {
					// キャッシュがなければリクエストを投げて、キャッシュをレスポンスに入れる
					return fetch(event.request)
						.then(function(res) {
							return cache.open(CACHE_NAME)
								.then(function(cache) {
									// 最後にresを返せるように、ここではclone()をする必要がある
									cache.put(event.request.url, res.clone());
									console.log('キャッシュからのデータを表示します');
									return res;
								})
						})
						.catch(function() {
							// エラーが発生しても何もしない
						});
				}
			})
	);
});

// 新しいバージョンのキャッシュがあったら古いキャッシュを削除
self.addEventListener('activate', function(event) {
  event.waitUntil(
    caches.keys()
      .then(function(keyList) {
        return Promise.all(keyList.map(function(key) {
          if (key !== CACHE_NAME && key !== CACHE_NAME) {
            console.log('古いキャッシュを削除します');
            return caches.delete(key);
          }
        }));
      })
  );
  return self.clients.claim();
});
