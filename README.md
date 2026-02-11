# OwnVoice TTS Server

A simple, fast Text-to-Speech server with Romanian language support.

## Features

- ✅ **Romanian TTS** with natural-sounding voices
- 🌍 **Multi-language support** (English, Spanish, French, German, Italian, Portuguese)
- 🚀 **Fast API** built with FastAPI
- 💾 **Smart caching** for improved performance
- 🔌 **RESTful API** easy to integrate

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/icefelix/ownvoice-tts.git
cd ownvoice-tts

# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py
```

The server will start on `http://0.0.0.0:8001`

### Docker (Alternative)

```bash
docker build -t ownvoice-tts .
docker run -p 8001:8001 ownvoice-tts
```

## API Endpoints

### POST /synthesize

Generate speech from text.

**Form Data:**
- `text` (required): Text to synthesize
- `lang` (optional, default: "ro"): Language code
- `voice` (optional): Voice ID (not used with gTTS)

**Example:**

```bash
curl -X POST "http://localhost:8001/synthesize" \
  -F "text=Bună ziua! Cum te numești?" \
  -F "lang=ro" \
  --output speech.mp3
```

**Supported Languages:**
- `ro` - Romanian
- `en` - English
- `es` - Spanish
- `fr` - French
- `de` - German
- `it` - Italian
- `pt` - Portuguese

### GET /health

Health check endpoint.

```bash
curl http://localhost:8001/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "OwnVoice TTS",
  "version": "1.0.0",
  "timestamp": "2024-02-11T10:00:00",
  "cache": {
    "directory": "cache",
    "files": 42
  },
  "supported_languages": 7
}
```

### GET /languages

List all supported languages.

```bash
curl http://localhost:8001/languages
```

### GET /voices

List available voices.

```bash
curl http://localhost:8001/voices
```

## Configuration

Environment variables:

- `PORT` - Server port (default: 8001)
- `HOST` - Server host (default: 0.0.0.0)

## Production Deployment

### Systemd Service

Create `/etc/systemd/system/ownvoice-tts.service`:

```ini
[Unit]
Description=OwnVoice TTS Server
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/ownvoice-tts
Environment="PATH=/var/www/ownvoice-tts/venv/bin"
ExecStart=/var/www/ownvoice-tts/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable ownvoice-tts
sudo systemctl start ownvoice-tts
```

### Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name nn-voice.icefelix.com;

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Testing

```bash
# Test health endpoint
curl http://localhost:8001/health

# Test synthesis
curl -X POST "http://localhost:8001/synthesize" \
  -F "text=Acesta este un test" \
  -F "lang=ro" \
  --output test.mp3

# Play the audio
mpg123 test.mp3  # or your audio player
```

## Cache Management

Audio files are cached in the `cache/` directory. To clear the cache:

```bash
rm -rf cache/*.mp3
```

## Technology Stack

- **FastAPI** - Modern, fast web framework
- **gTTS** - Google Text-to-Speech
- **Uvicorn** - ASGI server

## License

MIT License

## Author

IceFeliz Team

## Support

For issues and questions: https://github.com/icefelix/ownvoice-tts/issues
