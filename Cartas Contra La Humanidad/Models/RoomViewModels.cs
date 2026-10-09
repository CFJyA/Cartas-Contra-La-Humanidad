namespace Cartas_Contra_La_Humanidad.Models;

public class PlayerClientDto
{
    public string Id { get; set; } = string.Empty;
    public string Name { get; set; } = string.Empty;
    public string Avatar { get; set; } = string.Empty;
    public int Score { get; set; } = 0;
    public bool IsCzar { get; set; } = false;
    public bool IsHost { get; set; } = false;
    public bool IsReady { get; set; } = false;
    public bool IsConnected { get; set; } = true;
    public bool IsBot { get; set; } = false;
    public bool IsSpectator { get; set; } = false;
    public bool HasSubmitted { get; set; } = false;
}

public class SubmissionClientDto
{
    public string Id { get; set; } = string.Empty;
    public string PlayerId { get; set; } = string.Empty; // masked during Judging
    public string PlayerName { get; set; } = string.Empty; // masked during Judging
    public string PlayerAvatar { get; set; } = string.Empty; // masked during Judging
    public List<Card> Cards { get; set; } = new();
    public bool IsWinner { get; set; } = false;
}

public class RoomClientStateDto
{
    public string Code { get; set; } = string.Empty;
    public string State { get; set; } = "Lobby";
    public int TargetScore { get; set; } = 7;
    public int RoundTimerSeconds { get; set; } = 60;
    public int TimeRemaining { get; set; } = 0;
    public int CurrentRound { get; set; } = 0;
    public Card? ActiveBlackCard { get; set; }
    public List<PlayerClientDto> Players { get; set; } = new();
    public List<Card> MyHand { get; set; } = new();
    public List<Card> MySubmittedCards { get; set; } = new();
    public bool AmICzar { get; set; } = false;
    public bool AmIHost { get; set; } = false;
    public string CzarName { get; set; } = string.Empty;
    public string CzarAvatar { get; set; } = string.Empty;
    public List<SubmissionClientDto> Submissions { get; set; } = new();
    public SubmissionClientDto? WinningSubmission { get; set; }
    public string? WinnerPlayerName { get; set; }
    public bool RandoCardrissianEnabled { get; set; } = false;
    public int WhiteDeckCount { get; set; } = 0;
    public int BlackDeckCount { get; set; } = 0;
    public List<ChatMessage> ChatMessages { get; set; } = new();
}
