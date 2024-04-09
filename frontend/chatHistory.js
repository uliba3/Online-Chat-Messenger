function returnMessages(roomName) {
    fetch('../data.json')
        .then(response => response.json())
        .then(data => {
            return data[roomName]['messages'];
        })
        .catch(error => {
            console.error('Error fetching JSON file:', error);
        });
}

export { returnMessages };