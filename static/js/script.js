let medicamentList = [];
function handleAjouterMedicament(event) {

    let medicamentName = document.getElementById('medicament-name').value;
    let medicamentQuantity = document.getElementById('medicament-quantity').value;
    if (/^ *$/.test(medicamentName)) {
        alert("Le nom du médicament ne peut pas être vide.");
        return;
    }
    if (medicamentName.length < 3) {
        alert("Le nom du médicament doit contenir au moins 3 caractères.");
        return;
    }
    if (medicamentQuantity <= 0) {
        alert("La quantité doit être supérieure à zéro.");
        return;
    }
    const medicament = {
        name: medicamentName,
        quantity: medicamentQuantity
    };
    medicamentList.push(medicament);
    handleRemplirTableau();

}


function handleRemplirTableau() {
    let tbody = document.getElementById('medicament-list');
    tbody.innerHTML = '';
    medicamentList.forEach(medicament => {
        tbody.innerHTML += 
            `<tr>
                <td>${medicament.name}</td>
                <td>${medicament.quantity}</td>
                <td>
                    <div class="action-icons" onclick="handleSupprimerMedicament(${medicamentList.indexOf(medicament)})">
                        <img src="/static/images/supprimer.png" alt="">
                    </div>
                </td>
            </tr>`;
    });
}


function handleSupprimerMedicament(index) {
    medicamentList.splice(index, 1);
    handleRemplirTableau();
}

document.getElementById('ordonnance-form').addEventListener('submit', function(event) {
    let hiddenInput = document.getElementById('medicaments-json');
    if (!hiddenInput) {
        hiddenInput = document.createElement('input');
        hiddenInput.type = 'hidden';
        hiddenInput.name = 'medicaments';
        hiddenInput.id = 'medicaments-json';
        this.appendChild(hiddenInput);
    }
    hiddenInput.value = JSON.stringify(medicamentList);
    
    if (medicamentList.length == 0) {
        event.preventDefault();
        alert("Veuillez ajouter au moins un médicament avant de générer l'ordonnance.");
        return;
    }
});