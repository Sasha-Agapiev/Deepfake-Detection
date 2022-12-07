const button = document.querySelector('button');

button.addEventListener('mouseover', () => {
    button.style.backgroundColor = 'black';
    button.style.color = 'white';
    button.style.transform = 'scale(1.3)';

    document.querySelector('form').style.backgroundColor = '#900c94';

    document.querySelectorAll('input').forEach(input => {
        input.style.backgroundColor = 'black';
        input.style.color = 'white';
        input.style.transform = 'scale(0.7)';
    });
});

button.addEventListener('mouseleave', () => {
    button.style.backgroundColor = '#f5c2e0';
    button.style.color = 'black';
    button.style.transform = 'scale(1)';

    document.querySelector('form').style.backgroundColor = '#900c94';

    document.querySelector('#email').classList.remove('white_placeholder');
    document.querySelector('#password').classList.remove('white_placeholder');

    document.querySelectorAll('input').forEach(input => {
        input.style.backgroundColor = 'white';
        input.style.color = 'black';
        input.style.transform = 'scale(1)';
    });
});

document.querySelector('form').addEventListener('submit', event => {
    event.preventDefault();
    url = 'http://127.0.0.1:8000/DDS_Server/signup'

    const fname = document.querySelector("#firstname").value;
    const lname = document.querySelector("#lastname").value;
    const email = document.querySelector('#email').value;
    const pass = document.querySelector('#password').value;
    const confirmpass = document.querySelector("#confirmpassword").value;

    if (email && pass && fname && lname && confirmpass) {
        if (pass != confirmpass) {
            document.getElementById('warning').innerHTML = "Passwords do not match!";
        }
        else {
            var data = {};
            data.firstname = fname;
            data.lastname = lname;
            data.email = email;
            data.password = pass;

            console.log(data)
            fetch(url, {
                method: 'POST', // or 'PUT'
                headers: {
                  'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
                })
                .then((data) => {
                  console.log('Success:', data);
                  if (data != "FAIL") {
                    window.location.replace('./signin-popup.html');
                  }
                })
                .catch((error) => {
                  console.error('Error:', error);
            });
        }
    } else {
        document.getElementById('warning').innerHTML = "Please fill out every field!";
    }
});