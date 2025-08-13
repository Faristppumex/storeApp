from flask import Blueprint

chat_bp = Blueprint('chat',__name__)

@chat_bp.route('/chat')
def chat_page():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Simple WebSocket Chat</title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.6.0/socket.io.js"></script>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                margin: 20px; 
                background-color: #f5f5f5;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: white;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            #messages { 
                height: 400px; 
                border: 1px solid #ddd; 
                overflow-y: scroll; 
                padding: 15px; 
                margin-bottom: 15px; 
                background: #fafafa;
                border-radius: 5px;
            }
            #messageInput { 
                width: 70%; 
                padding: 12px; 
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 14px;
            }
            button { 
                padding: 12px 20px; 
                background: #007bff; 
                color: white; 
                border: none; 
                cursor: pointer; 
                border-radius: 5px;
                font-size: 14px;
                margin-left: 10px;
            }
            button:hover {
                background: #0056b3;
            }
            .message { 
                margin: 8px 0; 
                padding: 8px 12px; 
                background: white; 
                border-radius: 8px;
                border-left: 3px solid #007bff;
            }
            .username { 
                font-weight: bold; 
                color: #007bff; 
            }
            .timestamp { 
                font-size: 0.8em; 
                color: #666; 
                float: right;
            }
            .system-message {
                background: #e8f4fd;
                border-left: 3px solid #17a2b8;
                font-style: italic;
                color: #666;
            }
            .username-section {
                margin-bottom: 20px;
                padding: 15px;
                background: #f8f9fa;
                border-radius: 5px;
            }
            .status {
                padding: 10px;
                margin: 10px 0;
                border-radius: 5px;
                text-align: center;
            }
            .connected {
                background: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
            }
            .disconnected {
                background: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>🚀 WebSocket Chat Room</h2>
            
            <div id="connectionStatus" class="status disconnected">
                Connecting to server...
            </div>
            
            <div class="username-section">
                <input type="text" id="usernameInput" placeholder="Enter your name" style="padding: 8px; margin-right: 10px; border: 1px solid #ddd; border-radius: 5px;">
                <button onclick="setUsername()">Set Name</button>
                <span id="currentUser" style="margin-left: 15px; font-weight: bold;"></span>
            </div>
            
            <div id="messages"></div>
            
            <div style="margin-top: 15px;">
                <input type="text" id="messageInput" placeholder="Type a message..." maxlength="500">
                <button onclick="sendMessage()">Send</button>
            </div>
            
            <div style="margin-top: 10px; color: #666; font-size: 12px;">
                Press Enter to send messages
            </div>
        </div>
        
        <script>
            const socket = io();
            let username = 'Anonymous';
            let isConnected = false;
            
            // Connection events
            socket.on('connect', function() {
                console.log('Connected to server');
                isConnected = true;
                updateConnectionStatus('Connected to chat server', 'connected');
                addSystemMessage('✅ Connected to chat server');
            });
            
            socket.on('disconnect', function() {
                console.log('Disconnected from server');
                isConnected = false;
                updateConnectionStatus('Disconnected from server', 'disconnected');
                addSystemMessage('❌ Disconnected from chat server');
            });
            
            socket.on('connect_error', function(error) {
                console.log('Connection error:', error);
                updateConnectionStatus('Connection failed', 'disconnected');
            });
            
            // Message events
            socket.on('message', function(data) {
                console.log('Message received:', data);
                addMessage(data.username, data.message, data.timestamp);
            });
            
            socket.on('user_joined', function(data) {
                addSystemMessage('👋 ' + data.username + ' joined the chat');
            });
            
            socket.on('user_left', function(data) {
                addSystemMessage('👋 ' + data.username + ' left the chat');
            });
            
            // Functions
            function updateConnectionStatus(message, status) {
                const statusDiv = document.getElementById('connectionStatus');
                statusDiv.textContent = message;
                statusDiv.className = 'status ' + status;
            }
            
            function setUsername() {
                const input = document.getElementById('usernameInput');
                if (input.value.trim()) {
                    username = input.value.trim();
                    socket.emit('set_username', {username: username});
                    
                    // Update UI
                    document.getElementById('currentUser').textContent = 'Logged in as: ' + username;
                    input.style.display = 'none';
                    input.nextElementSibling.style.display = 'none';
                    
                    // Focus on message input
                    document.getElementById('messageInput').focus();
                }
            }
            
            function sendMessage() {
                const input = document.getElementById('messageInput');
                const message = input.value.trim();
                
                if (message && isConnected) {
                    console.log('Sending message:', message);
                    socket.emit('send_message', {
                        username: username,
                        message: message
                    });
                    input.value = '';
                } else if (!isConnected) {
                    addSystemMessage('❌ Cannot send message: Not connected to server');
                }
            }
            
            function addMessage(user, message, timestamp) {
                const div = document.createElement('div');
                div.className = 'message';
                div.innerHTML = `
                    <span class="timestamp">[${timestamp}]</span>
                    <span class="username">${escapeHtml(user)}:</span> ${escapeHtml(message)}
                `;
                document.getElementById('messages').appendChild(div);
                scrollToBottom();
            }
            
            function addSystemMessage(message) {
                const div = document.createElement('div');
                div.className = 'message system-message';
                div.innerHTML = escapeHtml(message);
                document.getElementById('messages').appendChild(div);
                scrollToBottom();
            }
            
            function scrollToBottom() {
                const messages = document.getElementById('messages');
                messages.scrollTop = messages.scrollHeight;
            }
            
            function escapeHtml(text) {
                const div = document.createElement('div');
                div.textContent = text;
                return div.innerHTML;
            }
            
            // Enter key support
            document.getElementById('messageInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });
            
            document.getElementById('usernameInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    setUsername();
                }
            });
            
            // Auto-focus on username input when page loads
            window.onload = function() {
                document.getElementById('usernameInput').focus();
            };
        </script>
    </body>
    </html>
    '''