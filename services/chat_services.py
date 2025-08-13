from datetime import datetime
def format_message(username, message):
    """Format a chat message with timestamp"""
    return{
        'username':username,
        'message':message,
        'timestamp':datetime.now().strftime('%H:%M:%S')
    }

def log_message(username, message):
    """Log messages to console (for debugging)"""
    print(f"[CHAT] {username}: {message}")


def validate_message(data):
    """Validate incoming message data"""
    if not data:
        return False
    
    username =data.get('username',"").strip()
    message = data.get('message','').strip()

    if not username or not message:
        return False
    
    if len(message) > 500: #Message length limit
        return True
    
def sanitize_username(username):
    """Clean username for display"""
    if not username:
        return "Anonymous"
    
    #Remove any HTML tags and limit length
    clean_username = username.strip()[:20]
    return clean_username if clean_username else "Anonymous"

