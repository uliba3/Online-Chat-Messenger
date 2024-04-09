const fs = require('fs');

// Write the JSON data to the file
const updateData = (jsonData) => {
    fs.writeFile('./data.json', jsonData, (err) => {
        if (err) {
            console.error('Error updating:', err);
        } else {
            console.log('Data updated successfully!');
        }
    });
};

const readData = () => {
    return JSON.parse(fs.readFileSync('./data.json', 'utf8'));
};

module.exports = {
    updateData,
    readData
};

