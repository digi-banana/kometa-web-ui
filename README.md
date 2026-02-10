# kometa-web-ui
Vibe coded Kometa Web UI with Monaco Editor and Cron

# ☄️ Kometa Web Commander

A custom web interface for [Kometa](https://github.com/Kometa-Team/Kometa) featuring a split-screen editor, real-time status updates, and cron scheduling.

## ✨ Features
- **Monaco Editor:** VS Code-grade YAML editing with context-aware parameter help.
- **Real-time Logs:** Stream Kometa output directly to your browser via WebSockets.
- **Asset Management:** Static poster preview with drag-and-drop upload functionality.
- **Cron Scheduling:** Schedule your syncs directly from the UI (defaulted to America/Detroit).
- **Dockerized:** Runs alongside the official Kometa container via Docker Compose.

## 🛠️ Quick Start
1. Clone the respository:
   ```bash
   git clone https://github.com/digi-banana/kometa-web-ui
2. Edit `docker-compose.yml`
   - `./config:/config` --> Replace "`./config`" with the location of where your existing config.yml file is
     - Note that this shows up in "volumes" under the kometa service and twice in the kometa-ui service
   - `TZ=America/New_York` --> Replace with your timezone so that the cron jobs will be run at the correct times
     - A list of timezones can be found here: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List
4. Place your `config.yml` in the `/config` directory.
5. Launch the stack:
   ```bash
   docker-compose up -d --build
6. Access the dashboard at http://localhost:8461
