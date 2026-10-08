namespace Cartas_Contra_La_Humanidad.Models;

public class RoundSubmission
{
    public string Id { get; set; } = Guid.NewGuid().ToString("N");
    public string PlayerId { get; set; } = string.Empty;
    public string PlayerName { get; set; } = string.Empty;
    public string PlayerAvatar { get; set; } = string.Empty;
    public List<Card> Cards { get; set; } = new();
    public bool IsWinner { get; set; } = false;
}
