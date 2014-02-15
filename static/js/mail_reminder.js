$(document).ready(function (){
    mail_status();
})


function mail_status()
{
    $.getJSON("/mail/get_status/", function(data)
	{
	    //var response = JSON.parse(data);
		if (data.status == "new_mail")
		{

		    $("#mail_reminder").removeAttr("style");
		}
	});
}