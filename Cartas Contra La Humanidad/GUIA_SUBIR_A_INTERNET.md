# 🌐 Guía para Subir Cartas Contra La Humanidad a una Página Web

Tienes **3 opciones excelentes** dependiendo de lo que busques:

---

## ⚡ Opción 1: Túnel Público Inmediato con Cloudflare (¡Listo en 10 segundos!)
Ideal para jugar **hoy mismo** con amigos en sus celulares sin configurar servidores ni abrir cuentas.

1. Inicia el juego en **Visual Studio** (presionando `Ctrl + F5` o el botón verde de Play).
2. Haz doble clic en el archivo **`iniciar_tunel_online.bat`** que te dejé en la carpeta del proyecto.
3. Se abrirá una ventana que mostrará un enlace como:
   ```
   https://tu-nombre-aleatorio.trycloudflare.com
   ```
4. **¡Listo!** Ese enlace es 100% público, seguro con HTTPS y funciona en cualquier celular (con datos 4G/5G o cualquier Wi-Fi) en cualquier parte del mundo.

---

## ☁️ Opción 2: Subir a MonsterASP.NET (Hosting Gratuito 24/7 de ASP.NET Core)
Ideal si quieres que la página web esté **siempre activa en internet** sin que tu computadora esté encendida.

1. Entra a [https://www.monsterasp.net](https://www.monsterasp.net) y crea una cuenta gratuita.
2. Crea un nuevo sitio web gratuito (te dará un subdominio como `micartas.monsterasp.net`).
3. En el panel de control, ve a **File Manager** (Gestor de Archivos).
4. Dale a **Upload Zip** y sube el archivo que ya te dejé preparado en la carpeta del proyecto:
   `CartasContraLaHumanidad_Publicacion.zip`
5. El sistema descomprimirá los archivos automáticamente.
6. ¡Listo! Tu juego estará online las 24 horas del día.

---

## 🚀 Opción 3: Desplegar en Render.com con Docker
Para programadores que usan GitHub y quieren despliegue continuo con SSL gratuito.

1. Sube tu proyecto a un repositorio de **GitHub**.
2. Entra a [https://render.com](https://render.com) e inicia sesión con tu GitHub.
3. Haz clic en **New +** > **Web Service**.
4. Selecciona tu repositorio.
5. Render detectará automáticamente el archivo `Dockerfile` que te dejé configurado.
6. En el plan selecciona **Free** y dale a **Create Web Service**.
7. En 2-3 minutos tendrás tu URL pública: `https://cartas-contra-la-humanidad.onrender.com`.

---

## 🔷 Opción 4: Publicar en Azure App Service desde Visual Studio
1. En Visual Studio, dale clic derecho al proyecto **Cartas Contra La Humanidad** en el Explorador de soluciones.
2. Selecciona **Publicar... (Publish)**.
3. Elige **Azure** > **Azure App Service (Linux o Windows)**.
4. Elige el plan gratuito **F1 Free**.
5. Tras publicar, en el portal de Azure asegúrate de ir a **Configuración** de la App y activar la opción **WebSockets = Activado (On)** para que SignalR funcione al 100%.
