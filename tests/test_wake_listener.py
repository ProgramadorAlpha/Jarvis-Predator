import unittest

import numpy as np

import wake_listener


class WakeListenerTests(unittest.TestCase):
    def test_spanish_wake_phrase(self):
        self.assertTrue(
            wake_listener._wake_phrase_detected("despierta jarvis")
        )
        self.assertTrue(
            wake_listener._wake_phrase_detected("¡Despierta, Yarvis!")
        )
        self.assertTrue(
            wake_listener._wake_phrase_detected("despierta ya avis")
        )
        self.assertFalse(wake_listener._wake_phrase_detected("buenos dias"))

    def test_clap_requires_a_sharp_transient(self):
        silence = np.zeros(1024, dtype=np.int16)
        clap = np.zeros(1024, dtype=np.int16)
        clap[492:508] = np.array(
            [40, -38] * 8,
            dtype=np.int16,
        )

        self.assertFalse(wake_listener._is_clap(silence, 0.00005))
        self.assertTrue(wake_listener._is_clap(clap, 0.00005))
        self.assertFalse(
            wake_listener._is_activation_clap(clap, 0.00005)
        )

        strong_clap = np.zeros(1024, dtype=np.int16)
        strong_clap[492:508] = np.array(
            [3000, -2800] * 8,
            dtype=np.int16,
        )
        self.assertTrue(
            wake_listener._is_activation_clap(strong_clap, 0.00005)
        )

    def test_profile_and_requested_video(self):
        self.assertEqual(wake_listener.CHROME_PROFILE, "Default")
        self.assertIn("dsUXAEzaC3Q", wake_listener.BAD_VIDEO_URL)


if __name__ == "__main__":
    unittest.main()
