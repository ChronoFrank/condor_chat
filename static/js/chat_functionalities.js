$(document).ready(function(){
        $('#action_menu_btn').click(function(){
            $('.action_menu').toggle();
        });

        get_available_users();
});

function get_available_users() {
    $.ajax({
        url: window.location.protocol+"api/v1/profiles/get_available_users/",
    }).then(function (data) {
        let html = '';
        $.each(data, function (index, object) {
            html += '<li class="active"><div class="d-flex bd-highlight">' +
                '<div class="img_cont">' +
                '<img class="rounded-circle user_img" src="'+object.avatar_url+'">'+
                '<span class="online_icon offline"></span></div>' +
                '<div class="user_info"><span>'+object.full_name+'</span></div></div></li>'
        });
        $("#concat_card_container").html(html);


    });
};

