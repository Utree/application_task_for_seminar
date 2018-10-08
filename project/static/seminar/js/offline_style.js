// 高さを取得
var h = $(window).height();

// オフライン画面の制御
window.onload = function() {
    if (navigator.onLine === true) {
        // オンライン時: 非表示
    } else if (navigator.onLine === false) {
        // オフライン時: 表示
        var h = $(window).height();
        $('#offline-bg ,#offline').height(h).css('display','block');
    } else {
        // その他: 表示
        var h = $(window).height();
        $('#offline-bg ,#offline').height(h).css('display','block');
    }
}
window.addEventListener("online", function(){
    // オンライン復帰時
    $('#offline-bg ,#offline').height(h).css('display','none');
}, false);
window.addEventListener("offline", function() {
    // オフライン時
    $('#offline-bg ,#offline').height(h).css('display','block');
}, false);