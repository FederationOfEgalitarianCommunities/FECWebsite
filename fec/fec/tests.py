"""This module contains unit tests for the general application, like PEP8."""

from unittest.case import TestCase

from .utils import check_pep8
from .templatetags.core_filters import get_first_by


class Pep8Tests(TestCase):
    """Ensure the application is PEP8 compliant."""
    def test_functional_test_pep8(self):
        """The functional tests should be PEP8 compliant."""
        result = check_pep8([
            'functional_tests/admin_tests.py',
            'functional_tests/community_page_tests.py',
            'functional_tests/document_tests.py',
            'functional_tests/general_page_tests.py',
            'functional_tests/home_page_tests.py',
        ])

        self.assertEqual(result.total_errors, 0,
                         "PEP8 issues were found in the functional tests.")

    def test_fec_pep8(self):
        """The fec package should be PEP8 compliant."""
        result = check_pep8([
            'fec/urls.py',
            'fec/utils.py',
            'fec/templatetags/core_filters.py',
            'fec/tests.py',
        ])

        self.assertEqual(result.total_errors, 0,
                         "PEP8 issues were found in the fec package.")

    def test_homepage_pep8(self):
        """The homepage package should be PEP8 compliant."""
        result = check_pep8([
            'homepage/admin.py',
            'homepage/models.py',
            'homepage/views.py',
        ])

        self.assertEqual(result.total_errors, 0,
                         "PEP8 issues were found in the homepage package.")

    def test_communities_pep8(self):
        """The communities package should be PEP8 compliant."""
        result = check_pep8([
            'communities/admin.py',
            'communities/models.py',
            'communities/urls.py',
            'communities/views.py',
            'communities/templatetags/communities_tags.py',
            'communities/templatetags/communities_tags_extras.py',
            'communities/tests.py',
        ])

        self.assertEqual(result.total_errors, 0,
                         "PEP8 issues were found in the communities package.")

    def test_documents_pep8(self):
        """The documents package should be PEP8 compliant."""
        result = check_pep8([
            'documents/admin.py',
            'documents/models.py',
            'documents/templatetags/documents_tags.py',
            'documents/templatetags/documents_tags_extras.py',
            'documents/urls.py',
            'documents/views.py',
        ])

        self.assertEqual(result.total_errors, 0,
                         "PEP8 issues were found in the documents package.")


class CoreFiltersTests(TestCase):
    '''Test the core_filters templatetags.'''
    def test_get_first_by_splits_correctly(self):
        '''The function should split the string using the stop_char.'''
        self.assertEqual(get_first_by('1,2,3,4', ','), '1')
        self.assertEqual(get_first_by('1;2;3;4', ';'), '1')
        self.assertEqual(get_first_by('1,2;3;4', ';'), '1,2')

    def test_get_first_by_empty_string(self):
        '''The function should be able to handle empty strings.'''
        self.assertEqual(get_first_by('', ','), '')
        self.assertEqual(get_first_by('', ';'), '')
