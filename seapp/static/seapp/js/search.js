document.getElementById('search').addEventListener('input', function() {
    const query = this.value;
    fetch(`?q=${query}`, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        const tableBody = document.querySelector('#candidates-table tbody');
        tableBody.innerHTML = ''; // Limpiar la tabla

        data.candidatos.forEach(persona => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${persona.nombre}</td>
                <td>${persona.apellido}</td>
                <td>${persona.email}</td>
                <td>${persona.telefono}</td>
                <td>${persona.estudios.map(estudio => estudio.carrera).join(', ') || 'No tiene estudios registrados'}</td>
            `;
            tableBody.appendChild(row);
        });
    });
});