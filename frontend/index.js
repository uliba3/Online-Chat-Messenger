import { returnMessages } from "./chatHistory";

async function showMessages(roomName) {
    try {
        const messages = await returnMessages(roomName);
        let messageList = document.getElementById('chatHistory');
        messageList.innerHTML = JSON.stringify(messages);
    } catch (error) {
        console.error('Error showing messages:', error);
    }
}

document.getElementById('myButton').addEventListener('click', function() {
    let roomName = document.getElementById('roomName').value;
    showMessages(roomName); // Pass the roomName variable, not the string 'roomName'
});
