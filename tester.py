import unittest
from unittest.mock import patch, MagicMock
from requests.exceptions import RequestException
from cats import CatFactProcessor, APIError

class CatFactProcessorUnitTests(unittest.TestCase):

    def test_initial_fact_is_empty(self):
        processor = CatFactProcessor()
        self.assertEqual(processor.last_fact, "")

    @patch('requests.get')
    def test_successful_fact_retrieval(self, mock_request):
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"fact": "Kittens are adorable."}
        mock_resp.raise_for_status.return_value = None
        mock_request.return_value = mock_resp

        processor = CatFactProcessor()
        fact = processor.get_fact()

        self.assertEqual(fact, "Kittens are adorable.")
        self.assertEqual(processor.last_fact, "Kittens are adorable.")

    @patch('requests.get')
    def test_api_request_failure_raises_custom_error(self, mock_request):
        mock_request.side_effect = RequestException("Failed to connect.")

        processor = CatFactProcessor()
        with self.assertRaises(APIError) as context:
            processor.get_fact()
        self.assertIn("Ошибка при запросе к API", str(context.exception))

    def test_analysis_returns_zero_for_empty_fact(self):
        processor = CatFactProcessor()
        result = processor.get_fact_analysis()
        expected = {"length": 0, "letter_frequencies": {}}
        self.assertEqual(result, expected)

    def test_analysis_correctness_with_given_fact(self):
        processor = CatFactProcessor()
        processor.last_fact = "Purr"
        expected_result = {
            "length": 4,
            "letter_frequencies": {'p': 1, 'u': 1, 'r': 2}
        }
        self.assertEqual(processor.get_fact_analysis(), expected_result)

if __name__ == '__main__':
    unittest.main()
