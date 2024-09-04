$(document).ready(function() {
    let taskId = null;
    const token = localStorage.getItem('access_token');
    const startButton = document.getElementById('startButton');
    let socket = null;

    function redirectToLogin() {
        localStorage.clear();
        window.location.href = '/login';
    }

    function track_task_status() {
        fetch('/api/task_status/', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            }).then(response => response.json())
            .then(data => {
                updateButtonState(data.completed)
            })
            .catch(error => {
                console.error('Error', error);
            });
    }

    function validateToken() {
        if (token) {
            fetch('/api/token/verify/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        token: token
                    }),
                })
                .then(response => {
                    if (response.status === 200) {
                        console.log('Token is valid');
                    } else {
                        window.location.href = '/login';
                    }
                })
                .catch(error => {
                    console.error('Error verifying token:', error);
                    window.location.href = '/login';
                });
        } else {
            window.location.href = '/login';
        }
    }

    function startProcess() {
        fetch('/api/process_data/', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`, // Corrected header syntax
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                taskId = data.task_id;
                initializeWebSocket();
            })
            .catch(error => {
                console.error('Error starting task:', error);
            });
    }

    function initializeWebSocket() {
        if (!taskId) return;

        socket = new WebSocket('ws://' + window.location.host + '/ws/consumer_path/' + taskId + '/');

        socket.onopen = function(event) {
            socket.send(JSON.stringify({
                'action': 'check_task_status',
                'task_id': taskId
            }));
        };

        socket.onmessage = function(event) {
            const data = JSON.parse(event.data);
            if (data.action === 'check_task_status') {
                updateButtonState(data.ready)
            }

        };

        socket.onclose = function(event) {
            console.log('WebSocket connection closed:', event);
        };
    }

    function updateButtonState(isReady) {
        startButton.disabled = !isReady;
    }

    document.addEventListener('DOMContentLoaded', function() {
        validateToken();
        track_task_status();
    });

    $('#startButton').on('click', startProcess);
    $('#logOutButton').on('click', redirectToLogin);
});