
document.getElementById('reportAWebsite').addEventListener("click", openReportForm)
document.getElementById('requestReportRemove').addEventListener("click", openRemoveReportForm)
document.getElementById('submitReport').addEventListener("click", sendReportData)
document.getElementById('submitRemoveReport').addEventListener("click", sendRemoveFlagData)

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

// When a user clicks on the Report Website button, it will display the report website form 
// and the submit report button while hiding the original report website button
function openReportForm(){ 
    document.getElementById('reportForm').style.display = 'block';
    document.getElementById('submitReport').style.display = '';
    document.getElementById('reportAWebsite').style.display = 'none';
    document.getElementById('report_display').style.visibility = 'hidden';
}

function openRemoveReportForm(){
    document.getElementById('remove_flag_display').style.visibility = 'hidden';
    document.getElementById('removeReportForm').style.display = '';
    document.getElementById('submitRemoveReport').style.display = '';    
    document.getElementById('requestReportRemove').style.display = 'none';
}

// For reporting a website
function sendReportData(){
    document.getElementById('report_display').style.visibility = 'visible';
    document.getElementById('reportAWebsite').style.display = '';
    document.getElementById('reportForm').style.display = 'none';
    document.getElementById('submitReport').style.display = 'none';
    var data = {};
    data.ReportedWebsite = document.getElementById('reported_website').value;
    $.post('http://127.0.0.1:8000/DDS_Server/predict', JSON.stringify(data), 
    function(data){})
}

function sendRemoveFlagData(){
    document.getElementById('removeReportForm').style.display = 'none';
    document.getElementById('submitRemoveReport').style.display = 'none';
    document.getElementById('requestReportRemove').style.display = '';
    document.getElementById('remove_flag_display').style.visibility = 'visible';
    var data = {};
    data.RemoveFlagRequestWebsite = document.getElementById('removeReportWebsite').value;
    $.post('http://127.0.0.1:8000/DDS_Server/predict', JSON.stringify(data), 
    function(data){})
}

