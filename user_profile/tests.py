from django.test import TestCase
from django.contrib.auth.models import User


class CustomSignupTest(TestCase):
    def test_signup_women_in_tech(self):
        response = self.client.post(
            "/accounts/signup/",
            {
                "username": "testwit",
                "email": "testwit@test.com",
                "password1": "testpass123",
                "password2": "testpass123",
                "user_type": "wit",
            },
        )
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username="testwit")
        self.assertTrue(hasattr(user, "women_in_tech_profile"))

    def test_signup_os_maintainer(self):
        response = self.client.post(
            "/accounts/signup/",
            {
                "username": "testosm",
                "email": "testosm@test.com",
                "password1": "testpass123",
                "password2": "testpass123",
                "user_type": "osm",
            },
        )
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username="testosm")
        self.assertTrue(hasattr(user, "os_maintainer_profile"))

    def test_signup_mentor(self):
        response = self.client.post(
            "/accounts/signup/",
            {
                "username": "testmentor",
                "email": "testmentor@test.com",
                "password1": "testpass123",
                "password2": "testpass123",
                "user_type": "mentor",
            },
        )
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username="testmentor")
        self.assertTrue(hasattr(user, "mentor_profile"))
