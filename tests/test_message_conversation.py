import unittest
from types import SimpleNamespace
from unittest.mock import patch

import main


class FakeUI:
    muted = False
    current_file = None

    def __init__(self):
        self.on_text_command = None
        self.logs = []
        self.states = []

    def write_log(self, text):
        self.logs.append(text)

    def set_state(self, state):
        self.states.append(state)


class MessageConversationTests(unittest.IsolatedAsyncioTestCase):
    async def test_platform_followup_keeps_recipient_and_message(self):
        jarvis = main.JarvisLive(FakeUI())
        calls = []

        def fake_send(parameters, **kwargs):
            calls.append(dict(parameters))
            if len(calls) == 1:
                return (
                    "NEEDS_PLATFORM: Ask the user whether to use WhatsApp or "
                    "email. No message was sent."
                )
            return "Message verified as sent."

        with patch.object(main, "send_message", side_effect=fake_send):
            jarvis._latest_user_text = (
                "Hermano, ¿a qué hora estamos listos?"
            )
            first = SimpleNamespace(
                name="send_message",
                id="first",
                args={
                    "receiver": "Jonathan 002",
                    "message_text": "Hermano, ¿a qué hora estamos listos?",
                    "platform": "auto",
                },
            )
            await jarvis._execute_tool(first)

            jarvis._latest_user_text = "WhatsApp"
            second = SimpleNamespace(
                name="send_message",
                id="second",
                args={
                    "receiver": "WhatsApp",
                    "message_text": "WhatsApp",
                    "platform": "whatsapp",
                },
            )
            await jarvis._execute_tool(second)

        self.assertEqual(calls[1]["receiver"], "Jonathan 002")
        self.assertEqual(
            calls[1]["message_text"],
            "Hermano, ¿a qué hora estamos listos?",
        )
        self.assertEqual(calls[1]["_user_request"], "WhatsApp")
        self.assertIsNone(jarvis._pending_message)


if __name__ == "__main__":
    unittest.main()
