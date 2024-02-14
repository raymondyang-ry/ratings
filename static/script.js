const leftButton = document.getElementById('left-button');
const rightButton = document.getElementById('right-button');

function updateLeaderboard(leaderboardData) {
    const leaderboardDiv = document.getElementById('leaderboard');
    leaderboardDiv.innerHTML = '<h2>Leaderboard</h2>'; // Clear existing list

    leaderboardData.forEach(item => {
        const listItem = document.createElement('p');
        listItem.textContent = `${item.choice}: ${item.count}`;
        leaderboardDiv.appendChild(listItem);
    });
}

leftButton.addEventListener('click', () => {
    fetch('/click/left')
        .then(response => response.json())
        .then(data => {
            leftButton.textContent = data.left_text;
            rightButton.textContent = data.right_text;
            updateLeaderboard(data.leaderboard);
            console.log(data.leaderboard);
        })
        .catch(error => console.error("Error updating buttons:", error)); // Error handling
           
});

rightButton.addEventListener('click', () => {
    fetch('/click/right')
        .then(response => response.json())
        .then(data => {
            leftButton.textContent = data.left_text;
            rightButton.textContent = data.right_text;
            updateLeaderboard(data.leaderboard);
            console.log(data.leaderboard);
        })
        .catch(error => console.error("Error updating buttons:", error)); // Error handling
});
