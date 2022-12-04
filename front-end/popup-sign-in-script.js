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
    url = 'http://127.0.0.1:8000/DDS_Server/login'

    const email = document.querySelector('#email').value;
    const pass = document.querySelector('#password').value;

    var data = {};
    data.email = email;
    data.password = pass;
    console.log(email)
    console.log(pass)

    if (email && pass) {
        $.post(url,JSON.stringify(data),
        function(data, textStatus, jqXHR)
        {
            if (data != "FAIL") {
                sessionStorage.setItem('userID', data.userid);
                window.location.replace('./homepage.html');
            }
        })
        
    } else {
        document.querySelector('#email').placeholder = "Enter an email.";
        document.querySelector('#password').placeholder = "Enter a password.";
        document.querySelector('#email').style.backgroundColor = 'red';
        document.querySelector('#password').style.backgroundColor = 'red';
        document.querySelector('#email').classList.add('white_placeholder');
        document.querySelector('#password').classList.add('white_placeholder');
    }
});