import unittest
import Audio
from pathlib import Path
import ffmpeg
import filecmp


class TestSum(unittest.TestCase):
    def setUp(self):
        pass

    def test_not_file(self):
        audio = Audio.Audio(check=False)

        self.assertEqual(False, audio.is_file(Path("wrong.mp3")),
                         "Wrong work of program with non - existent files")
        audio.history.ex_t()

    def test_not_audio(self):
        audio = Audio.Audio(check=False)
        self.assertEqual(False, audio.is_audio(Path("test.txt")),
                         "Wrong work of program with not musical files")
        audio.history.ex_t()

    def test_trim(self):
        audio = Audio.Audio(check=False, path="test.mp3")
        audio.trim_body(0, 5, stream=ffmpeg.input(str(audio.current)))
        result = audio.lenght(str(audio.current))
        self.assertTrue(5 - 0.1 <= result and result <= 5 + 0.1,
                        "Wrong work of tream")
        audio.history.ex_t()

    def test_concut(self):
        audio = Audio.Audio(check=False, path="test.mp3")
        streams = []
        streams.append(ffmpeg.input(str(audio.current)))
        streams.append(ffmpeg.input(str(audio.current)))
        audio.concut_body(streams)
        self.assertTrue(filecmp.cmp("test_concut.mp3", audio.current, shallow=False))
        self.assertFalse(filecmp.cmp("test.mp3", audio.current, shallow=False))
        audio.history.ex_t()

    def test_speed_change(self):
        audio = Audio.Audio(check=False, path="test.mp3")
        audio.change_speed_body("2")
        self.assertTrue(filecmp.cmp("test_speed.mp3", audio.current, shallow=False))
        self.assertFalse(filecmp.cmp("test.mp3", audio.current, shallow=False))
        audio.history.ex_t()

    def test_norm(self):
        audio = Audio.Audio(check=False, path="test.mp3")
        audio.norm()
        self.assertTrue(filecmp.cmp("test_norm.mp3", audio.current, shallow=False))
        self.assertFalse(filecmp.cmp("test.mp3", audio.current, shallow=False))
        audio.history.ex_t()

    def test_equalizer(self):
        audio = Audio.Audio(check=False, path="test.mp3")
        audio.equalizer_body(1000, 200, -10)
        self.assertTrue(filecmp.cmp("test_equalizer.mp3", audio.current, shallow=False))
        self.assertFalse(filecmp.cmp("test.mp3", audio.current, shallow=False))
        audio.history.ex_t()
