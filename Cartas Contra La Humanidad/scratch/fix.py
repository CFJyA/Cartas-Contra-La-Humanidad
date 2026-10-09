import os
import re

def fix_player():
    filepath = 'Models/Player.cs'
    with open(filepath, 'rb') as f:
        content = f.read()
    
    content = content.decode('utf-8', errors='ignore')
    content = re.sub(r'public string Avatar \{ get; set; \} = ".*?";', 'public string Avatar { get; set; } = "😎";', content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def fix_manager():
    filepath = 'Services/GameManager.cs'
    with open(filepath, 'rb') as f:
        content_bytes = f.read()
    
    # Try decoding
    try:
        content = content_bytes.decode('utf-8')
    except UnicodeDecodeError:
        content = content_bytes.decode('latin1')
        try:
            content = content.encode('latin1').decode('utf-8')
        except:
            pass
    
    # Fix BotNames
    content = re.sub(r'"El Bot T.*?xico"', '"El Bot Tóxico"', content)
    content = re.sub(r'"T.*?a Pikachu"', '"Tía Pikachu"', content)
    
    # Fix avatars
    content = re.sub(r'string\[\] botAvatars = \[.*?\];', 'string[] botAvatars = ["🤖", "👽", "👾", "🤡", "👻", "💀"];', content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_player()
fix_manager()
