namespace Cartas_Contra_La_Humanidad.Models;

public class Card
{
    public string Id { get; set; } = string.Empty;
    public string Text { get; set; } = string.Empty;
    public string Type { get; set; } = "white"; // "white" or "black"
    public int Pick { get; set; } = 1;
    public int Draw { get; set; } = 0;
}
