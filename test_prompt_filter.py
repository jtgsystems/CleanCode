import unittest
from unittest.mock import patch

import prompt_filter


class TestPromptFilter(unittest.TestCase):

    @patch("prompt_filter.ollama.chat")
    def test_analyze_prompt(self, mock_chat):
        mock_chat.return_value = {"message": {"content": "analysis"}}
        result = prompt_filter.analyze_prompt("test prompt", "test_model")
        self.assertEqual(result, "analysis")
        mock_chat.assert_called_once()

    @patch("prompt_filter.ollama.chat")
    def test_generate_solutions(self, mock_chat):
        mock_chat.return_value = {"message": {"content": "solutions"}}
        result = prompt_filter.generate_solutions("analysis", "test_model")
        self.assertEqual(result, "solutions")
        mock_chat.assert_called_once()

    @patch("prompt_filter.ollama.chat")
    def test_vet_and_refine(self, mock_chat):
        mock_chat.return_value = {"message": {"content": "vetting"}}
        result = prompt_filter.vet_and_refine("improvements", "test_model")
        self.assertEqual(result, "vetting")
        mock_chat.assert_called_once()

    @patch("prompt_filter.ollama.chat")
    def test_finalize_prompt(self, mock_chat):
        mock_chat.return_value = {"message": {"content": "final"}}
        result = prompt_filter.finalize_prompt("vetting", "original", "test_model")
        self.assertEqual(result, "final")
        mock_chat.assert_called_once()

    @patch("prompt_filter.ollama.chat")
    def test_enhance_prompt(self, mock_chat):
        mock_chat.return_value = {"message": {"content": "enhanced"}}
        result = prompt_filter.enhance_prompt("final", "test_model")
        self.assertEqual(result, "enhanced")
        mock_chat.assert_called_once()

    @patch("prompt_filter.ollama.chat")
    def test_comprehensive_review(self, mock_chat):
        mock_chat.return_value = {"message": {"content": "comprehensive"}}
        result = prompt_filter.comprehensive_review(
            "original",
            "analysis",
            "solutions",
            "vetting",
            "final",
            "enhanced",
            "test_model",
        )
        self.assertEqual(result, "comprehensive")
        mock_chat.assert_called_once()


if __name__ == "__main__":
    unittest.main()
