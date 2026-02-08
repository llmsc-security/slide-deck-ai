#!/usr/bin/env python3
"""
Tutorial PoC - HTTP API Test Client for SlideDeck AI Streamlit App

This script demonstrates how to interact with the SlideDeck AI application
via HTTP requests. It shows how to:
1. Test if the server is running
2. Get application information
3. Test chat/stream endpoints (if available)
4. Download generated slide decks

Note: This is a PoC (Proof of Concept) script. The actual API endpoints
may vary depending on the Streamlit app's implementation.
"""

import requests
import json
import sys
import time
from typing import Optional, Dict, Any, List


class SlideDeckAIClient:
    """
    HTTP client for testing SlideDeck AI Streamlit application.
    """

    def __init__(self, base_url: str = "http://localhost:8501"):
        """
        Initialize the client.

        Args:
            base_url: Base URL of the Streamlit app (default: http://localhost:8501)
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()

    def check_health(self) -> Dict[str, Any]:
        """
        Check if the server is running and responsive.

        Returns:
            Dictionary with health check results.
        """
        try:
            response = self.session.get(f"{self.base_url}/health")
            return {
                "status": "ok",
                "code": response.status_code,
                "data": response.json()
            }
        except requests.exceptions.ConnectionError:
            return {
                "status": "error",
                "message": "Could not connect to server"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def get_page(self, path: str = "/") -> Dict[str, Any]:
        """
        Fetch a page from the Streamlit app.

        Args:
            path: The path to fetch (default: root "/")

        Returns:
            Dictionary with page content info.
        """
        try:
            response = self.session.get(f"{self.base_url}{path}")
            return {
                "status": "ok",
                "code": response.status_code,
                "headers": dict(response.headers),
                "content_length": len(response.content)
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def test_homepage(self) -> Dict[str, Any]:
        """
        Test the homepage/load.

        Returns:
            Dictionary with test results.
        """
        print("=" * 60)
        print("SlideDeck AI - HTTP API Test Client")
        print("=" * 60)
        print(f"\nTesting against: {self.base_url}")
        print("-" * 60)

        # Check if server is reachable
        print("\n[1] Checking server health...")
        health = self.check_health()
        if health["status"] == "ok":
            print(f"    ✓ Server is running (HTTP {health['code']})")
        else:
            print(f"    ✗ Server check failed: {health.get('message', 'Unknown error')}")
            print("\n    Make sure the Streamlit app is running:")
            print(f"    cd /path/to/slide-deck-ai && streamlit run app.py --server.port=8501")
            return {"success": False}

        # Test homepage
        print("\n[2] Fetching homepage...")
        result = self.get_page("/")
        if result["status"] == "ok":
            print(f"    ✓ Homepage fetched (HTTP {result['code']})")
            print(f"    Content-Length: {result.get('content_length', 'N/A')} bytes")
        else:
            print(f"    ✗ Failed: {result.get('message', 'Unknown error')}")
            return {"success": False}

        # Test common endpoints
        print("\n[3] Testing common endpoints...")
        endpoints = ["/_stcore/health", "/robots.txt", "/favicon.ico"]
        for endpoint in endpoints:
            r = self.get_page(endpoint)
            if r["status"] == "ok":
                print(f"    ✓ {endpoint} - HTTP {r['code']}")
            else:
                print(f"    - {endpoint} - Not available")

        # Check for Streamlit protocol
        print("\n[4] Testing Streamlit WebSocket protocol...")
        try:
            ws_url = self.base_url.replace('http://', 'ws://') + "/ws"
            print(f"    WebSocket URL: {ws_url}")
            print("    (Note: Full WebSocket testing requires websocket-client)")
        except Exception as e:
            print(f"    Note: {e}")

        print("\n" + "=" * 60)
        print("Basic HTTP connectivity test completed!")
        print("=" * 60)
        print("\nTo test the full application:")
        print("1. Open the Streamlit app in your browser")
        print(f"2. Navigate to: {self.base_url}")
        print("3. Use the UI to generate slides or chat with AI")
        print("\nFor programmatic testing:")
        print("- Check the app.py source for API endpoints")
        print("- Consider using the official SlideDeck AI SDK if available")
        print("=" * 60)

        return {"success": True}

    def generate_slide_deck(self, prompt: str, api_key: Optional[str] = None) -> Dict[str, Any]:
        """
        Attempt to generate a slide deck via API.

        Note: This is a Streamlit app, so direct API access may not be available.
        This method attempts to find and use any available API endpoints.

        Args:
            prompt: The prompt for slide generation
            api_key: Optional API key for LLM provider

        Returns:
            Dictionary with generation results.
        """
        print("\n" + "=" * 60)
        print("Slide Deck Generation Test")
        print("=" * 60)

        # Check for potential API endpoints
        api_endpoints = [
            "/api/generate",
            "/api/slide",
            "/api/v1/generate",
            "/api/generate_slides",
            "/generate",
        ]

        for endpoint in api_endpoints:
            print(f"\n[?] Trying endpoint: {endpoint}")
            try:
                payload = {
                    "prompt": prompt,
                    "api_key": api_key
                }
                response = self.session.post(
                    f"{self.base_url}{endpoint}",
                    json=payload,
                    timeout=30
                )
                print(f"    Status: {response.status_code}")
                if response.status_code == 200:
                    try:
                        data = response.json()
                        print(f"    Response: {json.dumps(data, indent=2)}")
                        return {"success": True, "data": data}
                    except:
                        print(f"    Content: {response.text[:500]}")
            except requests.exceptions.ConnectionError:
                print("    Connection failed")
                break
            except Exception as e:
                print(f"    Error: {e}")

        print("\nNote: The SlideDeck AI app is a Streamlit application.")
        print("It does not expose a traditional REST API by default.")
        print("\nRecommended alternatives:")
        print("1. Use the web UI directly at: http://localhost:8501")
        print("2. Check if the app has a backend API in src/ directory")
        print("3. Consider running the app with --server.enableXsrfProtection=false")
        print("=" * 60)

        return {"success": False, "message": "No API endpoint found"}


def main():
    """
    Main entry point for the test client.
    """
    # Default URL - change if running on different host/port
    base_url = "http://localhost:8501"

    # Parse command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] in ["--help", "-h"]:
            print(__doc__)
            print("\nUsage:")
            print("  python tutorial_poc.py                    # Run basic tests")
            print("  python tutorial_poc.py <base_url>         # Test at custom URL")
            print("  python tutorial_poc.py <prompt>           # Test with prompt")
            sys.exit(0)
        else:
            base_url = sys.argv[1]

    # Create client
    client = SlideDeckAIClient(base_url)

    # Run tests
    result = client.test_homepage()

    if result["success"]:
        # If a prompt was provided, try to generate
        if len(sys.argv) > 2:
            prompt = " ".join(sys.argv[2:])
            client.generate_slide_deck(prompt)


if __name__ == "__main__":
    main()
