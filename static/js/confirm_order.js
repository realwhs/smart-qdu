$(document).ready(function (){
    submit_order();
})

function submit_order(){
    $("#confirm_submit").click(function (){
        form = $("form#confirm_form");
        messenger = Messenger();

        $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: form.serialize(),
            success: function (data){
                var response = JSON.parse(data);
                if(response.status == "success"){
                    messenger.post({
                        message: "订单提交成功",
                        type: "success"
                    })
                    window.location.href=response.redirect
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


