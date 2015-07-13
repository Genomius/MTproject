$( document ).ready(function() {
    var user_id = location.href.split('viewer_id=')[1].split('&')[0];
    var user_first_name;
    var user_last_name;

    $.ajaxSetup({
         beforeSend: function(xhr, settings) {
             function getCookie(name) {
                 var cookieValue = null;
                 if (document.cookie && document.cookie != '') {
                     var cookies = document.cookie.split(';');
                     for (var i = 0; i < cookies.length; i++) {
                         var cookie = jQuery.trim(cookies[i]);
                         // Does this cookie string begin with the name we want?
                     if (cookie.substring(0, name.length + 1) == (name + '=')) {
                         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                         break;
                     }
                 }
             }
             return cookieValue;
             }
             if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                 // Only send the token to relative URLs i.e. locally.
                 xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
             }
         }
    });

    VK.init(function() {
        VK.api('users.get',{user_ids: user_id}, function(data) {
          if (data.response) {
              user_first_name = data.response[0]['first_name'];
              user_last_name = data.response[0]['last_name'];

              $('#user-name').text(user_first_name + " " + user_last_name);
          }
        });

        VK.api('audio.get',{owner_id: user_id}, function(data) {
            if (data.response) {
                $(data.response.items).each(function(index, object){
                    var lyrics_id = $(this)[0]['lyrics_id'];
                    var artist = $(this)[0]['artist'];
                    var title = $(this)[0]['title'];

                    $('#user-audio').append('<div class="audio-block row" id="audio-' + lyrics_id + '">' +
                        '<i class="col-lg-1 glyphicon glyphicon-cd audio-cd-icon"></i>' +
                        '<p class="col-lg-7 audio-name">' + artist + " - " + title + '</p>' +
                        '<i class="col-lg-1 glyphicon glyphicon-log-in audio-translate-btn" title="Перевести"></i>' +
                        '<i class="col-lg-1 glyphicon glyphicon-edit audio-edit-btn" title="Переименовать"></i>' +
                    '</div>');
                });
            }
        });
      },
      function() {
         alert("ERROR");
      },
      '5.30'
    );

    $('body').on('click', '.audio-translate-btn', function(){
        var lyrics_id = $(this).parent()[0]['id'].split('audio-')[1];

        VK.api('audio.getLyrics',{lyrics_id: lyrics_id}, function(data) {
            if (data.response) {
                var text = data.response['text'];
                $.ajax({
                    type: "POST",
                    url: '/',
                    dataType: 'json',
                    data: {text: text},
                    success: function (data) {
                        if (data.russian) {
                            alert(data.russian);
                        }
                        else if (data.error) {
                            alert(data.error)
                        }
                        else {
                            //console.log(data.result);
                            alert(data.result.split('<text>текст=')[1].split('</text>')[0]);
                        }

                    },
                    error: function (err) {
                        console.log('translate-ajax-response-error: ' + err);
                    }
                });
            }
            else{
                $.ajax({
                    type: "POST",
                    url: 'translate/',
                    dataType: 'json',
                    data: {text: '1'},
                    success: function (data) {
                        console.log(data);
                    },
                    error: function (err) {
                        console.log('translate-ajax-response-error: ' + err);
                    }
                });
            }
        });
    });

    $('.audio-edit-btn').click(function () {
        var id = $(this).parent()[0]['id'].split('audio-')[1];

    });
});
