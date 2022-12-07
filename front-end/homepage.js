document.getElementById('Upload_Image').addEventListener('change', testing)
document.getElementById('reportAWebsite').addEventListener("click", openReportForm)
document.getElementById('requestReportRemove').addEventListener("click", openRemoveReportForm)
document.getElementById('submitReport').addEventListener("click", sendReportData)
document.getElementById('submitRemoveReport').addEventListener("click", sendRemoveFlagData)

function testing() {
  var inputfile = document.getElementById('Upload_Image');
  encodeImageFileAsURL(inputfile)
}

function encodeImageFileAsURL(element) { // We pass a callback as parameter
    console.log("hello");
    var preview = document.querySelector('img')
    var file = element.files[0];
    var reader = new FileReader();
    reader.onload = function(e) {
      preview.src = reader.result;
      var base64Image = reader.result
      // base64Image = base64Image.replace('data:image/png;base64,', '').replace('data:image/jpg;base64,', '')
      // Content is ready, call the callback
      var data = {};
      data.userid = sessionStorage.getItem('userID');
      data.picture = base64Image; 
      console.log(data);
      sendData(data, 'http://127.0.0.1:8000/DDS_Server/predict');
  }
    reader.readAsDataURL(file);

}

var P = 0;

function sendData(data, url) {
    fetch(url, {
        method: 'POST', // or 'PUT'
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })
        .then((response) => response.json())
        .then((data) => {
          console.log('Success:', data);
          P = data.prediction;
          document.getElementById('display').innerHTML = "Prediction: " + P;
        })
        .catch((error) => {
          console.error('Error:', error);
    });
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
    data.type = "flag";
    data.userid = sessionStorage.getItem('userID');
    data.domainname = document.getElementById('reported_website').value;
    console.log(data.domainname);
    fetch('http://127.0.0.1:8000/DDS_Server/report', {
        method: 'POST', // or 'PUT'
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })
        .then((data) => {
          console.log('Success:', data);
        })
        .catch((error) => {
          console.error('Error:', error);
    });
    
}

function sendRemoveFlagData(){
    document.getElementById('removeReportForm').style.display = 'none';
    document.getElementById('submitRemoveReport').style.display = 'none';
    document.getElementById('requestReportRemove').style.display = '';
    document.getElementById('remove_flag_display').style.visibility = 'visible';
    var data = {};
    data.type = "false_flag";
    data.userid = sessionStorage.getItem('userID');
    data.domainname = document.getElementById('removeReportWebsite').value;
    console.log("hi2");

    fetch('http://127.0.0.1:8000/DDS_Server/report', {
        method: 'POST', // or 'PUT'
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })
        .then((response) => response.json())
        .then((data) => {
          console.log('Success:', data);
        })
        .catch((error) => {
          console.error('Error:', error);
    });
}

