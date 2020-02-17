$(document).ready(function(){
        $('#action_menu_btn').click(function(){
            $('.action_menu').toggle();
        });
        // load contact list from available users in database
        get_available_users();

        // add callback for search users from the search bar
        $("#searchbar").on("keyup", function() {
            var value = $(this).val().toLowerCase();
            get_available_users(value);
        });

});

$(document).on('click','.user_li',function(e) {
    let is_selected = $(this).hasClass('active');
    if (is_selected === false){
        let user_id = $(this).attr('id');
        $('li.active').removeClass('active');
        $(this).addClass('active');

        $.ajax({url: window.location.protocol+"api/v1/profiles/"+user_id+'/'}).then(function (data) {
            $('div.msg_head img.user_img').attr('src', data.avatar_url);
            $('div.msg_head div.user_info span').text('Chat with '+ data.full_name);
        });

    }

});

function get_available_users(params=null) {
    let args = {
            url: window.location.protocol+"api/v1/profiles/get_available_users/",
        };
    if (params){
         args = {
            url: window.location.protocol+"api/v1/profiles/get_available_users/",
            data: {full_name: params}
        }
    }
    $.ajax(args).then(function (data) {
        let html = '';
        $.each(data, function (index, object) {
            html += '<li class="user_li" id="'+object.id+'"><div class="d-flex bd-highlight">' +
                '<div class="img_cont">' +
                '<img class="rounded-circle user_img" src="'+object.avatar_url+'">'+
                '</div>' +
                '<div class="user_info"><span>'+object.full_name+'</span></div></div></li>'
        });
        $("#concat_card_container").html(html);


    });
};

