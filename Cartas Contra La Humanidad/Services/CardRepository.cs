using System.Text.Json;
using Cartas_Contra_La_Humanidad.Models;

namespace Cartas_Contra_La_Humanidad.Services;

public class CardRepository
{
    private readonly List<Card> _whiteCards = new();
    private readonly List<Card> _blackCards = new();
    private readonly IWebHostEnvironment _env;

    public CardRepository(IWebHostEnvironment env)
    {
        _env = env;
        LoadCards();
    }

    private void LoadCards()
    {
        try
        {
            var filePath = Path.Combine(_env.ContentRootPath, "Data", "cards_database.json");
            if (!File.Exists(filePath)) return;

            var json = File.ReadAllText(filePath);
            using var doc = JsonDocument.Parse(json);
            var root = doc.RootElement;

            if (root.TryGetProperty("whiteCards", out var whites))
            {
                foreach (var el in whites.EnumerateArray())
                {
                    _whiteCards.Add(new Card
                    {
                        Id = el.GetProperty("id").GetString() ?? Guid.NewGuid().ToString("N"),
                        Text = el.GetProperty("text").GetString() ?? "",
                        Type = "white"
                    });
                }
            }

            if (root.TryGetProperty("blackCards", out var blacks))
            {
                foreach (var el in blacks.EnumerateArray())
                {
                    _blackCards.Add(new Card
                    {
                        Id = el.GetProperty("id").GetString() ?? Guid.NewGuid().ToString("N"),
                        Text = el.GetProperty("text").GetString() ?? "",
                        Type = "black",
                        Pick = el.TryGetProperty("pick", out var p) ? p.GetInt32() : 1,
                        Draw = el.TryGetProperty("draw", out var d) ? d.GetInt32() : 0
                    });
                }
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error loading cards: {ex.Message}");
        }
    }

    public List<Card> GetWhiteCards() => new(_whiteCards);
    public List<Card> GetBlackCards() => new(_blackCards);

    public void AddCustomCard(Card card)
    {
        if (card.Type == "black")
        {
            _blackCards.Add(card);
        }
        else
        {
            _whiteCards.Add(card);
        }
    }
}
