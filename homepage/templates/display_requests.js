function update_request(request_id, status) {
    $.ajax({
      type: "POST",
      url: "{% url 'homepage:display_requests_post' %}",
      contentType: "application/json",
      data: JSON.stringify({
        'request_id' : request_id,
        'status':status}),
      dataType: 'json',
      beforeSend: function () {
      },
      complete: function () {
      },
      success: function (response) {
        // console.log(response.formdata)

        // Update Satus output
        var status_id = request_id+"-status"
        if (status==true){
          document.getElementById(status_id).innerText="Accepted"
        }
        if (status==false){
          document.getElementById(status_id).innerText="Denied"
        }

        // Hide buttons
        var accept_id = request_id+"-accept"
        var deny_id = request_id+"-deny"
        document.getElementById(accept_id).style.visibility='hidden'
        document.getElementById(deny_id).style.visibility='hidden'
      },
      error: function (err) {
        console.log(err);
      }
    });
}