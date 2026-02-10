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
1. Place your `config.yml` in the `/config` directory.
2. Launch the stack:
   ```bash
   docker-compose up -d --build
