document.getElementById('confirm_payment').addEventListener("click",sendConfirmPayment)


function sendConfirmPayment(){
    console.log("hello");
    var data = {};
    data.userid = sessionStorage.getItem('userID');
    var firstname = document.querySelector('#fname').value;
    var email = document.querySelector('#email').value;
    var addr = document.querySelector('#adr').value;
    var city = document.querySelector('#city').value;
    var state = document.querySelector('#state').value;
    var zip = document.querySelector('#zip').value;

    var cname = document.querySelector('#cname').value;
    var ccnum = document.querySelector('#ccnum').value;
    
    var expmonth = document.querySelector('#expmonth').value;
    var expyear = document.querySelector('#expyear').value;
    var cvv = document.querySelector('#cvv').value;

    if (firstname && email && addr && city && state && zip && cname && ccnum && expmonth && expyear && cvv){
        data.ccnum = ccnum;
        fetch('http://127.0.0.1:8000/DDS_Server/subscribe', {
            method: 'POST', // or 'PUT'
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
          })
            .then((response) => response.json())
            .then((data) => {
              var resp = String(data.msg);
              if (resp == "Success") {
                sessionStorage.setItem('subscribed', 'true');
                window.location.replace('./accountpage.html');
              }
              else {
                document.getElementById('error').innerHTML = "You are already subscribed";
              }
            })
            .catch((error) => {
              console.error('Error:', error);
        });
        
    }
    else{
        document.getElementById('error').innerHTML = "Please fill out every field!";
    }
}