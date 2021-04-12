$('input#loginButton').click( function() {
    $.ajax({
        url: '/checkLogin',
        type: 'POST',
        dataType: 'json',
        data: $('form#loginForm').serialize(),
        success: function(data) {
             $('#errorDialog').text('Incorrect username/password');
        }
    });
 });