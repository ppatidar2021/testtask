$(document).ready(function() {
    const token = localStorage.getItem('access_token');

    function redirectToLogin() {
        localStorage.clear();
        window.location.href = '/login';
    }

    function validateToken() {
        if (!token) {
            redirectToLogin();
            return;
        }

        fetch('/api/token/verify/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ token }),
        })
        .then(response => {
            if (response.ok) {
                console.log('Token is valid');
                window.location.href = '/';
            } else {
                redirectToLogin();
            }
        })
        .catch(error => {
            console.error('Error verifying token:', error);
            redirectToLogin();
        });
    }

    function handleLogin(event) {
        event.preventDefault();
        const submitUrl = $('#login-form').find('button').data('url');

        $.ajax({
            url: '/api/token/',
            type: 'POST',
            data: {
                username: $('#username').val(),
                password: $('#password').val(),
            },
            success: function(data) {
                localStorage.setItem('access_token', data.access);
                window.location.href = submitUrl;
            },
            error: function(xhr) {
                $('#message').text('Invalid username or password');
            }
        });
    }

    document.addEventListener('DOMContentLoaded', function() {
        validateToken();
    });

    $('#login-form').on('submit', handleLogin);
});

