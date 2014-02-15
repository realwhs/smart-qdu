$(document).ready(function (){
    send_mail();
})

function send_mail(){
    $("#send_mail_submit").click(function (){
        form = $("form#send_mail_form");
        messenger = Messenger();

        $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: form.serialize(),
            success: function (data){
                var response = JSON.parse(data);
                if(response.status == "success"){
                    messenger.post({
                        message: "发送成功！",
                        type: "success"
                    })
                    window.location.href = response.redirect
                }
                else if(response.status == "error")
                    messenger.post({
                        message: response.content,
                        type: "error"
                    })
            },
        });
        return false;
    })
}


