namespace Cartas_Contra_La_Humanidad.Models;

public class Player
{
    public string Id { get; set; } = Guid.NewGuid().ToString("N");
    public string ConnectionId { get; set; } = string.Empty;
    public string Name { get; set; } = string.Empty;
    public string Avatar { get; set; } = "😎";
    public int Score { get; set; } = 0;
    public bool IsCzar { get; set; } = false;
    public bool IsHost { get; set; } = false;
    public bool IsReady { get; set; } = false;
    public bool IsConnected { get; set; } = true;
    public bool IsBot { get; set; } = false;
    public List<Card> Hand { get; set; } = new();
    public List<Card> SubmittedCards { get; set; } = new();
    public bool HasSubmitted => SubmittedCards.Count > 0;
}
