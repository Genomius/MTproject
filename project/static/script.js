$( document ).ready(function() {
    var user_id = location.href.split('viewer_id=')[1].split('&')[0];
    var user_first_name;
    var user_last_name;

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
                'https://translate.yandex.net/api/v1.5/tr/translate?key=' +  + '&lang=en-ru&text=To%20be,+or+not+to+be%3F&text=That+is+the+question.'
            }
        });
    });

    $('.audio-edit-btn').click(function () {
        var id = $(this).parent()[0]['id'].split('audio-')[1];

    });
});
