from django.core.urlresolvers import reverse
from django.test import TestCase
from mezzanine.generic.models import Keyword, AssignedKeyword

from .models import Document, DocumentCategory


class DocumentTagViewTests(TestCase):
    '''Test the View for Document Tags.'''
    def setUp(self):
        '''Create some documents and assign tags.'''
        self.category = DocumentCategory.objects.create(title='Test Cat')
        self.doc_one = Document.objects.create(
            title='doc 1', contents='', category=self.category)
        self.doc_two = Document.objects.create(
            title='doc 2', contents='', category=self.category)
        self.doc_three = Document.objects.create(
            title='doc 3', contents='', category=self.category)

        self.key_one, _ = Keyword.objects.get_or_create(title='key 1')
        self.doc_one.keywords.add(AssignedKeyword(keyword=self.key_one))
        self.key_three, _ = Keyword.objects.get_or_create(title='key 3')
        self.doc_three.keywords.add(AssignedKeyword(keyword=self.key_three))

    def test_tag_added_to_context(self):
        '''The Keyword should be added to the response's context.'''
        response = self.client.get(
            reverse('document_tag_list', kwargs={'tag': self.key_three.slug}))

        self.assertIn('tag', response.context)
        self.assertEqual(response.context['tag'].title, 'key 3')

    def test_only_documents_in_tag_shown(self):
        '''Only Documents with the tag should be shown.'''
        response = self.client.get(
            reverse('document_tag_list', kwargs={'tag': self.key_three.slug}))

        self.assertIn('documents', response.context)
        self.assertSequenceEqual(
            response.context['documents'], [self.doc_three])
