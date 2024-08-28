// Beispielhafte Datenstruktur für Spieler und Bußgelder
let players = [
    { id: 1, name: "Max Mustermann", position: "Stürmer", totalFines: 0 },
    { id: 2, name: "Erika Musterfrau", position: "Verteidiger", totalFines: 0 }
];

let fines = [];

// Funktion, um die Spieler in der Tabelle anzuzeigen
function loadPlayerTable() {
    let playerTable = document.getElementById('playerTable');
    playerTable.innerHTML = '';
    players.forEach(player => {
        playerTable.innerHTML += `
            <tr>
                <td>${player.name}</td>
                <td>${player.position}</td>
                <td>${player.totalFines.toFixed(2)}</td>
            </tr>
        `;
    });
}

// Funktion, um das Spieler-Dropdown zu füllen
function loadPlayerDropdown() {
    let playerDropdown = document.getElementById('spieler');
    playerDropdown.innerHTML = '';
    players.forEach(player => {
        playerDropdown.innerHTML += `<option value="${player.id}">${player.name}</option>`;
    });
}

// Funktion, um ein Bußgeld hinzuzufügen
document.getElementById('fineForm').addEventListener('submit', function(e) {
    e.preventDefault();

    let playerId = parseInt(document.getElementById('spieler').value);
    let offense = document.getElementById('vergehen').value;
    let amount = parseFloat(document.getElementById('betrag').value);
    let date = new Date().toLocaleDateString();

    fines.push({ playerId, offense, amount, date });

    // Bußgeld dem entsprechenden Spieler hinzufügen
    let player = players.find(p => p.id === playerId);
    player.totalFines += amount;

    alert('Bußgeld hinzugefügt!');
    loadPlayerTable();
    loadFineTable();
});

// Funktion, um die Bußgelder in der Übersicht anzuzeigen
function loadFineTable() {
    let fineTable = document.getElementById('fineTable');
    fineTable.innerHTML = '';
    fines.forEach(fine => {
        let player = players.find(p => p.id === fine.playerId);
        fineTable.innerHTML += `
            <tr>
                <td>${player.name}</td>
                <td>${fine.offense}</td>
                <td>${fine.amount.toFixed(2)}</td>
                <td>${fine.date}</td>
            </tr>
        `;
    });
}

// Initiale Daten laden, wenn die Seite geladen wird
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('playerTable')) {
        loadPlayerTable();
    }
    if (document.getElementById('spieler')) {
        loadPlayerDropdown();
    }
    if (document.getElementById('fineTable')) {
        loadFineTable();
    }
});
