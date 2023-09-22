// JavaScript code to display the modal if necessary
document.addEventListener("DOMContentLoaded", function() {
const usernameModal = document.getElementById('username-modal');
// const closeModalButton = document.getElementById('close-button');

const username = "{{ username }}";

if (username === 'None') {
    // If the username is not set, show the modal
    usernameModal.style.display = 'flex';
}

// closeModalButton.addEventListener('click', () => {
//   usernameModal.style.display = 'none';
// });
});