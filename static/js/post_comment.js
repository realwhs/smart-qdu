$(document).ready(function (){
    post_comment();
})

function post_comment(){
    $("#post_comment_submit").click(function (){
        form = $("form#post_comment_form");
        messenger = Messenger();

        $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: form.serialize(),
            success: function (data){
                var response = JSON.parse(data);
                if(response.status == "success"){
                    messenger.post({
                        message: "发表评论成功！",
                        type: "success"
                    })
                    location.reload()
                }
                else if(response.status == "error")
                    messenger.post({
                        message: response.content,
                        type: "error"
                    })
                else if(response.status == "not_login")
                    messenger.post({
                        message: "发表评论前请先登录！",
                        type: "error"
                    })
            },
        });
        return false;
    })
}


