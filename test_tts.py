#!/usr/bin/env python3
"""
OwnVoice TTS - Comprehensive Testing Script

Tests all API endpoints for Romanian and English languages.
Includes health checks, language listing, and audio synthesis.

Usage:
    python test_tts.py
"""

import requests
import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

# Configuration
BASE_URL = "http://nn-voice.icefelix.com"
OUTPUT_DIR = Path("test_output")
TIMEOUT = 30  # seconds

# Test texts
TEST_TEXTS = {
    "ro": {
        "short": "Bună ziua!",
        "medium": "Bună ziua! Cum te numești? Mă numesc OwnVoice și sunt un serviciu de sinteză vocală.",
        "long": """Acesta este un test mai lung al serviciului OwnVoice TTS în limba română.
        Serviciul nostru folosește tehnologia Google Text-to-Speech pentru a genera audio de înaltă calitate.
        Puteți folosi acest serviciu pentru aplicații de e-learning, asistență vocală,
        sau orice altă aplicație care necesită conversie text-to-speech.
        Serviciul este rapid, eficient și oferă suport pentru cache-uire automată."""
    },
    "en": {
        "short": "Hello!",
        "medium": "Hello! How are you today? My name is OwnVoice and I am a text-to-speech service.",
        "long": """This is a longer test of the OwnVoice TTS service in English.
        Our service uses Google Text-to-Speech technology to generate high-quality audio.
        You can use this service for e-learning applications, voice assistance,
        or any other application that requires text-to-speech conversion.
        The service is fast, efficient, and supports automatic caching."""
    }
}

# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(text: str):
    """Print formatted header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text:^80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.ENDC}\n")


def print_success(text: str):
    """Print success message"""
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")


def print_error(text: str):
    """Print error message"""
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")


def print_info(text: str):
    """Print info message"""
    print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")


def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")


def setup_output_dir():
    """Create output directory for test audio files"""
    OUTPUT_DIR.mkdir(exist_ok=True)
    print_info(f"Output directory: {OUTPUT_DIR.absolute()}")


def test_root_endpoint() -> bool:
    """Test GET / endpoint"""
    print_header("Testing Root Endpoint")

    try:
        response = requests.get(f"{BASE_URL}/", timeout=TIMEOUT)

        if response.status_code == 200:
            data = response.json()
            print_success(f"Status Code: {response.status_code}")
            print_info(f"Service: {data.get('service')}")
            print_info(f"Version: {data.get('version')}")
            print_info(f"Status: {data.get('status')}")
            print_info(f"Available Endpoints: {', '.join(data.get('endpoints', {}).keys())}")
            return True
        else:
            print_error(f"Unexpected status code: {response.status_code}")
            return False

    except requests.exceptions.RequestException as e:
        print_error(f"Request failed: {e}")
        return False


def test_health_endpoint() -> bool:
    """Test GET /health endpoint"""
    print_header("Testing Health Endpoint")

    try:
        response = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)

        if response.status_code == 200:
            data = response.json()
            print_success(f"Status Code: {response.status_code}")
            print_info(f"Service Status: {data.get('status')}")
            print_info(f"Service Name: {data.get('service')}")
            print_info(f"Version: {data.get('version')}")
            print_info(f"Timestamp: {data.get('timestamp')}")

            cache_info = data.get('cache', {})
            print_info(f"Cache Directory: {cache_info.get('directory')}")
            print_info(f"Cached Files: {cache_info.get('files')}")
            print_info(f"Supported Languages: {data.get('supported_languages')}")

            return data.get('status') == 'healthy'
        else:
            print_error(f"Unexpected status code: {response.status_code}")
            return False

    except requests.exceptions.RequestException as e:
        print_error(f"Request failed: {e}")
        return False


def test_languages_endpoint() -> Tuple[bool, List[str]]:
    """Test GET /languages endpoint"""
    print_header("Testing Languages Endpoint")

    try:
        response = requests.get(f"{BASE_URL}/languages", timeout=TIMEOUT)

        if response.status_code == 200:
            data = response.json()
            languages = data.get('languages', [])

            print_success(f"Status Code: {response.status_code}")
            print_info(f"Total Languages: {len(languages)}")

            language_codes = []
            for lang in languages:
                code = lang.get('code')
                name = lang.get('name')
                language_codes.append(code)
                print_info(f"  • {code}: {name}")

            return True, language_codes
        else:
            print_error(f"Unexpected status code: {response.status_code}")
            return False, []

    except requests.exceptions.RequestException as e:
        print_error(f"Request failed: {e}")
        return False, []


def test_voices_endpoint() -> bool:
    """Test GET /voices endpoint"""
    print_header("Testing Voices Endpoint")

    try:
        response = requests.get(f"{BASE_URL}/voices", timeout=TIMEOUT)

        if response.status_code == 200:
            data = response.json()
            voices = data.get('voices', [])

            print_success(f"Status Code: {response.status_code}")
            print_info(f"Total Voices: {len(voices)}")

            for voice in voices:
                voice_id = voice.get('id')
                name = voice.get('name')
                language = voice.get('language')
                print_info(f"  • {voice_id} ({language}): {name}")

            return True
        else:
            print_error(f"Unexpected status code: {response.status_code}")
            return False

    except requests.exceptions.RequestException as e:
        print_error(f"Request failed: {e}")
        return False


def test_synthesize(text: str, lang: str, label: str) -> Tuple[bool, str]:
    """Test POST /synthesize endpoint"""

    try:
        data = {
            'text': text,
            'lang': lang
        }

        response = requests.post(
            f"{BASE_URL}/synthesize",
            data=data,
            timeout=TIMEOUT
        )

        if response.status_code == 200:
            # Save audio file
            filename = f"{lang}_{label}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
            filepath = OUTPUT_DIR / filename

            with open(filepath, 'wb') as f:
                f.write(response.content)

            file_size = filepath.stat().st_size
            file_size_kb = file_size / 1024

            print_success(f"{label.capitalize()} ({lang}): {response.status_code}")
            print_info(f"  Text length: {len(text)} characters")
            print_info(f"  File size: {file_size_kb:.2f} KB")
            print_info(f"  Saved to: {filename}")

            return True, str(filepath)
        else:
            print_error(f"{label.capitalize()} ({lang}): {response.status_code}")
            print_error(f"  Response: {response.text}")
            return False, ""

    except requests.exceptions.RequestException as e:
        print_error(f"{label.capitalize()} ({lang}): Request failed - {e}")
        return False, ""


def test_all_synthesis():
    """Test synthesis for all text lengths and languages"""
    print_header("Testing Text-to-Speech Synthesis")

    results = {
        'passed': 0,
        'failed': 0,
        'total': 0
    }

    for lang, texts in TEST_TEXTS.items():
        print(f"\n{Colors.OKBLUE}{Colors.BOLD}Language: {lang.upper()}{Colors.ENDC}")
        print("-" * 80)

        for label, text in texts.items():
            results['total'] += 1
            success, filepath = test_synthesize(text, lang, label)

            if success:
                results['passed'] += 1
            else:
                results['failed'] += 1

    return results


def test_caching():
    """Test caching functionality by making duplicate requests"""
    print_header("Testing Cache Functionality")

    test_text = "Test text for caching"
    test_lang = "en"

    print_info("Making first request (should generate new audio)...")

    start_time = datetime.now()
    response1 = requests.post(
        f"{BASE_URL}/synthesize",
        data={'text': test_text, 'lang': test_lang},
        timeout=TIMEOUT
    )
    first_duration = (datetime.now() - start_time).total_seconds()

    if response1.status_code != 200:
        print_error("First request failed")
        return False

    print_success(f"First request completed in {first_duration:.3f}s")

    print_info("Making second request (should use cache)...")

    start_time = datetime.now()
    response2 = requests.post(
        f"{BASE_URL}/synthesize",
        data={'text': test_text, 'lang': test_lang},
        timeout=TIMEOUT
    )
    second_duration = (datetime.now() - start_time).total_seconds()

    if response2.status_code != 200:
        print_error("Second request failed")
        return False

    print_success(f"Second request completed in {second_duration:.3f}s")

    # Cache should be significantly faster
    speedup = first_duration / second_duration if second_duration > 0 else 0

    if second_duration < first_duration:
        print_success(f"Cache is working! Speedup: {speedup:.2f}x faster")
        return True
    else:
        print_warning("Cache might not be working (second request wasn't faster)")
        return False


def test_error_handling():
    """Test error handling for invalid inputs"""
    print_header("Testing Error Handling")

    test_cases = [
        {
            'name': 'Empty text',
            'data': {'text': '', 'lang': 'ro'},
            'expected_status': 400
        },
        {
            'name': 'Invalid language',
            'data': {'text': 'Test', 'lang': 'invalid_lang'},
            'expected_status': 400
        },
        {
            'name': 'Missing text parameter',
            'data': {'lang': 'ro'},
            'expected_status': 422  # FastAPI validation error
        }
    ]

    passed = 0
    failed = 0

    for test in test_cases:
        try:
            response = requests.post(
                f"{BASE_URL}/synthesize",
                data=test.get('data'),
                timeout=TIMEOUT
            )

            if response.status_code == test['expected_status']:
                print_success(f"{test['name']}: Got expected status {response.status_code}")
                passed += 1
            else:
                print_error(f"{test['name']}: Expected {test['expected_status']}, got {response.status_code}")
                failed += 1

        except requests.exceptions.RequestException as e:
            print_error(f"{test['name']}: Request failed - {e}")
            failed += 1

    return passed, failed


def print_summary(results: Dict):
    """Print test summary"""
    print_header("Test Summary")

    total_tests = sum(results.values())
    passed_tests = results.get('passed', 0)
    failed_tests = results.get('failed', 0)

    success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0

    print(f"Total Tests: {total_tests}")
    print_success(f"Passed: {passed_tests}")

    if failed_tests > 0:
        print_error(f"Failed: {failed_tests}")
    else:
        print_info(f"Failed: {failed_tests}")

    print(f"\nSuccess Rate: {success_rate:.1f}%")

    if success_rate == 100:
        print(f"\n{Colors.OKGREEN}{Colors.BOLD}🎉 All tests passed!{Colors.ENDC}")
    elif success_rate >= 80:
        print(f"\n{Colors.WARNING}{Colors.BOLD}⚠ Most tests passed, but some failed{Colors.ENDC}")
    else:
        print(f"\n{Colors.FAIL}{Colors.BOLD}❌ Many tests failed{Colors.ENDC}")


def main():
    """Main test execution"""
    print(f"{Colors.BOLD}{Colors.HEADER}")
    print("=" * 80)
    print("OwnVoice TTS - Comprehensive Test Suite".center(80))
    print("=" * 80)
    print(f"{Colors.ENDC}")

    print_info(f"Base URL: {BASE_URL}")
    print_info(f"Timeout: {TIMEOUT}s")
    print_info(f"Test Start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Setup
    setup_output_dir()

    # Track overall results
    all_results = {
        'passed': 0,
        'failed': 0
    }

    # Test 1: Root endpoint
    if test_root_endpoint():
        all_results['passed'] += 1
    else:
        all_results['failed'] += 1

    # Test 2: Health endpoint
    if test_health_endpoint():
        all_results['passed'] += 1
    else:
        all_results['failed'] += 1

    # Test 3: Languages endpoint
    success, languages = test_languages_endpoint()
    if success:
        all_results['passed'] += 1
    else:
        all_results['failed'] += 1

    # Test 4: Voices endpoint
    if test_voices_endpoint():
        all_results['passed'] += 1
    else:
        all_results['failed'] += 1

    # Test 5: Synthesis for all languages
    synthesis_results = test_all_synthesis()
    all_results['passed'] += synthesis_results['passed']
    all_results['failed'] += synthesis_results['failed']

    # Test 6: Caching
    if test_caching():
        all_results['passed'] += 1
    else:
        all_results['failed'] += 1

    # Test 7: Error handling
    error_passed, error_failed = test_error_handling()
    all_results['passed'] += error_passed
    all_results['failed'] += error_failed

    # Print summary
    print_summary(all_results)

    print_info(f"\nTest End: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print_info(f"Audio files saved to: {OUTPUT_DIR.absolute()}")

    # Exit with appropriate code
    sys.exit(0 if all_results['failed'] == 0 else 1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}Test interrupted by user{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n{Colors.FAIL}Unexpected error: {e}{Colors.ENDC}")
        sys.exit(1)
