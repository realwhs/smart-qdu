$(document).ready(function (){
    get_contact();
})


function get_contact(){
    $("#get_contact_submit").click(function (){
        form = $("form#get_contact_form");
        contact = $("#contact")
        $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: form.serialize(),
            success: function (data){
                var response = JSON.parse(data);
                if(response.status == "success"){
                   contact.html(response.content)
                   $("#get_contact_form").hide()
                }
                else if(response.status == "error"){
                   contact.html(response.content)
                   location.reload()
                }
            },
        });
        return false;
    })
}


