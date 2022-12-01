
function encodeImageFileAsURL(element, cb) { // We pass a callback as parameter
    var preview = document.querySelector('img')
    var file = element.files[0];
    var reader = new FileReader();
    reader.onload = function(e) {
        preview.src = reader.result;
        var base64Image = reader.result
        // base64Image = base64Image.replace('data:image/png;base64,', '').replace('data:image/jpg;base64,', '')
        // Content is ready, call the callback
        cb(base64Image);
    }
    reader.readAsDataURL(file);
}

var P = 0;

function sendData(data, url) {
    console.log("Try to send the data");
    $.post(url,JSON.stringify(data),
    function(data, textStatus, jqXHR)
    {
        P = data.prediction;
        document.getElementById('display').innerHTML = "Prediction: " + P;
    })
}


