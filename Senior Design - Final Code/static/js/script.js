function displayFileName() {
    var input = document.getElementById('input-file');
    var filenameDisplay = document.getElementById('filename');

    if (input.files.length > 0) {
        filenameDisplay.textContent = input.files[0].name;
    } else {
        filenameDisplay.textContent = 'Drag and Drop .txt file or click to browse';
    }
}

function startCountdown() {
    let seconds = 3;
    const countdownTextElement = document.getElementById('CountDownText');
    const countdownDiv = document.getElementById('CountDown');

    if (countdownTextElement && countdownDiv) {
        countdownDiv.style.display = 'block';

        function updateCountdown() {
            countdownTextElement.innerText = "Processing...";
            seconds--;

            if (seconds < 0) {
                location.reload();
            } else {
                setTimeout(updateCountdown, 1000);
            }
        }

        updateCountdown();
    } else {
        console.error('Countdown elements not found');
    }
}

function startCountdown2() {
    let seconds = 6;
    const countdownTextElement = document.getElementById('CountDownText');
    const countdownDiv = document.getElementById('CountDown');

    if (countdownTextElement && countdownDiv) {
        countdownDiv.style.display = 'block';

        function updateCountdown() {
            countdownTextElement.innerText = "Processing...";
            seconds--;

            if (seconds < 0) {
                location.reload();
            } else {
                setTimeout(updateCountdown, 1000);
            }
        }

        updateCountdown();
    } else {
        console.error('Countdown elements not found');
    }
}

document.addEventListener('DOMContentLoaded', function () {
    var submitButton = document.getElementById('submit');
    submitButton.addEventListener('click', function () {
        var input = document.getElementById('input-file');

        if (input.files.length > 0) {
            var formData = new FormData();
            formData.append('file', input.files[0]);

            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/CheckEmailUpload/upload', true);
            xhr.onload = function () {
                if (xhr.status === 200) {
                    console.log('File uploaded successfully:', xhr.responseText);
                } else {
                    console.error('Error uploading file:', xhr.statusText);
                }
            };

            xhr.send(formData);
        } else {
            alert('Please select a file before submitting.');
        }
    });
});

document.getElementById('Submit').addEventListener('click', function() {
    const content = document.getElementById('content').textContent;
    const header = document.getElementById('header').textContent;

    fetch('/CheckEmailManual', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ Content: content, Header: header })
    })
});