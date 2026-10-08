using System.Security.Cryptography;

namespace Cartas_Contra_La_Humanidad.Models;

public class GameRoom
{
    private readonly object _lock = new();

    public string Code { get; set; } = string.Empty;
    public string HostId { get; set; } = string.Empty;
    public string State { get; set; } = "Lobby"; // "Lobby", "Playing", "Judging", "RoundResults", "GameOver"
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

    public int TargetScore { get; set; } = 7;
    public int RoundTimerSeconds { get; set; } = 60;
    public int TimeRemaining { get; set; } = 0;
    public int CurrentRound { get; set; } = 0;
    public int CurrentCzarIndex { get; set; } = -1;

    public Card? ActiveBlackCard { get; set; }
    public List<Player> Players { get; set; } = new();
    public List<RoundSubmission> Submissions { get; set; } = new();
    public RoundSubmission? WinningSubmission { get; set; }
    public string? WinnerPlayerName { get; set; }

    public List<Card> WhiteDeck { get; set; } = new();
    public List<Card> BlackDeck { get; set; } = new();
    public List<Card> WhiteDiscard { get; set; } = new();
    public List<Card> BlackDiscard { get; set; } = new();

    public bool RandoCardrissianEnabled { get; set; } = true;
    public List<ChatMessage> ChatMessages { get; set; } = new();

    public object SyncLock => _lock;

    public Player? GetPlayer(string playerId) => Players.FirstOrDefault(p => p.Id == playerId);
    public Player? GetPlayerByConnection(string connectionId) => Players.FirstOrDefault(p => p.ConnectionId == connectionId);

    public void AddPlayer(Player player)
    {
        lock (_lock)
        {
            var existing = Players.FirstOrDefault(p => p.Id == player.Id);
            if (existing != null)
            {
                existing.ConnectionId = player.ConnectionId;
                existing.IsConnected = true;
                existing.Name = player.Name;
                existing.Avatar = player.Avatar;
                return;
            }

            if (Players.Count == 0)
            {
                player.IsHost = true;
                HostId = player.Id;
            }

            // If game is already active, deal hand so player is ready
            if (State != "Lobby")
            {
                DealCardsToPlayer(player, 10);
            }

            Players.Add(player);
        }
    }

    public void RemovePlayer(string playerId)
    {
        lock (_lock)
        {
            var p = Players.FirstOrDefault(x => x.Id == playerId);
            if (p == null) return;

            p.IsConnected = false;

            // If bot or lobby, we can remove completely
            if (p.IsBot || State == "Lobby")
            {
                Players.Remove(p);
            }

            // If host left, elect new host
            if (p.IsHost && Players.Any(x => x.IsConnected && !x.IsBot))
            {
                var newHost = Players.First(x => x.IsConnected && !x.IsBot);
                newHost.IsHost = true;
                HostId = newHost.Id;
            }

            // If Czar disconnected during game
            if (p.IsCzar && State is "Playing" or "Judging")
            {
                ElectNewCzar();
            }
        }
    }

    public void ElectNewCzar()
    {
        var activeHumanOrBots = Players.Where(x => x.IsConnected).ToList();
        if (activeHumanOrBots.Count == 0) return;

        foreach (var pl in Players) pl.IsCzar = false;
        CurrentCzarIndex = (CurrentCzarIndex + 1) % activeHumanOrBots.Count;
        activeHumanOrBots[CurrentCzarIndex].IsCzar = true;
    }

    public bool StartGame(List<Card> initialWhiteCards, List<Card> initialBlackCards)
    {
        lock (_lock)
        {
            if (Players.Count < 2) return false;

            WhiteDeck = Shuffle(new List<Card>(initialWhiteCards));
            BlackDeck = Shuffle(new List<Card>(initialBlackCards));
            WhiteDiscard.Clear();
            BlackDiscard.Clear();

            CurrentRound = 0;
            CurrentCzarIndex = -1;

            foreach (var p in Players)
            {
                p.Score = 0;
                p.Hand.Clear();
                p.SubmittedCards.Clear();
                p.IsCzar = false;
                DealCardsToPlayer(p, 10);
            }

            if (RandoCardrissianEnabled && !Players.Any(p => p.Name == "Rando Cardrissian"))
            {
                AddBot("Rando Cardrissian", "🤖");
            }

            StartNewRound();
            return true;
        }
    }

    public void StartNewRound()
    {
        lock (_lock)
        {
            CurrentRound++;
            WinningSubmission = null;
            WinnerPlayerName = null;
            Submissions.Clear();

            // Refill hands for all players up to 10
            foreach (var p in Players)
            {
                p.SubmittedCards.Clear();
                if (p.Hand.Count < 10)
                {
                    DealCardsToPlayer(p, 10 - p.Hand.Count);
                }
            }

            // Rotate Czar
            var activePlayers = Players.Where(p => p.IsConnected).ToList();
            if (activePlayers.Count == 0) return;

            foreach (var pl in Players) pl.IsCzar = false;
            CurrentCzarIndex = (CurrentCzarIndex + 1) % activePlayers.Count;
            activePlayers[CurrentCzarIndex].IsCzar = true;

            // Pick Black Card
            if (BlackDeck.Count == 0)
            {
                BlackDeck = Shuffle(BlackDiscard);
                BlackDiscard.Clear();
            }

            if (BlackDeck.Count > 0)
            {
                ActiveBlackCard = BlackDeck[0];
                BlackDeck.RemoveAt(0);
                BlackDiscard.Add(ActiveBlackCard);
            }

            // If black card specifies Draw > 0, give each player extra cards
            if (ActiveBlackCard != null && ActiveBlackCard.Draw > 0)
            {
                foreach (var p in Players)
                {
                    DealCardsToPlayer(p, ActiveBlackCard.Draw);
                }
            }

            State = "Playing";
            TimeRemaining = RoundTimerSeconds;

            // Trigger bot submissions
            BotAutoPlay();
        }
    }

    public void BotAutoPlay()
    {
        if (ActiveBlackCard == null) return;
        int required = ActiveBlackCard.Pick;

        var bots = Players.Where(p => p.IsBot && !p.IsCzar && p.IsConnected).ToList();
        var rng = new Random();

        foreach (var bot in bots)
        {
            if (bot.Hand.Count < required)
            {
                DealCardsToPlayer(bot, 10);
            }

            if (bot.Hand.Count >= required)
            {
                // Shuffle bot hand and take required count
                var selected = bot.Hand.OrderBy(_ => rng.Next()).Take(required).ToList();
                foreach (var c in selected)
                {
                    bot.Hand.Remove(c);
                }
                bot.SubmittedCards = new List<Card>(selected);

                Submissions.Add(new RoundSubmission
                {
                    PlayerId = bot.Id,
                    PlayerName = bot.Name,
                    PlayerAvatar = bot.Avatar,
                    Cards = new List<Card>(selected)
                });
            }
        }
    }

    public bool SubmitCards(string playerId, List<string> cardIds)
    {
        lock (_lock)
        {
            if (State != "Playing" || ActiveBlackCard == null) return false;

            var player = GetPlayer(playerId);
            if (player == null || player.IsCzar || player.HasSubmitted) return false;

            if (cardIds.Count != ActiveBlackCard.Pick) return false;

            var playedCards = new List<Card>();
            foreach (var cid in cardIds)
            {
                var card = player.Hand.FirstOrDefault(c => c.Id == cid);
                if (card == null) return false; // invalid card or not in hand
                playedCards.Add(card);
            }

            // Remove from hand in order
            foreach (var card in playedCards)
            {
                player.Hand.Remove(card);
                WhiteDiscard.Add(card);
            }

            player.SubmittedCards = new List<Card>(playedCards);

            Submissions.Add(new RoundSubmission
            {
                PlayerId = player.Id,
                PlayerName = player.Name,
                PlayerAvatar = player.Avatar,
                Cards = new List<Card>(playedCards)
            });

            // Check if all non-Czar connected players have submitted
            var nonCzars = Players.Where(p => !p.IsCzar && p.IsConnected).ToList();
            if (nonCzars.All(p => p.HasSubmitted))
            {
                TransitionToJudging();
            }

            return true;
        }
    }

    public void TransitionToJudging()
    {
        lock (_lock)
        {
            State = "Judging";
            TimeRemaining = 0;
            // Shuffle submissions so Czar has no idea whose is whose
            Submissions = Shuffle(Submissions);
        }
    }

    public bool SelectWinner(string czarPlayerId, string submissionId)
    {
        lock (_lock)
        {
            if (State != "Judging") return false;

            var czar = GetPlayer(czarPlayerId);
            if (czar == null || !czar.IsCzar) return false;

            var submission = Submissions.FirstOrDefault(s => s.Id == submissionId);
            if (submission == null) return false;

            submission.IsWinner = true;
            WinningSubmission = submission;

            var winnerPlayer = GetPlayer(submission.PlayerId);
            if (winnerPlayer != null)
            {
                winnerPlayer.Score += 1;
                WinnerPlayerName = winnerPlayer.Name;

                if (winnerPlayer.Score >= TargetScore)
                {
                    State = "GameOver";
                    return true;
                }
            }
            else
            {
                WinnerPlayerName = submission.PlayerName;
            }

            State = "RoundResults";
            return true;
        }
    }

    public void AddBot(string name, string avatar = "🤖")
    {
        lock (_lock)
        {
            var bot = new Player
            {
                Id = Guid.NewGuid().ToString("N"),
                Name = name,
                Avatar = avatar,
                IsBot = true,
                IsReady = true,
                IsConnected = true
            };
            DealCardsToPlayer(bot, 10);
            Players.Add(bot);
        }
    }

    public void RemoveBot(string botId)
    {
        lock (_lock)
        {
            var bot = Players.FirstOrDefault(p => p.Id == botId && p.IsBot);
            if (bot != null)
            {
                Players.Remove(bot);
            }
        }
    }

    public void DealCardsToPlayer(Player player, int count)
    {
        for (int i = 0; i < count; i++)
        {
            if (WhiteDeck.Count == 0)
            {
                WhiteDeck = Shuffle(WhiteDiscard);
                WhiteDiscard.Clear();
            }

            if (WhiteDeck.Count > 0)
            {
                var card = WhiteDeck[0];
                WhiteDeck.RemoveAt(0);
                player.Hand.Add(card);
            }
        }
    }

    public RoomClientStateDto ToClientDto(string requestingPlayerId)
    {
        lock (_lock)
        {
            var requestingPlayer = GetPlayer(requestingPlayerId);
            var czar = Players.FirstOrDefault(p => p.IsCzar);

            var dto = new RoomClientStateDto
            {
                Code = Code,
                State = State,
                TargetScore = TargetScore,
                RoundTimerSeconds = RoundTimerSeconds,
                TimeRemaining = TimeRemaining,
                CurrentRound = CurrentRound,
                ActiveBlackCard = ActiveBlackCard,
                RandoCardrissianEnabled = RandoCardrissianEnabled,
                WhiteDeckCount = WhiteDeck.Count,
                BlackDeckCount = BlackDeck.Count,
                CzarName = czar?.Name ?? "",
                CzarAvatar = czar?.Avatar ?? "",
                WinnerPlayerName = WinnerPlayerName,
                ChatMessages = ChatMessages.TakeLast(30).ToList(),
                Players = Players.Select(p => new PlayerClientDto
                {
                    Id = p.Id,
                    Name = p.Name,
                    Avatar = p.Avatar,
                    Score = p.Score,
                    IsCzar = p.IsCzar,
                    IsHost = p.IsHost,
                    IsReady = p.IsReady,
                    IsConnected = p.IsConnected,
                    IsBot = p.IsBot,
                    HasSubmitted = p.HasSubmitted
                }).ToList()
            };

            if (requestingPlayer != null)
            {
                dto.MyHand = new List<Card>(requestingPlayer.Hand);
                dto.MySubmittedCards = new List<Card>(requestingPlayer.SubmittedCards);
                dto.AmICzar = requestingPlayer.IsCzar;
                dto.AmIHost = requestingPlayer.IsHost;
            }

            // Format submissions:
            // During "Judging", hide player identity!
            // During "RoundResults" and "GameOver", reveal who submitted what!
            if (State == "Judging")
            {
                dto.Submissions = Submissions.Select(s => new SubmissionClientDto
                {
                    Id = s.Id,
                    PlayerId = "",
                    PlayerName = "Anónimo",
                    PlayerAvatar = "🃏",
                    Cards = s.Cards,
                    IsWinner = s.IsWinner
                }).ToList();
            }
            else if (State is "RoundResults" or "GameOver")
            {
                dto.Submissions = Submissions.Select(s => new SubmissionClientDto
                {
                    Id = s.Id,
                    PlayerId = s.PlayerId,
                    PlayerName = s.PlayerName,
                    PlayerAvatar = s.PlayerAvatar,
                    Cards = s.Cards,
                    IsWinner = s.IsWinner
                }).ToList();

                if (WinningSubmission != null)
                {
                    dto.WinningSubmission = new SubmissionClientDto
                    {
                        Id = WinningSubmission.Id,
                        PlayerId = WinningSubmission.PlayerId,
                        PlayerName = WinningSubmission.PlayerName,
                        PlayerAvatar = WinningSubmission.PlayerAvatar,
                        Cards = WinningSubmission.Cards,
                        IsWinner = true
                    };
                }
            }

            return dto;
        }
    }

    private static List<T> Shuffle<T>(List<T> list)
    {
        var rng = new Random();
        var buffer = new List<T>(list);
        for (int i = buffer.Count - 1; i > 0; i--)
        {
            int j = rng.Next(i + 1);
            (buffer[i], buffer[j]) = (buffer[j], buffer[i]);
        }
        return buffer;
    }
}
