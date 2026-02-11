#!/usr/bin/env python3
"""Quick test for speed parameter"""

import requests
import subprocess
from pathlib import Path

BASE_URL = "http://nn-voice.icefelix.com"
OUTPUT_DIR = Path("speed_test")
OUTPUT_DIR.mkdir(exist_ok=True)

tests = [
    {"text": "Bună ziua! Acesta este un test de viteză.", "lang": "ro", "speed": 1.0, "label": "normal"},
    {"text": "Bună ziua! Acesta este un test de viteză.", "lang": "ro", "speed": 1.25, "label": "fast"},
    {"text": "Bună ziua! Acesta este un test de viteză.", "lang": "ro", "speed": 1.5, "label": "very_fast"},
]

print("🧪 Testing Speed Parameter\n")

for test in tests:
    print(f"Testing {test['label']} ({test['speed']}x)...")

    response = requests.post(
        f"{BASE_URL}/synthesize",
        data={
            'text': test['text'],
            'lang': test['lang'],
            'speed': test['speed']
        }
    )

    if response.status_code == 200:
        filename = f"{test['lang']}_{test['label']}_{test['speed']}x.mp3"
        filepath = OUTPUT_DIR / filename

        with open(filepath, 'wb') as f:
            f.write(response.content)

        file_size = filepath.stat().st_size / 1024
        print(f"  ✅ Generated: {filename} ({file_size:.2f} KB)")

        # Play audio
        print(f"  🔊 Playing...")
        subprocess.run(['afplay', str(filepath)])
        print()
    else:
        print(f"  ❌ Error: {response.status_code}")
        print(f"     {response.text}\n")

print("✅ All tests completed!")
