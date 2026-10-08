using Cartas_Contra_La_Humanidad.Models;
using Cartas_Contra_La_Humanidad.Services;
using Microsoft.AspNetCore.SignalR;

namespace Cartas_Contra_La_Humanidad.Hubs;

public class GameHub : Hub
{
    private readonly GameManager _gameManager;

    public GameHub(GameManager gameManager)
    {
        _gameManager = gameManager;
    }

    public async Task<object> CreateRoom(string playerName, string avatar, int targetScore, int timerSeconds, bool randoBot)
    {
        var room = _gameManager.CreateRoom(playerName, avatar, targetScore, timerSeconds, randoBot);
        var host = room.Players.First();
        host.ConnectionId = Context.ConnectionId;

        _gameManager.RegisterConnection(Context.ConnectionId, room.Code, host.Id);
        await Groups.AddToGroupAsync(Context.ConnectionId, room.Code);

        await _gameManager.BroadcastRoomStateAsync(room);

        return new
        {
            success = true,
            roomCode = room.Code,
            playerId = host.Id
        };
    }

    public async Task<object> JoinRoom(string roomCode, string? playerId, string playerName, string avatar)
    {
        if (string.IsNullOrWhiteSpace(roomCode))
        {
            return new { success = false, message = "Código de sala no válido." };
        }

        var room = _gameManager.GetRoom(roomCode);
        if (room == null)
        {
            return new { success = false, message = $"No se encontró la sala con código {roomCode.ToUpperInvariant()}." };
        }

        Player? player = null;

        lock (room.SyncLock)
        {
            if (!string.IsNullOrEmpty(playerId))
            {
                player = room.GetPlayer(playerId);
            }

            if (player != null)
            {
                // Reconnecting existing player — always allowed
                player.ConnectionId = Context.ConnectionId;
                player.IsConnected = true;
                if (!string.IsNullOrWhiteSpace(playerName)) player.Name = playerName.Trim();
                if (!string.IsNullOrWhiteSpace(avatar)) player.Avatar = avatar;
            }
            else
            {
                // New player trying to join — block if game is already active
                if (room.State != "Lobby")
                {
                    return new { success = false, message = "gameInProgress" };
                }

                // New player joining lobby
                player = new Player
                {
                    Id = Guid.NewGuid().ToString("N"),
                    ConnectionId = Context.ConnectionId,
                    Name = string.IsNullOrWhiteSpace(playerName) ? $"Jugador {room.Players.Count + 1}" : playerName.Trim(),
                    Avatar = string.IsNullOrWhiteSpace(avatar) ? "😎" : avatar,
                    IsConnected = true
                };
                room.AddPlayer(player);
            }
        }

        _gameManager.RegisterConnection(Context.ConnectionId, room.Code, player.Id);
        await Groups.AddToGroupAsync(Context.ConnectionId, room.Code);

        await _gameManager.BroadcastRoomStateAsync(room);

        return new
        {
            success = true,
            roomCode = room.Code,
            playerId = player.Id
        };
    }

    public async Task StartGame()
    {
        var info = _gameManager.GetConnectionInfo(Context.ConnectionId);
        if (info == null) return;

        var room = _gameManager.GetRoom(info.Value.roomCode);
        if (room == null) return;

        lock (room.SyncLock)
        {
            var player = room.GetPlayer(info.Value.playerId);
            if (player == null || !player.IsHost) return;
        }

        var whiteCards = _gameManager.GetDefaultWhiteCards();
        var blackCards = _gameManager.GetDefaultBlackCards();

        bool started = room.StartGame(whiteCards, blackCards);
        if (started)
        {
            await _gameManager.BroadcastRoomStateAsync(room);
        }
    }

    public async Task SubmitCards(List<string> cardIds)
    {
        var info = _gameManager.GetConnectionInfo(Context.ConnectionId);
        if (info == null) return;

        var room = _gameManager.GetRoom(info.Value.roomCode);
        if (room == null) return;

        bool success = room.SubmitCards(info.Value.playerId, cardIds);
        if (success)
        {
            await _gameManager.BroadcastRoomStateAsync(room);
        }
    }

    public async Task SelectWinner(string submissionId)
    {
        var info = _gameManager.GetConnectionInfo(Context.ConnectionId);
        if (info == null) return;

        var room = _gameManager.GetRoom(info.Value.roomCode);
        if (room == null) return;

        bool success = room.SelectWinner(info.Value.playerId, submissionId);
        if (success)
        {
            await _gameManager.BroadcastRoomStateAsync(room);
        }
    }

    public async Task NextRound()
    {
        var info = _gameManager.GetConnectionInfo(Context.ConnectionId);
        if (info == null) return;

        var room = _gameManager.GetRoom(info.Value.roomCode);
        if (room == null) return;

        lock (room.SyncLock)
        {
            var player = room.GetPlayer(info.Value.playerId);
            if (player == null) return;

            if (room.State is "RoundResults")
            {
                room.StartNewRound();
            }
            else if (room.State is "GameOver" && player.IsHost)
            {
                var whiteCards = _gameManager.GetDefaultWhiteCards();
                var blackCards = _gameManager.GetDefaultBlackCards();
                room.StartGame(whiteCards, blackCards);
            }
        }

        await _gameManager.BroadcastRoomStateAsync(room);
    }

    public async Task AddBot()
    {
        var info = _gameManager.GetConnectionInfo(Context.ConnectionId);
        if (info == null) return;

        var room = _gameManager.GetRoom(info.Value.roomCode);
        if (room == null) return;

        lock (room.SyncLock)
        {
            var player = room.GetPlayer(info.Value.playerId);
            if (player == null || !player.IsHost) return;
        }

        _gameManager.AddBotToRoom(room);
        await _gameManager.BroadcastRoomStateAsync(room);
    }

    public async Task RemoveBot(string botId)
    {
        var info = _gameManager.GetConnectionInfo(Context.ConnectionId);
        if (info == null) return;

        var room = _gameManager.GetRoom(info.Value.roomCode);
        if (room == null) return;

        lock (room.SyncLock)
        {
            var player = room.GetPlayer(info.Value.playerId);
            if (player == null || !player.IsHost) return;
            room.RemoveBot(botId);
        }

        await _gameManager.BroadcastRoomStateAsync(room);
    }

    /// <summary>
    /// Host kicks a player out of the room. The kicked player receives a "YouWereKicked" event.
    /// </summary>
    public async Task KickPlayer(string targetPlayerId)
    {
        var info = _gameManager.GetConnectionInfo(Context.ConnectionId);
        if (info == null) return;

        var room = _gameManager.GetRoom(info.Value.roomCode);
        if (room == null) return;

        string? targetConnectionId = null;
        bool kicked;

        lock (room.SyncLock)
        {
            var target = room.GetPlayer(targetPlayerId);
            targetConnectionId = target?.ConnectionId;
            kicked = room.KickPlayer(info.Value.playerId, targetPlayerId);
        }

        if (kicked)
        {
            if (!string.IsNullOrEmpty(targetConnectionId))
            {
                await Clients.Client(targetConnectionId).SendAsync("YouWereKicked");
                await Groups.RemoveFromGroupAsync(targetConnectionId, room.Code);
                _gameManager.UnregisterConnection(targetConnectionId);
            }

            await _gameManager.BroadcastRoomStateAsync(room);
        }
    }

    public async Task SendChat(string message)
    {
        if (string.IsNullOrWhiteSpace(message)) return;

        var info = _gameManager.GetConnectionInfo(Context.ConnectionId);
        if (info == null) return;

        var room = _gameManager.GetRoom(info.Value.roomCode);
        if (room == null) return;

        ChatMessage chatMsg;
        lock (room.SyncLock)
        {
            var player = room.GetPlayer(info.Value.playerId);
            if (player == null) return;

            chatMsg = new ChatMessage
            {
                SenderName = player.Name,
                SenderAvatar = player.Avatar,
                Text = message.Trim().Length > 200 ? message.Trim()[..200] : message.Trim(),
                Timestamp = DateTime.UtcNow
            };

            room.ChatMessages.Add(chatMsg);
        }

        await Clients.Group(room.Code).SendAsync("ChatMessageReceived", chatMsg);
    }

    public async Task SendReaction(string emoji)
    {
        if (string.IsNullOrWhiteSpace(emoji)) return;

        var info = _gameManager.GetConnectionInfo(Context.ConnectionId);
        if (info == null) return;

        var room = _gameManager.GetRoom(info.Value.roomCode);
        if (room == null) return;

        var player = room.GetPlayer(info.Value.playerId);
        var senderName = player?.Name ?? "Alguien";

        await Clients.Group(room.Code).SendAsync("ReactionReceived", new
        {
            emoji = emoji.Trim(),
            senderName,
            senderAvatar = player?.Avatar ?? "😎"
        });
    }

    public async Task AddCustomCard(string text, bool isBlack, int pick)
    {
        if (string.IsNullOrWhiteSpace(text)) return;

        var info = _gameManager.GetConnectionInfo(Context.ConnectionId);
        if (info == null) return;

        var room = _gameManager.GetRoom(info.Value.roomCode);
        if (room == null) return;

        var card = new Card
        {
            Id = $"c_{Guid.NewGuid():N}",
            Text = text.Trim(),
            Type = isBlack ? "black" : "white",
            Pick = Math.Clamp(pick, 1, 3)
        };

        lock (room.SyncLock)
        {
            if (isBlack)
            {
                room.BlackDeck.Add(card);
            }
            else
            {
                room.WhiteDeck.Add(card);
            }

            room.ChatMessages.Add(new ChatMessage
            {
                SenderName = "Sistema",
                SenderAvatar = "⚡",
                Text = $"¡Se agregó una nueva carta personalizada: «{card.Text}»!",
                IsSystem = true
            });
        }

        await _gameManager.BroadcastRoomStateAsync(room);
    }

    public override async Task OnDisconnectedAsync(Exception? exception)
    {
        var info = _gameManager.GetConnectionInfo(Context.ConnectionId);
        if (info != null)
        {
            var room = _gameManager.GetRoom(info.Value.roomCode);
            if (room != null)
            {
                bool shouldClose = room.RemovePlayer(info.Value.playerId);

                if (shouldClose)
                {
                    // Only 1 human left mid-game — notify all to go back to lobby
                    await _gameManager.Clients.Group(room.Code).SendAsync("RoomClosed", "Quedó solo un jugador. La sala se ha cerrado.");
                }
                else
                {
                    await _gameManager.BroadcastRoomStateAsync(room);
                }
            }
            _gameManager.UnregisterConnection(Context.ConnectionId);
        }

        await base.OnDisconnectedAsync(exception);
    }
}
