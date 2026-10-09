import re
with open('wwwroot/js/game.js', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update JoinRoom success check
target_join = r'if \(res\.message === \'gameInProgress\'\) \{[\s\r\n]*// Game already started.*?showGameInProgressOverlay\(code\);[\s\r\n]*\}'
replacement_join = '''if (res.message === 'gameInProgress') {
                    // Game already started
                    sessionStorage.removeItem('cah_active_room');
                    showGameInProgressOverlay(code);
                }'''
# Actually we removed 'gameInProgress' from server, so res.success will be true!
# So we need to check if the player is in the players list as a spectator.
# Let's modify renderRoom.

target_render = r'function renderRoom\(room\) \{[\s\r\n]*if \(\!room\) \{[\s\r\n]*showScreen\(\'welcome\'\);[\s\r\n]*return;[\s\r\n]*\}'
replacement_render = '''function renderRoom(room) {
        if (!room) {
            showScreen('welcome');
            return;
        }

        // Check if spectator
        const me = room.players.find(p => p.id === myPlayerId);
        if (me && me.isSpectator) {
            showGameInProgressOverlay(room.code);
            return;
        } else {
            const overlay = document.getElementById('overlay-game-in-progress');
            if (overlay) overlay.style.display = 'none';
        }'''

code = re.sub(target_render, replacement_render, code, flags=re.DOTALL)

with open('wwwroot/js/game.js', 'w', encoding='utf-8') as f:
    f.write(code)
print('Updated game.js')
