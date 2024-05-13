import unittest
from app import app

class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_health_check(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "OK"})

    def test_readiness_probe_initial(self):
        response = self.app.get('/ready')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "OK"})

    def test_enable_readiness(self):
        response = self.app.get('/ready/enable')
        self.assertEqual(response.status_code, 202)
        followup = self.app.get('/ready')
        self.assertDictEqual(followup.json, {"status": "OK"})

    def test_disable_readiness(self):
        response = self.app.get('/ready/disable')
        self.assertEqual(response.status_code, 202)
        followup = self.app.get('/ready')
        self.assertDictEqual(followup.json, {"status": "SERVICE UNAVAILABLE"})

    def test_metrics_endpoint(self):
        response = self.app.get('/metrics')
        self.assertEqual(response.status_code, 200)
        # Verify the exact content type, including charset
        self.assertEqual(response.content_type, 'text/plain; charset=utf-8')
        # Check if the response contains the specific metric name
        self.assertIn('requests_per_second', response.data.decode('utf-8'))

if __name__ == '__main__':
    unittest.main()
