
document.getElementById("restart-button").addEventListener("click", async function() {
    event.preventDefault()
try {
    
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const formData = new FormData();
    formData.append('csrfmiddlewaretoken', csrfToken);


    const response = await fetch("/reset_game/", {
    method: "POST",
    headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': csrfToken // Include CSRF token in headers
    },
    body: formData,
    });
    
    if (response.ok) {
        console.log("Reloading the page...");
        window.location.reload();
        
    } 
}catch (error) {
    console.error("Error:", error);
}
});