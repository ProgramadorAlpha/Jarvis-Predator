import unittest
from unittest.mock import MagicMock, patch

from PIL import Image

from actions import send_message


class SendMessageTests(unittest.TestCase):
    def test_explicit_platform_is_taken_from_user_words(self):
        self.assertEqual(
            send_message._explicit_platform("Mandalo por WhatsApp"),
            "whatsapp",
        )
        self.assertEqual(
            send_message._explicit_platform("Responde este correo"),
            "email",
        )
        self.assertIsNone(
            send_message._explicit_platform("Envia un mensaje a Victoria")
        )
        self.assertEqual(
            send_message._contact_fallback_query("Jonathan 002"),
            "Jonathan",
        )
        self.assertTrue(
            send_message._contact_name_matches(
                "Jonathan 002",
                "Jonathan En Portugal 002",
            )
        )
        self.assertFalse(
            send_message._contact_name_matches(
                "Jonathan 002",
                "Don Que back JONATHAN",
            )
        )
        self.assertEqual(
            send_message._platform_from_foreground(
                "J.A.R.V.I.S — MARK XXXIX",
                "Qt690QWindowIcon",
            ),
            "unknown",
        )
        self.assertEqual(
            send_message._platform_from_foreground(
                "WhatsApp",
                "WinUIDesktopWin32WindowClass",
            ),
            "whatsapp",
        )
        self.assertIsNone(
            send_message._platform_from_foreground(
                "RE: Orçamentos pendentes - Google Chrome",
                "Chrome_WidgetWin_1",
            )
        )

    @patch.object(send_message, "_open_app", return_value=True)
    @patch.object(send_message, "_select_whatsapp_contact", return_value=None)
    def test_whatsapp_no_results_never_sends(
        self,
        select_contact,
        open_app,
    ):
        result = send_message._send_whatsapp(
            "Jonathan 002",
            "Hermano, que vamos a hacer en el almuerzo?",
        )

        self.assertIn("No WhatsApp contact", result)
        self.assertIn("no message was sent", result)
        select_contact.assert_called_once_with("Jonathan 002")

    @patch.object(send_message, "_open_app", return_value=True)
    @patch.object(
        send_message,
        "_select_whatsapp_contact",
        return_value="Jonathan En Portugal 002 Monday",
    )
    @patch.object(
        send_message,
        "_whatsapp_open_header",
        return_value="Don Que back JONATHAN",
    )
    @patch.object(send_message, "_send_whatsapp_accessible")
    def test_whatsapp_wrong_opened_chat_never_writes_message(
        self,
        send_accessible,
        open_header,
        select_contact,
        open_app,
    ):
        message = "Hermano, que vamos a hacer en el almuerzo?"
        result = send_message._send_whatsapp("Jonathan 002", message)

        self.assertIn("does not match", result)
        self.assertIn("no message was sent", result)
        send_accessible.assert_not_called()
        open_header.assert_called_once_with("Jonathan 002")
        select_contact.assert_called_once_with("Jonathan 002")

    @patch.object(send_message, "_open_app", return_value=True)
    @patch.object(
        send_message,
        "_select_whatsapp_contact",
        return_value="Jonathan En Portugal 002 Monday",
    )
    @patch.object(
        send_message,
        "_whatsapp_open_header",
        return_value="Jonathan En Portugal 002",
    )
    @patch.object(send_message, "_send_whatsapp_accessible", return_value=True)
    def test_whatsapp_matching_chat_is_sent_and_verified(
        self,
        send_accessible,
        open_header,
        select_contact,
        open_app,
    ):
        message = "Hermano, que vamos a hacer en el almuerzo?"

        result = send_message._send_whatsapp("Jonathan 002", message)

        self.assertIn("verified as sent", result)
        send_accessible.assert_called_once_with(message)

    @patch.object(send_message, "_capture_window")
    @patch.object(send_message, "_analyze")
    def test_email_recipient_mismatch_never_clicks(
        self,
        analyze,
        capture_window,
    ):
        capture_window.return_value = (Image.new("RGB", (100, 100)), (0, 0))
        analyze.return_value = {
            "email_open": True,
            "visible_sender": "Someone Else",
            "recipient_matches": False,
            "reply_center": [10, 10],
        }

        with patch.object(send_message, "_click_local") as click:
            result = send_message._send_email_reply("Victoria", "Gracias")

        self.assertIn("does not match", result)
        self.assertIn("no email was sent", result)
        click.assert_not_called()

    @patch.object(send_message, "_send_email_reply", return_value="email path")
    @patch.object(send_message, "_send_whatsapp", return_value="whatsapp path")
    @patch.object(send_message, "_detect_visible_platform", return_value="email")
    def test_unspecified_platform_uses_visible_context(
        self,
        detect_platform,
        send_whatsapp,
        send_email,
    ):
        result = send_message.send_message(
            {
                "receiver": "Victoria",
                "message_text": "Gracias por la respuesta",
                "platform": "auto",
                "_user_request": "Envia un mensaje a Victoria agradeciendo la respuesta",
            }
        )

        self.assertEqual(result, "email path")
        detect_platform.assert_called_once()
        send_email.assert_called_once()
        send_whatsapp.assert_not_called()


if __name__ == "__main__":
    unittest.main()
