"""This module contains unit tests for the general application, like PEP8."""

from unittest.case import TestCase

from .utils import check_pep8


class Pep8Tests(TestCase):
    """Ensure the application is PEP8 compliant."""
    def test_communities_pep8_compliance(self):
        """The communities package should be PEP8 compliant."""
        result = check_pep8([
            'communities/admin.py',
            'communities/models.py',
            'communities/views.py',
            'communities/urls.py',
            'communities/templatetags/communities_tags.py'
        ])

        self.assertEqual(result.total_errors, 0,
                         "PEP8 issues were found in the communities package.")
