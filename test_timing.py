#!/usr/bin/env python3
"""
OwnVoice TTS - Performance Timing Test

Measures complete end-to-end timing from request to audio playback.
"""

import requests
import time
import subprocess
import os
from pathlib import Path

BASE_URL = "http://nn-voice.icefelix.com"
OUTPUT_DIR = Path("timing_test")

# ANSI colors
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
BOLD = '\033[1m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BOLD}{BLUE}{'=' * 80}{RESET}")
    print(f"{BOLD}{BLUE}{text:^80}{RESET}")
    print(f"{BOLD}{BLUE}{'=' * 80}{RESET}\n")

def test_tts_timing(text, lang, label):
    """Test TTS with complete timing measurement"""

    print(f"{BOLD}Testing: {label} ({lang}){RESET}")
    print(f"Text: '{text[:50]}{'...' if len(text) > 50 else ''}'\n")

    # 1. Start timing
    start_total = time.time()

    # 2. Make request
    print(f"{BLUE}⏱️  Making API request...{RESET}")
    start_request = time.time()

    response = requests.post(
        f"{BASE_URL}/synthesize",
        data={'text': text, 'lang': lang},
        timeout=30
    )

    request_time = time.time() - start_request
    print(f"{GREEN}✓  Request completed in {request_time:.3f}s{RESET}")

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None

    # 3. Save file
    print(f"{BLUE}💾 Saving audio file...{RESET}")
    start_save = time.time()

    OUTPUT_DIR.mkdir(exist_ok=True)
    filename = f"{lang}_{label}_timing.mp3"
    filepath = OUTPUT_DIR / filename

    with open(filepath, 'wb') as f:
        f.write(response.content)

    save_time = time.time() - start_save
    file_size = filepath.stat().st_size / 1024  # KB

    print(f"{GREEN}✓  File saved in {save_time:.3f}s ({file_size:.2f} KB){RESET}")

    # 4. Play audio (measure playback time)
    print(f"{BLUE}🔊 Playing audio...{RESET}")
    start_play = time.time()

    subprocess.run(['afplay', str(filepath)], check=True)

    play_time = time.time() - start_play
    print(f"{GREEN}✓  Playback completed in {play_time:.3f}s{RESET}")

    # 5. Calculate totals
    total_time = time.time() - start_total
    processing_time = total_time - play_time  # Time without playback

    # Print summary
    print(f"\n{BOLD}{YELLOW}{'─' * 80}{RESET}")
    print(f"{BOLD}Timing Breakdown:{RESET}")
    print(f"  1. API Request:        {request_time:>8.3f}s  ({request_time/total_time*100:>5.1f}%)")
    print(f"  2. File Save:          {save_time:>8.3f}s  ({save_time/total_time*100:>5.1f}%)")
    print(f"  3. Audio Playback:     {play_time:>8.3f}s  ({play_time/total_time*100:>5.1f}%)")
    print(f"  {BOLD}Processing Time:      {processing_time:>8.3f}s  ({processing_time/total_time*100:>5.1f}%){RESET}")
    print(f"  {BOLD}TOTAL TIME:           {total_time:>8.3f}s  (100.0%){RESET}")
    print(f"\n  File Size:            {file_size:>8.2f} KB")
    print(f"  Text Length:          {len(text):>8} chars")
    print(f"{BOLD}{YELLOW}{'─' * 80}{RESET}\n")

    return {
        'request': request_time,
        'save': save_time,
        'play': play_time,
        'processing': processing_time,
        'total': total_time,
        'file_size': file_size,
        'text_length': len(text)
    }

def main():
    print_header("OwnVoice TTS - Performance Timing Test")

    tests = [
        {
            'text': 'Bună ziua!',
            'lang': 'ro',
            'label': 'scurt'
        },
        {
            'text': 'Bună ziua! Cum te numești? Mă numesc OwnVoice și sunt un serviciu de sinteză vocală.',
            'lang': 'ro',
            'label': 'mediu'
        },
        {
            'text': 'Hello! How are you today? My name is OwnVoice and I am a text-to-speech service.',
            'lang': 'en',
            'label': 'medium'
        }
    ]

    results = []

    for i, test in enumerate(tests, 1):
        print(f"\n{BOLD}═══ Test {i}/{len(tests)} ═══{RESET}")
        result = test_tts_timing(test['text'], test['lang'], test['label'])
        if result:
            results.append({**test, **result})
        time.sleep(0.5)  # Small delay between tests

    # Final summary
    print_header("Summary - All Tests")

    print(f"{BOLD}{'Test':<20} {'Request':<10} {'Processing':<12} {'Playback':<10} {'Total':<10}{RESET}")
    print(f"{'─' * 70}")

    for r in results:
        label = f"{r['label']} ({r['lang']})"
        print(f"{label:<20} {r['request']:>8.3f}s  {r['processing']:>10.3f}s  {r['play']:>8.3f}s  {r['total']:>8.3f}s")

    print(f"\n{GREEN}✅ All tests completed!{RESET}")
    print(f"{BLUE}ℹ️  Audio files saved to: {OUTPUT_DIR.absolute()}{RESET}\n")

if __name__ == "__main__":
    main()
