// Create a new WebSocket connection to our endpoint
const ws = new WebSocket('ws://127.0.0.1:8000/ws/video_chat/');

// Event listener for when the connection is opened
ws.onopen = (event) => {
    console.log('WebSocket connection opened:', event);
    // Send a message after a short delay
    setTimeout(() => {
        ws.send(JSON.stringify({ 'message': 'Hello from the browser!' }));
    }, 1000);
};

// Event listener for when a message is received from the server
ws.onmessage = (event) => {
    console.log('Message from server:', event.data);
};

// Event listener for when the connection is closed
ws.onclose = (event) => {
    console.log('WebSocket connection closed:', event);
};

// Event listener for errors
ws.onerror = (error) => {
    console.error('WebSocket error:', error);
};

