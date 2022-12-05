document.getElementById('confirm_payment').addEventListener("click", )


function sendConfirmPayment(){
    var data = {};
    var subscription = "1 Month";
    data.userid = sessionStorage.getItem('userID');
    data.subscribed = subscription;
    $.post('http://127.0.0.1:8000/DDS_Server/predict', JSON.stringify(data), 
    function(data){})
}