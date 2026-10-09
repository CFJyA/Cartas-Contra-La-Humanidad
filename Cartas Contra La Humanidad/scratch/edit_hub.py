import re
with open('Hubs/GameHub.cs', 'r', encoding='utf-8') as f:
    code = f.read()

target = r'// New player trying to join.*?if \(room\.State != "Lobby"\)[\s\r\n]*\{[\s\r\n]*return new \{ success = false, message = "gameInProgress" \};[\s\r\n]*\}'
replacement = '''// New player joining mid-game -> add as spectator
                bool isSpectator = room.State != "Lobby";'''
code = re.sub(target, replacement, code, flags=re.DOTALL)

target2 = r'// New player joining lobby[\s\r\n]*player = new Player[\s\r\n]*\{[\s\r\n]*Id = Guid\.NewGuid\(\)\.ToString\("N"\),[\s\r\n]*ConnectionId = Context\.ConnectionId,[\s\r\n]*Name = string\.IsNullOrWhiteSpace\(playerName\) \? \$"Jugador \{room\.Players\.Count \+ 1\}" : playerName\.Trim\(\),[\s\r\n]*Avatar = string\.IsNullOrWhiteSpace\(avatar\) \? ".*?" : avatar,[\s\r\n]*IsConnected = true[\s\r\n]*\};'
replacement2 = '''// New player joining
                player = new Player
                {
                    Id = Guid.NewGuid().ToString("N"),
                    ConnectionId = Context.ConnectionId,
                    Name = string.IsNullOrWhiteSpace(playerName) ? $"Jugador {room.Players.Count + 1}" : playerName.Trim(),
                    Avatar = string.IsNullOrWhiteSpace(avatar) ? "🥷" : avatar,
                    IsConnected = true,
                    IsSpectator = isSpectator
                };'''

code = re.sub(target2, replacement2, code, flags=re.DOTALL)

with open('Hubs/GameHub.cs', 'w', encoding='utf-8') as f:
    f.write(code)
print('Updated GameHub.cs')
