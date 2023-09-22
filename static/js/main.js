

// Function to show the modal
function showPlayerModal(playerImage, playerMessage,playerName) {
    const modal = document.getElementById("details");
    const playerMessageElement = document.getElementById("playerMessage");
    const playerImageElement = document.getElementById("playerImage");
    const playerImageName = document.getElementById("playerName");



    playerImageElement.src = playerImage;
    playerImageName.textContent = playerName;
    playerMessageElement.textContent = playerMessage;

    modal.style.display = "block";
}
document.getElementById("playGame").addEventListener("click", async function() {
    event.preventDefault()
try {
    var hiddenInput = document.getElementById("hiddenInput");
    if (hiddenInput.value === "False") {
        showPlayerModal("/static/img/guess.jpg",'','')
        fetchDataAndDisplay()
    } else{
        const guess = document.getElementById("guess").value;
    const currentScore = document.getElementById("currentScore").textContent;

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const formData = new FormData();
    formData.append('csrfmiddlewaretoken', csrfToken);
    formData.append('currentScore', currentScore);

    formData.append('guess', guess);

    const response = await fetch("/start_game/", {
    method: "POST",
    headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': csrfToken // Include CSRF token in headers
    },
    body: formData,
    });
    
    if (response.ok) {
    const data = await response.json();
    // const data = JSON.parse(jsonObject);
    const newScore = data.score;

    document.getElementById("currentScore").textContent = newScore;
    document.getElementById("hiddenInput").value = 'False';
    document.getElementById("playGame").textContent = 'Continue';


    if (data.win === true) {
            // Show the modal with player information
            showPlayerModal(data.player_photo_url, data.message,data.player_name);
        }

    } else {
    console.error("Error fetching data:", response.status);
    }
    }
    
} catch (error) {
    console.error("Error:", error);
}
});

// document.getElementById("loadDataButton").addEventListener("click", async function() {
async function fetchDataAndDisplay() {
    event.preventDefault()
    try {
    const selectedLevel = document.getElementById("level").value;
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const formData = new FormData();
    formData.append('csrfmiddlewaretoken', csrfToken);
    formData.append('level', selectedLevel);

    const response = await fetch("/get_player_data/", {
        method: "POST",
        headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': csrfToken // Include CSRF token in headers
        },
        body: formData,
    });
    
    if (response.ok) {
    const jsonObject = await response.json();
    const data = JSON.parse(jsonObject);
    const table = document.getElementById("playerTable");
    table.innerHTML = "";

    const headerRow = document.createElement("tr");
    for (const key in data[0]) {
    const th = document.createElement("th");
    th.textContent = key;
    headerRow.appendChild(th);

    }
    table.appendChild(headerRow);

    data.forEach(player => {
    const row = document.createElement("tr");
    for (const key in player) {
        const cell = document.createElement("td");
        cell.textContent = player[key];
        row.appendChild(cell);
    }
    table.appendChild(row);
    });

        document.getElementById("guessCard").style.display = "block";
        document.getElementById("tableCard").style.display = "block";
        document.getElementById("hiddenInput").value = 'True';

        document.getElementById("playGame").textContent = 'Submit';

} else {
    console.error("Error fetching data:", response.status);
}
} catch (error) {
console.error("Error:", error);
}
};

