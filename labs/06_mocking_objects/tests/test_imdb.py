"""
Test Cases for Mocking Lab
"""
import json
from unittest import TestCase
from unittest.mock import patch, Mock
from requests import Response
from models import IMDb

IMDB_DATA = {}

class TestIMDbDatabase(TestCase):
    """Tests Cases for IMDb Database"""

    @classmethod
    def setUpClass(cls):
        """ Load imdb responses needed by tests """
        global IMDB_DATA
        with open('tests/fixtures/imdb_responses.json') as json_data:
            IMDB_DATA = json.load(json_data)


    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    @patch('test_imdb.IMDb.search_titles')
    def test_search_by_title(self, imdb_mock):
        """Test searching by title"""
        imdb_mock.return_value = IMDB_DATA["GOOD_SEARCH"]
        imdb = IMDb("k_12345678")
        results = imdb.search_titles("Bambi")
        self.assertIsNotNone(results)
        self.assertIsNone(results["errorMessage"])
        self.assertIsNotNone(results["results"])
        self.assertEqual(results["results"][0]["id"], IMDB_DATA["GOOD_SEARCH"]["results"][0]["id"])

    @patch('models.imdb.requests.get')
    def test_search_with_no_results(self, imdb_mock):
        """Test searching with no results"""
        imdb_mock.return_value = Mock(spec=Response,
                                        status_code=404,
                                        text="Not Found")
        imdb = IMDb("k_12345678")
        results = imdb.search_titles("Bambi")
        self.assertEqual(results, {})

    @patch('models.imdb.requests.get')
    def test_search_by_title_failed(self, imdb_mock):
        """Test searching by title failed"""
        imdb_mock.return_value = Mock(spec=Response,
                                        status_code=200,
                                        json=Mock(return_value=IMDB_DATA["INVALID_API"]))
        imdb = IMDb("bad-key")
        results = imdb.search_titles("Bambi")
        self.assertIsNotNone(results)
        self.assertEqual(results["errorMessage"], "Invalid API Key")

    @patch('models.imdb.requests.get')
    def test_search_by_invalid_movie(self, imdb_mock):
        """Test searching by invalid movie"""
        imdb_mock.return_value = Mock(spec=Response,
                                        status_code=200,
                                        json=Mock(return_value=IMDB_DATA["MOVIE_INVALID"]))
        imdb = IMDb("bad-key")
        results = imdb.search_titles("Bambi")
        self.assertIsInstance(results, dict)
        self.assertIn("errorMessage", results)
        self.assertEqual(results["errorMessage"], IMDB_DATA["MOVIE_INVALID"]["errorMessage"])

    @patch('models.imdb.requests.get')
    def test_movie_ratings(self, imdb_mock):
        """Test movie ratings"""
        imdb_mock.return_value = Mock(spec=Response,
                                        status_code=200,
                                        json=Mock(return_value=IMDB_DATA["GOOD_RATING"]))
        imdb = IMDb("k_12345678")
        results = imdb.movie_ratings("tt1375666")
        self.assertIsNotNone(results)
        self.assertEqual(results["title"], IMDB_DATA["GOOD_RATING"]["title"])
        self.assertEqual(results["filmAffinity"], IMDB_DATA["GOOD_RATING"]["filmAffinity"])
        self.assertEqual(results["rottenTomatoes"], IMDB_DATA["GOOD_RATING"]["rottenTomatoes"])

    @patch('models.imdb.requests.get')
    def test_search_by_invalid_movie_ratings(self, imdb_mock):
        """Test searching by invalid movie ratings"""
        imdb_mock.return_value = Mock(spec=Response,
                                        status_code=400,
                                        json=Mock(return_value={}))
        imdb = IMDb("bad-key")
        results = imdb.movie_ratings("invalid-movie-id")
        self.assertEqual(results, {})

    @patch('models.imdb.requests.get')
    def test_movie_review(self, imdb_mock):
        """Test movie review"""
        imdb_mock.return_value = Mock(spec=Response,
                                        status_code=200,
                                        json=Mock(return_value=IMDB_DATA["GOOD_REVIEW"]))
        imdb = IMDb("k_12345678")
        results = imdb.movie_reviews("tt1375666")
        self.assertIsNotNone(results)
        self.assertEqual(imdb_mock.return_value.status_code, 200)
        self.assertEqual(results["title"], IMDB_DATA["GOOD_REVIEW"]["title"])
        self.assertEqual(results["year"], IMDB_DATA["GOOD_REVIEW"]["year"])
        self.assertIsNone(results["errorMessage"])
        self.assertEqual(results["items"], IMDB_DATA["GOOD_REVIEW"]["items"])


    @patch('models.imdb.requests.get')
    def test_movie_review_invalid(self, imdb_mock):
        """Test movie review invalid"""
        imdb_mock.return_value = Mock(spec=Response,
                                status_code = 400,
                                json=Mock(return_value={}))
        imdb = IMDb("bad-key")
        results = imdb.movie_reviews("invalid-movie-id")
        self.assertEqual(results, {})
