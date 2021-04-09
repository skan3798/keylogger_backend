$(document).ready(function(){
    //when page loads, show the contents of the keylogger
    $('.container > #keyAll').show();
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
    $('#keyAll > table > tbody').empty();
  
    /*for (const [key,value] of Object.entries(keys)){
      var k = JSON.parse(value);
	  console.log(k);
      $('#keylogView > table > tbody').append(
        '<tr><td>'
        + k.datetime
        +'</td><td>'
        + k.isKeyDown
        +'</td><td>'
        + k.windowName
        +'</td><td>'
	    + k.processedKey
	    +'</td></tr>'
      );
    } */
    keys.forEach((item) => {
        console.log(item)
        $('#keylogView > table > tbody').append(
            '<tr><td>'
            + item.datetime
            +'</td><td>'
            + item.isKeyDown
            +'</td><td>'
            + item.windowName
            +'</td><td>'
    	    + item.processedKey
    	    +'</td></tr>'
        )
    })
  }
