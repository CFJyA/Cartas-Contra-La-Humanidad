using System.Diagnostics;
using System.Net;
using System.Net.NetworkInformation;
using System.Net.Sockets;
using Cartas_Contra_La_Humanidad.Models;
using Microsoft.AspNetCore.Mvc;

namespace Cartas_Contra_La_Humanidad.Controllers;

public class HomeController : Controller
{
    public IActionResult Index()
    {
        string? hotspotIp = null;
        string? wifiIp = null;
        var detectedIps = new List<(string Label, string Ip)>();

        try
        {
            var interfaces = NetworkInterface.GetAllNetworkInterfaces()
                .Where(n => n.OperationalStatus == OperationalStatus.Up);

            foreach (var iface in interfaces)
            {
                var ipProps = iface.GetIPProperties();
                var ipv4 = ipProps.UnicastAddresses
                    .FirstOrDefault(u => u.Address.AddressFamily == AddressFamily.InterNetwork && !IPAddress.IsLoopback(u.Address))?.Address.ToString();

                if (string.IsNullOrEmpty(ipv4) || ipv4.StartsWith("169.254")) continue;

                var desc = iface.Description.ToLowerInvariant();
                var name = iface.Name.ToLowerInvariant();

                // Detect Windows Mobile Hotspot (Microsoft Wi-Fi Direct or 192.168.137.x subnet)
                if (desc.Contains("wi-fi direct") || desc.Contains("virtual") || ipv4.StartsWith("192.168.137") || name.Contains("área local*") || name.Contains("local area*"))
                {
                    hotspotIp = ipv4;
                    detectedIps.Insert(0, ("Punto de Acceso (Hotspot)", ipv4));
                }
                else if (desc.Contains("wi-fi") || desc.Contains("wireless") || name.Contains("wi-fi"))
                {
                    wifiIp = ipv4;
                    detectedIps.Add(("Red Wi-Fi", ipv4));
                }
                else
                {
                    detectedIps.Add((iface.Name, ipv4));
                }
            }
        }
        catch
        {
            // fallback
        }

        ViewBag.HotspotIp = hotspotIp ?? "192.168.137.1";
        ViewBag.WifiIp = wifiIp ?? "localhost";
        ViewBag.PrimaryMobileIp = hotspotIp ?? wifiIp ?? "localhost";
        ViewBag.AllIps = detectedIps;

        return View();
    }

    [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
    public IActionResult Error()
    {
        return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
    }
}
