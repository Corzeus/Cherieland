function analysecode(){
    console.log("C");

    var obj = document.getElementById("inputitem");
    var text = obj.value;
    text = text.toUpperCase();
    var dict_key_words = load_data();
    var keys = Object.keys(dict_key_words)
    if (keys.includes(text)){
        window.open("Pages/"+dict_key_words[text]);
    }
}

function load_data(){
    var data = {
        "CHERIELAND": "CarteNicolas.html",
        "COPAINVILLE": "",
        "SOLAL": "Solal.html",
        "CASTELLE": "CamilleEstelle.html"
    }
    return data;
}