@echo off
chcp 65001 >nul
title Cartas Contra La Humanidad - Tunel Publico Cloudflare
echo ======================================================================
echo    🃏 CARTAS CONTRA LA HUMANIDAD - TÚNEL PÚBLICO CLOUDFLARE
echo ======================================================================
echo.
echo  1. Asegúrate de que el juego esté iniciado (en Visual Studio con F5/Ctrl+F5).
echo  2. Este programa creará un enlace HTTPS público gratuito y seguro.
echo  3. Busca abajo la línea que dice:
echo.
echo     https://[nombre-aleatorio].trycloudflare.com
echo.
echo  4. Comparte ese enlace por WhatsApp o ábrelo en cualquier celular con datos
echo     o Wi-Fi. ¡Funcionará de inmediato en cualquier parte del mundo!
echo ======================================================================
echo.
cloudflared.exe tunnel --url http://localhost:5012
pause
