from django.test import TestCase

from apps.analysis.services import AnalysisService


class AnalysisServiceTests(TestCase):

    def test_service_can_be_imported(self):
        service = AnalysisService()

        self.assertIsInstance(service.observations, list)
        self.assertTrue(service.observations)
