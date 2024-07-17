document.querySelector('.enviar').addEventListener('click', () => {
    const email = document.getElementById('email').value.trim();
    const mensaje = document.getElementById('mensaje').value.trim();

    if (email === '' || mensaje === '') {
        alert('Por favor, ingresa tu email y mensaje antes de enviar.');
        return;
    }

    // Enviar los datos al backend usando fetch
    fetch('http://localhost:5000/guardar_mensaje', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, mensaje })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Ocurrió un error al guardar el mensaje.');
    });
});