const messages = document.querySelector('.v9_22');
const textarea = document.querySelector('.v9_59');
const button = document.querySelector('.v9_17');

button.addEventListener('click', () => {
    const message = textarea.value;
    if (message.trim() === '') return;

    const messageElement = document.createElement('div');
    messageElement.classList.add('message', 'usted');
    messageElement.textContent = message;
    messages.appendChild(messageElement);

    // Enviar el mensaje al backend
    fetch('http://localhost:5000/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        const almaMessageDiv = document.createElement('div');
        almaMessageDiv.classList.add('message', 'ALMA');
        almaMessageDiv.textContent = data.response;
        messages.appendChild(almaMessageDiv);

        // Scroll al final del contenedor de mensajes
        messages.scrollTop = messages.scrollHeight;
    })
    .catch(error => {
        console.error(error);
    });
    textarea.value = '';
});

// Enviar el mensaje al presionar Enter
textarea.addEventListener('keydown', event => {
    if (event.key === 'Enter') {
        button.click();
    }
});