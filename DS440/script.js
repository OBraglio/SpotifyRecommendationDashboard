function printInput(event, inputType) {
    if (event.key === "Enter") {
        var inputElement = document.getElementById(inputType);
        var inputValue = inputElement.value;
        var valueElement = document.getElementById(inputType + '-value');
        var listElement = document.getElementById(inputType + '-list');

        // Create a new list item for the input value
        var listItem = document.createElement('li');
        
        // Create span for the input value
        var valueSpan = document.createElement('span');
        valueSpan.textContent = inputValue;

        // Create remove button
        var removeButton = document.createElement('button');
        removeButton.textContent = '❌'; // Red X emoji
        removeButton.classList.add('remove-button'); // Add class to style the button
        removeButton.onclick = function() {
            listItem.remove(); // Remove the list item when the button is clicked
        };

        // Append span and button to list item
        listItem.appendChild(valueSpan);
        listItem.appendChild(removeButton);

        // Append the new input value to the list
        listElement.appendChild(listItem);

        inputElement.value = ""; // Clear the input box
    }
}


function calculate() {
    var songList = getValues('song-list');
    var artistList = getValues('artist-list');
    var genreList = getValues('genre-list');

    var data = {
        'songs': songList,
        'artists': artistList,
        'genres': genreList
    };

    // Send the data to the server
    fetch('http://localhost:8000/generate_playlist', { // Adjust the URL if needed
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Response from server:', data);
        // Handle the response as needed
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function getValues(listId) {
    var values = [];
    var listItems = document.getElementById(listId).getElementsByTagName('li');
    for (var i = 0; i < listItems.length; i++) {
        values.push(listItems[i].getElementsByTagName('span')[0].textContent);
    }
    return values;
}