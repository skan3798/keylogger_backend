$(document).ready(function(){
    //when page loads, show the contents of the keylogger
    $('.container > #keylogView').show();
    showKeys();
      
  
    })
  
  // request and display all the keys collected
  function showKeys() {
    $.ajax({
      url: "./showKeylog",
      method: "GET",
      dataType: 'json',
      success: showKeyTable,
      fail: console.log("FAILED")
    });
    console.log("help");
  }
  
  function showKeyTable(keys){
    $('#keylogView > table > tbody').empty();
    console.log("hello");
  
    for (const [key,value] of Object.entries(keys)){
      var k = JSON.parse(value);
      $('#keylogView > table > tbody').append(
        '<tr><td>'
        + k.time
        +'</td><td>'
        + k.key_up
        +'</td><td>'
        + k.key
        +'</td></tr>'
      );
    }
  }