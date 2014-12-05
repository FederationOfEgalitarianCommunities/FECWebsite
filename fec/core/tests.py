"""This module contains unit tests for the general application, like PEP8."""

from unittest.case import TestCase

from .utils import check_pep8


class Pep8Tests(TestCase):
    """Ensure the application is PEP8 compliant."""
    def test_functional_test_pep8_compliance(self):
        """The functional tests should be PEP8 compliant."""
        result = check_pep8([
            'functional_tests/general_page_tests.py',
            'functional_tests/home_page_tests.py',
            'functional_tests/admin_tests.py',
            'functional_tests/community_page_tests.py',
            'functional_tests/document_tests.py',
        ])

        self.assertEqual(result.total_errors, 0,
                         "PEP8 issues were found in the functional tests.")

    def test_core_pep8_compliance(self):
        """The core package should be PEP8 compliant."""
        result = check_pep8([
            'core/urls.py',
            'core/utils.py',
            'core/templatetags/core_filters.py',
            'core/tests.py',
        ])

        self.assertEqual(result.total_errors, 0,
                         "PEP8 issues were found in the core package.")

    def test_communities_pep8_compliance(self):
        """The communities package should be PEP8 compliant."""
        result = check_pep8([
            'communities/admin.py',
            'communities/models.py',
            'communities/views.py',
            'communities/urls.py',
            'communities/templatetags/communities_tags.py',
            'communities/templatetags/communities_tags_extras.py',
            'communities/tests.py',
        ])

        self.assertEqual(result.total_errors, 0,
                         "PEP8 issues were found in the communities package.")

    def test_documents_pep8_compliance(self):
        """The documents package should be PEP8 compliant."""
        result = check_pep8([
            'documents/admin.py',
            'documents/models.py',
            'documents/views.py',
            'documents/urls.py',
            'documents/templatetags/documents_tags.py',
            'documents/templatetags/documents_tags_extras.py',
        ])

        self.assertEqual(result.total_errors, 0,
                         "PEP8 issues were found in the documents package.")
