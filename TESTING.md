# Testing Guide - OwnVoice TTS

Complete guide for testing the OwnVoice TTS API.

## Quick Start

### Using Python Test Script

```bash
# Install requests library
pip install requests

# Run the test script
python test_tts.py
```

The script will:
- ✅ Test all API endpoints
- ✅ Generate audio in Romanian and English
- ✅ Test caching functionality
- ✅ Test error handling
- ✅ Save all generated audio files to `test_output/` directory
- ✅ Provide detailed colored output

### Using Postman

1. **Import Collection**
   - Open Postman
   - Click "Import"
   - Select `OwnVoice-TTS.postman_collection.json`

2. **Set Base URL Variable**
   - Collection is pre-configured with `http://nn-voice.icefelix.com`
   - To test locally, change `base_url` variable to `http://localhost:8001`

3. **Run Tests**
   - Expand folders: Health & Info, Languages & Voices, Text-to-Speech Synthesis
   - Click "Send" on any request
   - Audio files can be saved from response

### Using cURL

**Health Check:**
```bash
curl http://nn-voice.icefelix.com/health
```

**Romanian TTS:**
```bash
curl -X POST "http://nn-voice.icefelix.com/synthesize" \
  -F "text=Bună ziua! Cum te numești?" \
  -F "lang=ro" \
  -o romanian.mp3
```

**English TTS:**
```bash
curl -X POST "http://nn-voice.icefelix.com/synthesize" \
  -F "text=Hello! How are you?" \
  -F "lang=en" \
  -o english.mp3
```

## Test Script Details

### What Gets Tested

1. **Root Endpoint** (`GET /`)
   - Service information
   - Available endpoints

2. **Health Check** (`GET /health`)
   - Service status
   - Cache statistics
   - Supported languages count

3. **Languages** (`GET /languages`)
   - List all supported languages
   - Verify language codes and names

4. **Voices** (`GET /voices`)
   - List all available voices
   - Verify voice metadata

5. **Text-to-Speech Synthesis** (`POST /synthesize`)
   - **Romanian**: short, medium, and long texts
   - **English**: short, medium, and long texts
   - File size validation
   - Audio quality check

6. **Cache Functionality**
   - First request timing
   - Second request timing (should be faster)
   - Cache speedup calculation

7. **Error Handling**
   - Empty text validation
   - Invalid language code
   - Missing parameters

### Test Output

The script creates a `test_output/` directory containing:
- `ro_short_<timestamp>.mp3` - Romanian short text
- `ro_medium_<timestamp>.mp3` - Romanian medium text
- `ro_long_<timestamp>.mp3` - Romanian long text
- `en_short_<timestamp>.mp3` - English short text
- `en_medium_<timestamp>.mp3` - English medium text
- `en_long_<timestamp>.mp3` - English long text

### Expected Results

**Successful Test Run:**
```
================================================================================
                          OwnVoice TTS - Comprehensive Test Suite
================================================================================

ℹ Base URL: http://nn-voice.icefelix.com
ℹ Timeout: 30s
ℹ Test Start: 2026-02-11 12:00:00
ℹ Output directory: /path/to/test_output

================================================================================
                              Testing Root Endpoint
================================================================================

✓ Status Code: 200
ℹ Service: OwnVoice TTS Server
ℹ Version: 1.0.0
ℹ Status: running

... (more tests)

================================================================================
                                 Test Summary
================================================================================

Total Tests: 19
✓ Passed: 19
ℹ Failed: 0

Success Rate: 100.0%

🎉 All tests passed!
```

### Exit Codes

- `0` - All tests passed
- `1` - One or more tests failed or error occurred

## Manual Testing Checklist

### Basic Functionality

- [ ] Service is accessible at http://nn-voice.icefelix.com
- [ ] Health endpoint returns status "healthy"
- [ ] Languages endpoint returns 8 languages
- [ ] Voices endpoint returns 8 voices

### Romanian Synthesis

- [ ] Short text (< 20 chars) generates audio
- [ ] Medium text (20-100 chars) generates audio
- [ ] Long text (> 100 chars) generates audio
- [ ] Audio file plays correctly
- [ ] Audio is in Romanian language

### English Synthesis

- [ ] Short text (< 20 chars) generates audio
- [ ] Medium text (20-100 chars) generates audio
- [ ] Long text (> 100 chars) generates audio
- [ ] Audio file plays correctly
- [ ] Audio is in English language

### Performance

- [ ] First request completes in < 5 seconds
- [ ] Cached request completes in < 1 second
- [ ] Cache is used for identical requests
- [ ] File sizes are reasonable (< 100KB for short texts)

### Error Handling

- [ ] Empty text returns 400 error
- [ ] Invalid language returns 400 error
- [ ] Missing parameters return 422 error
- [ ] Error messages are descriptive

### Multi-Language Support

- [ ] Spanish (es) synthesis works
- [ ] French (fr) synthesis works
- [ ] German (de) synthesis works
- [ ] Italian (it) synthesis works
- [ ] Portuguese (pt) synthesis works

## Performance Benchmarks

Expected response times (first request, no cache):

| Text Length | Romanian | English |
|-------------|----------|---------|
| Short (< 20 chars) | ~1-2s | ~1-2s |
| Medium (20-100 chars) | ~2-3s | ~2-3s |
| Long (> 100 chars) | ~3-5s | ~3-5s |

Expected file sizes:

| Text Length | File Size |
|-------------|-----------|
| Short | 5-15 KB |
| Medium | 20-40 KB |
| Long | 50-100 KB |

## Troubleshooting

### Connection Errors

**Problem:** `Connection refused` or `Connection timeout`

**Solutions:**
1. Check if service is running: `systemctl status ownvoice-tts`
2. Check if nginx is running: `systemctl status nginx`
3. Verify DNS resolution: `ping nn-voice.icefelix.com`
4. Check firewall rules: `sudo ufw status`

### Audio Not Playing

**Problem:** Downloaded MP3 file won't play

**Solutions:**
1. Verify file size is > 0: `ls -lh audio.mp3`
2. Check file format: `file audio.mp3` (should say "Audio file with ID3")
3. Try different audio player
4. Check if gTTS service is working on server

### Cache Not Working

**Problem:** Second request is not faster than first

**Solutions:**
1. Check cache directory exists: `ls -la cache/`
2. Check permissions: `ls -l cache/`
3. Verify cache files are created: `ls cache/*.mp3`
4. Check server logs: `journalctl -u ownvoice-tts -f`

### High Response Times

**Problem:** Requests take > 10 seconds

**Solutions:**
1. Check server load: `top` or `htop`
2. Check network latency: `ping nn-voice.icefelix.com`
3. Check if gTTS API is responsive
4. Review server logs for errors

## Continuous Integration

### GitHub Actions Example

```yaml
name: API Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install requests
      - name: Run tests
        run: python test_tts.py
```

## Load Testing

For load testing, use tools like:

**Apache Bench:**
```bash
ab -n 100 -c 10 http://nn-voice.icefelix.com/health
```

**wrk:**
```bash
wrk -t12 -c400 -d30s http://nn-voice.icefelix.com/health
```

## Security Testing

Check for:
- [ ] HTTPS support (if configured)
- [ ] Rate limiting (if configured)
- [ ] Input validation
- [ ] XSS protection
- [ ] SQL injection protection (N/A for this service)

## Need Help?

- **GitHub Issues:** https://github.com/AlexBordei/ownvoice-tts/issues
- **Documentation:** [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- **Server Health:** http://nn-voice.icefelix.com/health
