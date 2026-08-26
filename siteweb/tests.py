from django.test import SimpleTestCase, override_settings


TEST_STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}


@override_settings(STORAGES=TEST_STORAGES)
class HomePageTests(SimpleTestCase):

    def test_home_page_retorna_status_200(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)