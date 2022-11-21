const toggle_warnings_button = document.getElementById('toggle_warnings');
const cancel_subscription_button = document.getElementById('cancel_sub')

toggle_warnings_button.addEventListener("click", toggle_warnings);
if(cancel_subscription_button){
    cancel_subscription_button.addEventListener("click", confirm_cancel_subscription);
}

// toggles warnings button text (on/off) on user click 
function toggle_warnings(){
    var elem = document.getElementById("toggle_warnings");
    if (elem.value=="Currently On") elem.value = "Currently Off";
    else elem.value = "Currently On"
}

function confirm_cancel_subscription(){
    confirm("Are you sure you want to end your current subscription?");
}
