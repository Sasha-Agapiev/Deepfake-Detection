document.getElementById('cancel_sub').addEventListener("click", openCancelSubscriptionForm);
document.getElementById('toggle_warnings').addEventListener("click", toggle_warnings);
document.getElementById('Keep_Sub_Button').addEventListener("click", keepSubButtonForm);
document.getElementById('Cancel_Sub_Button').addEventListener("click", sendCancelSubscription);
document.addEventListener("DOMContentLoaded", function() {

    //firstname
    var firstname = sessionStorage.getItem('firstname');
    document.getElementById('firstname').innerHTML = '<b> Welcome, </b><br>' + firstname +'</h1>';
    
    //account type
    var subscribed = sessionStorage.getItem('subscribed');
    var accounttype = "BASIC";

    if (subscribed == 'true') {
        accounttype = "PREMIUM"
    }
    document.getElementById('accounttype').innerHTML = '<b>Account Type:</b></h5><h5>' + accounttype+ '</h5>';

    //predictions left
    var num_left = sessionStorage.getItem('predictons_left');
    var predictons_left;
    if (subscribed == 'true') {
        predictons_left = "UNLIMITED";
    }
    else {
        predictons_left = num_left;
    }
    document.getElementById('predictions_left').innerHTML = '<b>Predictions Remaining:</b></h5><h5>' + predictons_left + '</h5>';

    //user reports
    var reports = sessionStorage.getItem('user_reports');
    var reports_arr = reports.split(",");
    console.log(reports_arr)
    var text = '<br>';
    var date;
    var site;
    var a_r;
    for (let i = 0; i+2 <= reports_arr.length; i+=3) {
        date = reports_arr[i];
        site = reports_arr[i+1];
        a_r = reports_arr[i+2];
        text += "<b>Date Reported:</b> " + date  + " <b>Domain Name:</b> " + site + " <b>Flag:</b> " + a_r +  "<br>";
    }
    document.getElementById('userreports').innerHTML =  '<b>Websites You\'ve Reported</b></h5>'+ text + '</h5>';
    
    
    //subscription status
    var status;

    if (subscribed == 'false') {
        status = "You are not currently subscribed";
        document.getElementById('subscriptionprompt').style.visibility = "visible";
        document.getElementById('cancel_sub').style.visibility = "hidden";
        
    }
    else {
        var days_left = sessionStorage.getItem('days_left')
        if (days_left == 1){
            status =  sessionStorage.getItem('days_left') + " day left";
        }
        else{
            status =  sessionStorage.getItem('days_left') + " days left";
        }
        document.getElementById('subscriptionprompt').style.visibility = "hidden";
        document.getElementById('cancel_sub').style.visibility = "visible";
    }
    document.getElementById('status').innerHTML = '<b>Subscription Status:</b></h5><br>' + status;
   
    //alert
    var reminded = sessionStorage.getItem('reminded');
    if (subscribed == "true" && days_left <= 7 && reminded == "false"){
        chrome.notifications.create(
            {
                type: "basic",
                iconUrl: "images/dds_icon.png",
                title: "Subscription Renewal",
                message: "Your subscription is expiring in less than 7 days! Renew with us to continue detecting Deepfakes",
                silent: false
            },
            () => { });
        sendReminded();
    }
  });


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
    
    document.getElementById('areyousure').style.visibility = "hidden";
    document.getElementById('Cancel_Sub_Button').style.display = 'none';
    document.getElementById('Keep_Sub_Button').style.display = 'none';  
    var data = {};
    data.userid = sessionStorage.getItem('userID');
    data.request = "unsubscribe";
    fetch('http://127.0.0.1:8000/DDS_Server/user_update', {
        method: 'POST', // or 'PUT'
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })
        .then((data) => {
          console.log('Success:', data);
          document.getElementById('cancel_sub_status').innerHTML = "Your DDS subscription has been successfully terminated.";
          sessionStorage.setItem('subscribed', 'false');
          window.location.replace('./accountpage.html');

        })
        .catch((error) => {
          console.error('Error:', error);
    });
}

function sendReminded(){
    
    var data = {};
    data.userid = sessionStorage.getItem('userID');
    data.request = "reminded";
    fetch('http://127.0.0.1:8000/DDS_Server/user_update', {
        method: 'POST', // or 'PUT'
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })
        .then((data) => {
          console.log('Success:', data);
          sessionStorage.setItem('reminded', 'true');
        })
        .catch((error) => {
          console.error('Error:', error);
    });
}