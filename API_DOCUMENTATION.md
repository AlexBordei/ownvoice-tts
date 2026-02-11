# OwnVoice TTS API - Complete Documentation

Complete REST API documentation for OwnVoice Text-to-Speech service.

**Base URL:** `http://nn-voice.icefelix.com`

**Version:** 1.0.0

---

## Table of Contents

- [Authentication](#authentication)
- [Endpoints](#endpoints)
  - [GET /](#get-)
  - [GET /health](#get-health)
  - [GET /languages](#get-languages)
  - [GET /voices](#get-voices)
  - [POST /synthesize](#post-synthesize)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)
- [Examples](#examples)

---

## Authentication

Currently, the API does not require authentication. All endpoints are publicly accessible.

> **Note for Production:** It's recommended to implement API key authentication or rate limiting for production deployments.

---

## Endpoints

### GET /

Root endpoint providing service information.

**URL:** `/`

**Method:** `GET`

**Response:**

```json
{
  "service": "OwnVoice TTS Server",
  "version": "1.0.0",
  "status": "running",
  "endpoints": {
    "synthesize": "POST /synthesize",
    "health": "GET /health",
    "languages": "GET /languages",
    "voices": "GET /voices"
  }
}
```

**Status Codes:**
- `200 OK` - Service is running

**Example:**

```bash
curl http://nn-voice.icefelix.com/
```

---

### GET /health

Health check endpoint for monitoring service availability.

**URL:** `/health`

**Method:** `GET`

**Response:**

```json
{
  "status": "healthy",
  "service": "OwnVoice TTS",
  "version": "1.0.0",
  "timestamp": "2026-02-11T09:34:20.255034",
  "cache": {
    "directory": "cache",
    "files": 42
  },
  "supported_languages": 8
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | Service health status (`healthy` or `unhealthy`) |
| `service` | string | Service name |
| `version` | string | API version |
| `timestamp` | string | Current server timestamp (ISO 8601) |
| `cache.directory` | string | Cache directory path |
| `cache.files` | integer | Number of cached audio files |
| `supported_languages` | integer | Total supported languages |

**Status Codes:**
- `200 OK` - Service is healthy

**Example:**

```bash
curl http://nn-voice.icefelix.com/health
```

---

### GET /languages

List all supported languages for text-to-speech synthesis.

**URL:** `/languages`

**Method:** `GET`

**Response:**

```json
{
  "languages": [
    {
      "code": "ro",
      "name": "Romanian"
    },
    {
      "code": "ro-f",
      "name": "Romanian (Female)"
    },
    {
      "code": "en",
      "name": "English"
    },
    {
      "code": "es",
      "name": "Spanish"
    },
    {
      "code": "fr",
      "name": "French"
    },
    {
      "code": "de",
      "name": "German"
    },
    {
      "code": "it",
      "name": "Italian"
    },
    {
      "code": "pt",
      "name": "Portuguese"
    }
  ]
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `languages` | array | Array of language objects |
| `languages[].code` | string | Language code (ISO 639-1) |
| `languages[].name` | string | Language display name |

**Status Codes:**
- `200 OK` - Languages retrieved successfully

**Example:**

```bash
curl http://nn-voice.icefelix.com/languages
```

---

### GET /voices

List all available voices per language.

**URL:** `/voices`

**Method:** `GET`

**Response:**

```json
{
  "voices": [
    {
      "id": "ro",
      "name": "Romanian (Default)",
      "language": "ro"
    },
    {
      "id": "ro-f",
      "name": "Romanian (Female) (Default)",
      "language": "ro-f"
    },
    {
      "id": "en",
      "name": "English (Default)",
      "language": "en"
    }
  ]
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `voices` | array | Array of voice objects |
| `voices[].id` | string | Voice identifier |
| `voices[].name` | string | Voice display name |
| `voices[].language` | string | Language code for this voice |

**Status Codes:**
- `200 OK` - Voices retrieved successfully

**Example:**

```bash
curl http://nn-voice.icefelix.com/voices
```

---

### POST /synthesize

**Main Endpoint** - Synthesize text to speech and return audio file.

**URL:** `/synthesize`

**Method:** `POST`

**Content-Type:** `multipart/form-data`

**Request Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `text` | string | **Yes** | - | Text to synthesize (max 5000 characters) |
| `lang` | string | No | `ro` | Language code (ro, en, es, fr, de, it, pt) |
| `voice` | string | No | - | Voice ID (currently not used with gTTS) |

**Request Example:**

```bash
curl -X POST "http://nn-voice.icefelix.com/synthesize" \
  -F "text=Bună ziua! Cum te numești?" \
  -F "lang=ro" \
  -o output.mp3
```

**Response:**

Binary audio file in MP3 format.

**Response Headers:**

```
Content-Type: audio/mpeg
Content-Disposition: attachment; filename="speech_<hash>.mp3"
```

**Status Codes:**
- `200 OK` - Audio generated successfully
- `400 Bad Request` - Invalid parameters (empty text, unsupported language)
- `500 Internal Server Error` - TTS generation failed

**Error Response (400):**

```json
{
  "detail": "Text cannot be empty"
}
```

or

```json
{
  "detail": "Unsupported language: xx. Supported: ro, ro-f, en, es, fr, de, it, pt"
}
```

**Error Response (500):**

```json
{
  "detail": "Failed to generate speech: <error_message>"
}
```

**Supported Languages:**

| Code | Language | Description |
|------|----------|-------------|
| `ro` | Romanian | Default Romanian voice |
| `ro-f` | Romanian (Female) | Alias for Romanian (same as `ro` with gTTS) |
| `en` | English | English voice |
| `es` | Spanish | Spanish voice |
| `fr` | French | French voice |
| `de` | German | German voice |
| `it` | Italian | Italian voice |
| `pt` | Portuguese | Portuguese voice |

**Caching:**

The service automatically caches generated audio files based on text and language. Subsequent requests with the same text and language will return cached audio instantly.

**Text Limitations:**

- Maximum text length: 5000 characters
- Minimum text length: 1 character
- Empty or whitespace-only text will return an error

**Examples:**

**Romanian Text:**

```bash
curl -X POST "http://nn-voice.icefelix.com/synthesize" \
  -F "text=Bună ziua! Acesta este un test al serviciului de sinteză vocală." \
  -F "lang=ro" \
  -o romanian.mp3
```

**English Text:**

```bash
curl -X POST "http://nn-voice.icefelix.com/synthesize" \
  -F "text=Hello! This is a test of the text-to-speech service." \
  -F "lang=en" \
  -o english.mp3
```

**Long Text:**

```bash
curl -X POST "http://nn-voice.icefelix.com/synthesize" \
  -F "text=Acesta este un text mai lung care va fi convertit în vorbire. Serviciul OwnVoice TTS suportă texte de până la 5000 de caractere și folosește tehnologia Google Text-to-Speech pentru o calitate excelentă a vocii." \
  -F "lang=ro" \
  -o long_text.mp3
```

**French Text:**

```bash
curl -X POST "http://nn-voice.icefelix.com/synthesize" \
  -F "text=Bonjour! Comment allez-vous aujourd'hui?" \
  -F "lang=fr" \
  -o french.mp3
```

---

## Error Handling

All errors follow a consistent JSON format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

**Common Error Scenarios:**

### 400 Bad Request

**Cause:** Invalid request parameters

**Examples:**
- Empty text field
- Unsupported language code
- Text exceeds 5000 characters

**Solution:** Check request parameters and ensure they meet requirements

### 500 Internal Server Error

**Cause:** Server-side error during TTS generation

**Examples:**
- gTTS service unavailable
- File system issues
- Network problems

**Solution:** Retry the request or contact support if the issue persists

---

## Rate Limiting

Currently, no rate limiting is implemented. However, consider implementing rate limiting in production:

**Recommended Limits:**
- 100 requests per minute per IP
- 1000 requests per hour per IP
- 10MB maximum audio file size

---

## Examples

### Python

```python
import requests

# Synthesize Romanian text
response = requests.post(
    'http://nn-voice.icefelix.com/synthesize',
    data={
        'text': 'Bună ziua! Cum te numești?',
        'lang': 'ro'
    }
)

with open('romanian.mp3', 'wb') as f:
    f.write(response.content)
```

### JavaScript (Node.js)

```javascript
const axios = require('axios');
const fs = require('fs');
const FormData = require('form-data');

const form = new FormData();
form.append('text', 'Hello! How are you?');
form.append('lang', 'en');

axios.post('http://nn-voice.icefelix.com/synthesize', form, {
    headers: form.getHeaders(),
    responseType: 'arraybuffer'
})
.then(response => {
    fs.writeFileSync('english.mp3', response.data);
    console.log('Audio saved successfully');
})
.catch(error => {
    console.error('Error:', error.message);
});
```

### PHP

```php
<?php
$ch = curl_init();

curl_setopt($ch, CURLOPT_URL, 'http://nn-voice.icefelix.com/synthesize');
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, [
    'text' => 'Bună ziua! Cum te numești?',
    'lang' => 'ro'
]);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$audio = curl_exec($ch);
curl_close($ch);

file_put_contents('romanian.mp3', $audio);
?>
```

### cURL

```bash
# Basic usage
curl -X POST "http://nn-voice.icefelix.com/synthesize" \
  -F "text=Hello World" \
  -F "lang=en" \
  -o output.mp3

# With verbose output
curl -v -X POST "http://nn-voice.icefelix.com/synthesize" \
  -F "text=Bună ziua" \
  -F "lang=ro" \
  -o romanian.mp3

# Check file size
curl -X POST "http://nn-voice.icefelix.com/synthesize" \
  -F "text=Test text" \
  -F "lang=en" \
  -o test.mp3 && ls -lh test.mp3
```

---

## Performance Considerations

### Caching

The service implements automatic caching:
- Cache key: MD5 hash of (text + language)
- Cache location: `cache/` directory on server
- Cache expiration: No automatic expiration (manual cleanup required)
- Cache benefits: Instant response for repeated requests

### Response Times

**First request (no cache):**
- Short text (<50 chars): ~1-2 seconds
- Medium text (50-500 chars): ~2-4 seconds
- Long text (500-5000 chars): ~4-8 seconds

**Cached requests:**
- Any text length: <100ms

### Audio File Sizes

Approximate MP3 file sizes:
- 10 words: ~5-10 KB
- 50 words: ~20-30 KB
- 100 words: ~40-60 KB
- 500 words: ~200-300 KB

---

## Best Practices

1. **Always handle errors gracefully** - Check response status codes
2. **Cache audio files client-side** - Don't re-request the same audio
3. **Validate text length** - Stay under 5000 characters
4. **Use appropriate language codes** - Check supported languages first
5. **Stream audio when possible** - Don't load entire file into memory

---

## Support & Contact

- **GitHub Issues:** https://github.com/AlexBordei/ownvoice-tts/issues
- **Documentation:** https://github.com/AlexBordei/ownvoice-tts
- **Server Status:** http://nn-voice.icefelix.com/health

---

## Changelog

### Version 1.0.0 (2026-02-11)

- Initial release
- Support for 8 languages (ro, ro-f, en, es, fr, de, it, pt)
- Automatic caching
- RESTful API with 5 endpoints
- Health monitoring
- Production deployment on nn-voice.icefelix.com

---

**Last Updated:** February 11, 2026
