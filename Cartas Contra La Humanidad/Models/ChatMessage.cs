namespace Cartas_Contra_La_Humanidad.Models;

public class ChatMessage
{
    public string SenderName { get; set; } = string.Empty;
    public string SenderAvatar { get; set; } = string.Empty;
    public string Text { get; set; } = string.Empty;
    public DateTime Timestamp { get; set; } = DateTime.UtcNow;
    public bool IsSystem { get; set; } = false;
}
