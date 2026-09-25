"""Regression tests. Gemini is always stubbed, so running them costs nothing.

Run: python -m unittest test_app -v
"""

import inspect
import unittest
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

import main
from ai_reader import without_thinking
from doshas import _check_mangal_dosha
from yogas import detect_yogas

SIGNS = ["Mesha", "Vrishabha", "Mithuna", "Karka", "Simha", "Kanya",
         "Tula", "Vrishchika", "Dhanu", "Makara", "Kumbha", "Meena"]
LORDS = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury",
         "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]
BASE = {"Sun": 3, "Moon": 6, "Mars": 11, "Mercury": 3, "Jupiter": 8,
        "Venus": 2, "Saturn": 12, "Rahu": 5, "Ketu": 11}
BIRTH = {"name": "Test", "birth_date": "1990-05-17", "birth_time": "10:30", "birth_city": "Jaipur",
         "latitude": 26.9124, "longitude": 75.7873, "language": "en"}


def make_chart(asc_sign, house_of):
    """Whole-sign chart for a Lagna sign (1-12) from {planet: house}."""
    houses = []
    for h in range(1, 13):
        s = (asc_sign + h - 2) % 12
        houses.append({"house": h, "sign_num": s + 1, "sign": SIGNS[s], "lord": LORDS[s], "planets": []})
    planets = []
    for name, h in house_of.items():
        hd = houses[h - 1]
        planets.append({"name": name, "house": h, "sign_num": hd["sign_num"], "sign": hd["sign"],
                        "lord": hd["lord"], "dignity": "neutral", "longitude": (hd["sign_num"] - 1) * 30 + 15})
    return planets, houses


def yoga_names(asc_sign, house_of):
    planets, houses = make_chart(asc_sign, house_of)
    return [y["name"] for y in detect_yogas(planets, houses, {})]


class YogaRules(unittest.TestCase):
    def test_yogakaraka_raj_yoga_only_for_classical_lagnas(self):
        expected = {2: "Saturn", 7: "Saturn", 4: "Mars", 5: "Mars", 10: "Venus", 11: "Venus"}
        for asc in range(1, 13):
            planets, houses = make_chart(asc, BASE)
            single = [y["planets"][0] for y in detect_yogas(planets, houses, {})
                      if y["name"] == "Raj Yoga" and len(y["planets"]) == 1]
            self.assertEqual(single, [expected[asc]] if asc in expected else [], SIGNS[asc - 1])

    def test_gajakesari_needs_jupiter_in_kendra_from_moon(self):
        for jupiter, present in [(1, True), (4, True), (7, True), (10, True),
                                 (2, False), (5, False), (8, False), (11, False)]:
            names = yoga_names(1, {**BASE, "Moon": 1, "Jupiter": jupiter})
            self.assertEqual("Gajakesari Yoga" in names, present, f"Jupiter in H{jupiter}")

    def test_adhi_yoga_counts_6_7_8_from_moon(self):
        self.assertIn("Adhi Yoga", yoga_names(1, {**BASE, "Moon": 1, "Jupiter": 6, "Venus": 7, "Mercury": 8}))
        self.assertNotIn("Adhi Yoga", yoga_names(1, {**BASE, "Moon": 1, "Jupiter": 9, "Venus": 9, "Mercury": 5}))


class MangalDosha(unittest.TestCase):
    def test_jupiter_aspect_counted_from_jupiter(self):
        for jupiter, aspects in [(1, True), (3, True), (11, True), (12, False), (5, False)]:
            planets, _ = make_chart(1, {**BASE, "Mars": 7, "Jupiter": jupiter})
            cancellation = _check_mangal_dosha(planets)[0]["cancellation"]
            self.assertEqual("Jupiter aspects Mars" in cancellation, aspects, f"Jupiter in H{jupiter}")


class ThinkingBudget(unittest.TestCase):
    def test_zero_budget_only_for_2_5_flash(self):
        payload = {"contents": [], "generationConfig": {"temperature": 0.4}}
        config = without_thinking(payload, "gemini-2.5-flash")["generationConfig"]
        self.assertEqual(config["thinkingConfig"], {"thinkingBudget": 0})
        self.assertNotIn("thinkingConfig", without_thinking(payload, "gemini-2.0-flash")["generationConfig"])
        self.assertNotIn("thinkingConfig", payload["generationConfig"])  # input not mutated


class Api(unittest.TestCase):
    def setUp(self):
        main._ai_usage.clear()
        self.client = TestClient(main.app)

    def ask(self, headers=None, **overrides):
        body = {**BIRTH, "question": "Career?", "history": [], **overrides}
        return self.client.post("/api/ask-jyotishi", json=body,
                                headers=headers or {"CF-Connecting-IP": "1.1.1.1"})

    def test_only_frontend_files_are_public(self):
        for path in ("/", "/app.js", "/style.css", "/favicon.svg"):
            self.assertEqual(self.client.get(path).status_code, 200, path)
        for path in ("/main.py", "/ai_reader.py", "/render.yaml", "/.git/HEAD", "/.env"):
            self.assertEqual(self.client.get(path).status_code, 404, path)

    def test_other_origins_cannot_call_the_api(self):
        r = self.client.options("/api/ask-jyotishi", headers={
            "Origin": "https://evil.example", "Access-Control-Request-Method": "POST"})
        self.assertNotIn("access-control-allow-origin", r.headers)

    def test_blocking_endpoints_run_in_threadpool(self):
        for endpoint in (main.api_chart, main.api_cities, main.api_geocode):
            self.assertFalse(inspect.iscoroutinefunction(endpoint), endpoint.__name__)

    def test_chart_endpoint(self):
        r = self.client.post("/api/chart", json=BIRTH)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()["planets"]), 9)

    @patch("main.ask_jyotishi", new_callable=AsyncMock, return_value={"answer": "ok"})
    def test_question_limit_is_per_client(self, gemini):
        limit = main.AI_DAILY_LIMITS["question"]
        for _ in range(limit):
            self.assertEqual(self.ask().status_code, 200)
        self.assertEqual(self.ask().status_code, 429)
        spoofed = {"CF-Connecting-IP": "1.1.1.1", "X-Forwarded-For": "9.9.9.9"}
        self.assertEqual(self.ask(headers=spoofed).status_code, 429)
        self.assertEqual(self.ask(headers={"CF-Connecting-IP": "2.2.2.2"}).status_code, 200)
        self.assertEqual(gemini.await_count, limit + 1)

    @patch("main.generate_ai_reading", new_callable=AsyncMock, return_value={"sections": {}})
    def test_reading_limit(self, gemini):
        limit = main.AI_DAILY_LIMITS["reading"]
        for _ in range(limit):
            self.assertEqual(self.client.post("/api/ai-reading", json=BIRTH).status_code, 200)
        r = self.client.post("/api/ai-reading", json={**BIRTH, "language": "hi"})
        self.assertEqual(r.status_code, 429)
        self.assertIn("कल", r.json()["detail"])
        self.assertEqual(gemini.await_count, limit)

    @patch("main.ask_jyotishi", new_callable=AsyncMock, return_value={"answer": "ok"})
    def test_inputs_capped_and_client_chart_ignored(self, gemini):
        self.assertEqual(self.ask(question="x" * (main.MAX_QUESTION_CHARS + 1)).status_code, 422)
        self.assertEqual(self.ask(name="n" * 101).status_code, 422)
        self.assertEqual(gemini.await_count, 0)

        self.ask(chart={"planets": [{"name": "INJECTED"}]},
                 history=[{"role": "user", "content": "y" * 50000}] * 10)
        sent = gemini.call_args.kwargs
        self.assertEqual([p["name"] for p in sent["chart"]["planets"]][:2], ["Sun", "Moon"])
        self.assertEqual(len(sent["history"]), 6)
        self.assertTrue(all(len(m["content"]) == main.MAX_HISTORY_CHARS for m in sent["history"]))


if __name__ == "__main__":
    unittest.main()
