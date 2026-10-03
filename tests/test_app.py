import unittest

from app import create_app


class AppFlowTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_home_page_renders(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Smart Traffic Violation Logger", response.get_data(as_text=True))

    def test_public_vehicle_check_page_renders(self):
        response = self.client.get("/check-violation?vehicle_number=ABC123")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Check Violation", response.get_data(as_text=True))

    def test_login_page_renders(self):
        response = self.client.get("/login")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Officer Login", response.get_data(as_text=True))

    def test_dashboard_renders_for_logged_in_officer(self):
        with self.client.session_transaction() as session:
            session["logged_in"] = True
            session["username"] = "trafficadmin"

        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Officer dashboard", response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
