document.getElementById('cancel_sub').addEventListener("click", openCancelSubscriptionForm);
document.getElementById('toggle_warnings').addEventListener("click", toggle_warnings);
document.getElementById('Keep_Sub_Button').addEventListener("click", keepSubButtonForm);
document.getElementById('Cancel_Sub_Button').addEventListener("click", sendCancelSubscription);

if(cancel_subscription_button){
    cancel_subscription_button.addEventListener("click", confirm_cancel_subscription);
}

// toggles warnings button text (on/off) on user click 
function toggle_warnings(){
    var elem = document.getElementById("toggle_warnings");
    if (elem.value=="Currently On") elem.value = "Currently Off";
    else elem.value = "Currently On"
}

function openCancelSubscriptionForm(){
    document.getElementById('cancel_sub_status').innerHTML = "";
    document.getElementById('cancel_sub').style.display = 'none';
    document.getElementById('areyousure').style.visibility = "visible";
    document.getElementById('Cancel_Sub_Button').style.display = '';
    document.getElementById('Keep_Sub_Button').style.display = '';
}

function keepSubButtonForm(){
    document.getElementById('cancel_sub_status').innerHTML = "No worries, your DDS subscription is still active.";
    document.getElementById('cancel_sub').style.display = '';
    document.getElementById('areyousure').style.visibility = "hidden";
    document.getElementById('Cancel_Sub_Button').style.display = 'none';
    document.getElementById('Keep_Sub_Button').style.display = 'none';  
}

function sendCancelSubscription(){
    document.getElementById('cancel_sub_status').innerHTML = "Your DDS subscription has been successfully terminated.";
    document.getElementById('areyousure').style.visibility = "hidden";
    document.getElementById('Cancel_Sub_Button').style.display = 'none';
    document.getElementById('Keep_Sub_Button').style.display = 'none';  
    var data = {};
    data.userid = sessionStorage.getItem('userID');
    data.cancelled = true;
    $.post('http://127.0.0.1:8000/DDS_Server/predict', JSON.stringify(data), 
    function(data){})
}