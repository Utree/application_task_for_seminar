$(function() {
  var url = '/api/v1/images/';
  var token = localStorage.getItem('token');
  var headerParams = {'Authorization':'Bearer ' + token};
  $.ajax({
    url: url,
    type:'GET',
    headers: headerParams,
    dataType: 'json',
    timeout: 3000,
  }).done(function(response) {
     // コンテンツを表示
    for (var i=0; i<response.image_url.length; i++) {
        var content = '<div class="col-lg-4 col-sm-6">'
                    + '<a class="portfolio-box" href="/media/' + response.image_url[i] + '">'
                    + '<img class="img-fluid" src="/media/' + response.image_url[i] + '" alt="">'
                    + '</a>'
                    + '</div>';
        $('#contents').append(content);
    }
    // コンテンツ数が0の場合はno_image.pngを表示
    if(response.image_url.length == 0) {
        var content = '<div class="col-lg-4 col-sm-6">'
                    + '<a class="portfolio-box" href="/static/seminar/img/no_image.png">'
                    + '<img class="img-fluid" src="/static/seminar/img/no_image.png" alt="">'
                    + '</a>'
                    + '</div>';
        $('#contents').append(content);
    }
  }).fail(function(XMLHttpRequest, textStatus, errorThrown) {
    // トークンが間違っている場合、強制的にLoginページに飛ばす
    location.href = "login";
  })
    $('#logout').click(function(){
         localStorage.clear();
         location.href = "login";
    });
})