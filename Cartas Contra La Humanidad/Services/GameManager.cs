using System.Collections.Concurrent;
using Cartas_Contra_La_Humanidad.Hubs;
using Cartas_Contra_La_Humanidad.Models;
using Microsoft.AspNetCore.SignalR;

namespace Cartas_Contra_La_Humanidad.Services;

public class GameManager
{
    private readonly ConcurrentDictionary<string, GameRoom> _rooms = new();
    private readonly ConcurrentDictionary<string, (string roomCode, string playerId)> _connections = new();
    private readonly CardRepository _cardRepository;
    private readonly IHubContext<GameHub> _hubContext;
    private readonly Timer _tickTimer;

    private static readonly string[] RoomWords =
    [
        "VERGA", "CHILE", "HUMAN", "FARKAS", "TULIO", "POTO", "PICANTE", "CAH", "TURBO", "CRACK"
    ];

    private static readonly string[] BotNames =
    [
        "El Brayan Bot", "El Bot Tóxico", "Don Graf", "Tía Pikachu", "El Cuma Bot", "Farkas Bot"
    ];

    public GameManager(CardRepository cardRepository, IHubContext<GameHub> hubContext)
    {
        _cardRepository = cardRepository;
        _hubContext = hubContext;
        _tickTimer = new Timer(OnTick, null, 1000, 1000);
    }

    /// <summary>Exposes the hub clients so GameHub can send targeted events (e.g. RoomClosed).</summary>
    public IHubClients Clients => _hubContext.Clients;


    public GameRoom CreateRoom(string hostPlayerName, string avatar, int targetScore, int timerSeconds, bool randoBot)
    {
        var code = GenerateRoomCode();
        var host = new Player
        {
            Id = Guid.NewGuid().ToString("N"),
            Name = string.IsNullOrWhiteSpace(hostPlayerName) ? "Jugador 1" : hostPlayerName.Trim(),
            Avatar = string.IsNullOrWhiteSpace(avatar) ? "😎" : avatar,
            IsHost = true,
            IsReady = true
        };

        var room = new GameRoom
        {
            Code = code,
            HostId = host.Id,
            TargetScore = Math.Clamp(targetScore, 3, 20),
            RoundTimerSeconds = timerSeconds >= 0 ? timerSeconds : 60,
            RandoCardrissianEnabled = randoBot
        };

        room.AddPlayer(host);
        _rooms[code] = room;

        return room;
    }

    public GameRoom? GetRoom(string code)
    {
        if (string.IsNullOrWhiteSpace(code)) return null;
        _rooms.TryGetValue(code.Trim().ToUpperInvariant(), out var room);
        return room;
    }

    public void RegisterConnection(string connectionId, string roomCode, string playerId)
    {
        _connections[connectionId] = (roomCode.ToUpperInvariant(), playerId);
    }

    public (string roomCode, string playerId)? GetConnectionInfo(string connectionId)
    {
        if (_connections.TryGetValue(connectionId, out var info))
        {
            return info;
        }
        return null;
    }

    public void UnregisterConnection(string connectionId)
    {
        _connections.TryRemove(connectionId, out _);
    }

    public async Task BroadcastRoomStateAsync(GameRoom room)
    {
        List<Player> targetPlayers;
        lock (room.SyncLock)
        {
            targetPlayers = room.Players.Where(p => p.IsConnected && !p.IsBot).ToList();
        }

        foreach (var player in targetPlayers)
        {
            if (!string.IsNullOrEmpty(player.ConnectionId))
            {
                var state = room.ToClientDto(player.Id);
                try
                {
                    await _hubContext.Clients.Client(player.ConnectionId).SendAsync("RoomUpdated", state);
                }
                catch
                {
                    // Ignore transient network errors
                }
            }
        }
    }

    public void AddBotToRoom(GameRoom room)
    {
        lock (room.SyncLock)
        {
            var usedNames = room.Players.Select(p => p.Name).ToHashSet();
            var availableName = BotNames.FirstOrDefault(n => !usedNames.Contains(n)) 
                                ?? $"Bot #{room.Players.Count(p => p.IsBot) + 1}";

            string[] botAvatars = ["🤖", "👽", "👾", "🤡", "👻", "💀"];
            var rndAvatar = botAvatars[Random.Shared.Next(botAvatars.Length)];

            room.AddBot(availableName, rndAvatar);
        }
    }

    public List<Card> GetDefaultWhiteCards() => _cardRepository.GetWhiteCards();
    public List<Card> GetDefaultBlackCards() => _cardRepository.GetBlackCards();

    public void AddCustomCard(Card card)
    {
        _cardRepository.AddCustomCard(card);
    }

    private string GenerateRoomCode()
    {
        var rnd = new Random();
        for (int i = 0; i < 50; i++)
        {
            var word = RoomWords[rnd.Next(RoomWords.Length)];
            var num = rnd.Next(10, 99);
            var code = $"{word}{num}";
            if (!_rooms.ContainsKey(code))
            {
                return code;
            }
        }
        return Guid.NewGuid().ToString("N")[..6].ToUpperInvariant();
    }

    private async void OnTick(object? state)
    {
        foreach (var kvp in _rooms)
        {
            var room = kvp.Value;
            bool stateChanged = false;

            lock (room.SyncLock)
            {
                if (room.State == "Playing" && room.RoundTimerSeconds > 0)
                {
                    if (room.TimeRemaining > 0)
                    {
                        room.TimeRemaining--;
                    }
                    else
                    {
                        // Timer expired! Auto submit random cards for players who haven't played
                        if (room.ActiveBlackCard != null)
                        {
                            var pickCount = room.ActiveBlackCard.Pick;
                            var pendingPlayers = room.Players.Where(p => !p.IsCzar && p.IsConnected && !p.HasSubmitted && !p.IsSpectator).ToList();

                            foreach (var p in pendingPlayers)
                            {
                                if (p.Hand.Count >= pickCount)
                                {
                                    var randomPicks = p.Hand.OrderBy(_ => Random.Shared.Next()).Take(pickCount).Select(c => c.Id).ToList();
                                    room.SubmitCards(p.Id, randomPicks);
                                }
                            }
                        }

                        room.TransitionToJudging();
                        stateChanged = true;
                    }
                }
            }

            if (stateChanged)
            {
                await BroadcastRoomStateAsync(room);
            }
            else if (room.State == "Playing" && room.RoundTimerSeconds > 0)
            {
                // Send timer tick event
                await _hubContext.Clients.Group(room.Code).SendAsync("TimerTick", room.TimeRemaining);
            }
        }
    }
}
