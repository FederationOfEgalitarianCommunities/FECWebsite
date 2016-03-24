"""This module contains functional tests that validate Community Pages."""
from django.core.urlresolvers import reverse
from mezzanine.generic.models import Keyword, AssignedKeyword

from communities.models import Community
from fec.utils import SeleniumTestCase
from documents.models import Document, DocumentCategory


class DocumentCategoryListPageTests(SeleniumTestCase):
    """Test Expectations for the Document Category List Page."""
    def setUp(self):
        """Create some Categories and Documents, visit the child's page."""
        self.root = DocumentCategory.objects.create(title="Darmok")
        self.root_two = DocumentCategory.objects.create(title="Foo")
        self.root_three = DocumentCategory.objects.create(title="Fiz")
        self.child = DocumentCategory.objects.create(title="Jalad",
                                                     parent=self.root)
        self.doc_one = Document.objects.create(
            category=self.child, title="Tenagra",
            contents="Aaaahh!!! Real Monsters")
        self.doc_two = Document.objects.create(
            category=self.child, title="The Switching Hour",
            contents="A night of total terror.")
        self.root_doc = Document.objects.create(
            category=self.root, title="Le Root Doc",
            contents="Je ne suis pas une pipe.")
        Document.objects.create(
            category=self.root_two, title="Hello", contents="World")

        self.selenium.get(self.live_server_url +
                          reverse('document_category_list'))

    def test_page_contains_root_categories(self):
        """The page should contain every parent-less Category."""
        self.assertEqual(
            self.root.title,
            self.selenium.find_element_by_css_selector("#darmok-tab").text)
        self.assertEqual(
            self.root_two.title,
            self.selenium.find_element_by_css_selector("#foo-tab").text)

    def test_empty_root_categories_hidden(self):
        """The page should not show empty parent-less Categories."""
        self.assertElementDoesNotExist(
            self.selenium.find_element_by_css_selector, "#fiz-tab")

    def test_root_categories_contain_documents(self):
        """The parent-less Categories should contain their Documents."""
        root_element = self.selenium.find_element_by_css_selector("#darmok")
        doc_element = root_element.find_element_by_css_selector(
            "#" + self.root_doc.slug)
        self.assertIn(self.root_doc.title, doc_element.text)

    def test_root_categories_contain_children(self):
        """The parent-less Categories should contain their Children."""
        root_element = self.selenium.find_element_by_css_selector("#darmok")
        child_element = root_element.find_element_by_css_selector("#jalad")
        self.assertEqual(self.child.title, child_element.text)

    def test_child_categories_contain_documents(self):
        """The child Categories should contain their Documents."""
        root_element = self.selenium.find_element_by_css_selector("#darmok")
        child_element = root_element.find_element_by_css_selector(
            "#collapse-jalad")
        doc_one_element = child_element.find_element_by_css_selector(
            "#" + self.doc_one.slug)
        doc_two_element = child_element.find_element_by_css_selector(
            "#" + self.doc_two.slug)
        self.assertIn(self.doc_one.title, doc_one_element.text)
        self.assertIn(self.doc_two.title, doc_two_element.text)


class DocumentCategoryDetailPageTests(SeleniumTestCase):
    """Test Expectations for the Document Category Detail Pages."""
    def setUp(self):
        """Create some Categories and Documents, visit the child's page."""
        self.root = DocumentCategory.objects.create(title="Darmok")
        self.child = DocumentCategory.objects.create(title="Jalad",
                                                     parent=self.root)
        self.doc_one = Document.objects.create(
            category=self.child, title="Tenagra",
            contents="Aaaahh!!! Real Monsters")
        self.doc_two = Document.objects.create(
            category=self.child, title="The Switching Hour",
            contents="A night of total terror.")

        self.selenium.get(self.live_server_url + self.child.get_absolute_url())

    def test_page_title_is_category_name(self):
        """The page's title should be the Category's Name."""
        self.assertTitleEquals(self.child.title)

    def test_page_header_is_category_name(self):
        """The page's header should be the Category's Name."""
        self.assertPageHeaderEquals(self.child.title)

    def test_category_name_is_active_breadcrumb(self):
        """The Category name should be active in the breadcrumb menu."""
        self.assertActiveBreadcrumbEquals(self.child.title)

    def test_parent_name_is_in_breadcrumbs(self):
        """The category's parent's name should be an inactive breadcrumb."""
        self.assertInactiveBreadcrumbEquals(self.root.title)

    def test_page_contains_categories_documents(self):
        """The category page should contain any child documents in a table."""
        docs = self.selenium.find_elements_by_css_selector("#documents li")
        self.assertIn(self.doc_one.title, docs[0].text)
        self.assertIn(self.doc_two.title, docs[1].text)

    def test_page_contains_child_categories(self):
        """The page should show any child categories if they exist."""
        self.selenium.get(self.live_server_url + self.root.get_absolute_url())
        children = self.selenium.find_elements_by_css_selector(
            ".child-category")
        self.assertIn(self.child.title, children[0].text)

    def test_page_contains_childrens_documents(self):
        """The page sould show any of it's children's documents."""
        self.selenium.get(self.live_server_url + self.root.get_absolute_url())
        jalad_element = self.selenium.find_element_by_css_selector(
            ".child-category")
        docs = jalad_element.find_elements_by_css_selector(
            ".child-category ul.list-group li")
        self.assertIn(self.doc_one.title, docs[0].text)
        self.assertIn(self.doc_two.title, docs[1].text)

    def test_tag_link_is_valid(self):
        """Entries with a Tag should have a valid link to a Tag page.

        The link should use the Tag's slug, in case there are spaces in the
        Tag's title. See issue #785.
        """
        self.tag, _ = Keyword.objects.get_or_create(title='Tag With Spaces')
        self.doc_one.keywords.add(AssignedKeyword(keyword=self.tag))
        self.selenium.refresh()
        tag_link_is_valid(self)


class DocumentDetailPageTests(SeleniumTestCase):
    """Test Expectations for the Document Detail Pages."""
    def setUp(self):
        """Create a Document and visit it's details page."""
        self.parent = DocumentCategory.objects.create(title="Enterprise")
        self.category = DocumentCategory.objects.create(
            title="Tenagra", parent=self.parent)
        self.community = Community.objects.create(
            title="Picard", membership_status=Community.MEMBER)
        self.document = Document.objects.create(
            title="Darmok & Jalad", category=self.category,
            community=self.community, contents="Treaty of Algeron, 2311.")

        self.selenium.get(self.live_server_url +
                          self.document.get_absolute_url())

    def test_page_title_is_document_name(self):
        """The page's title should be the Document's Name."""
        self.assertTitleEquals(self.document.title)

    def test_page_header_is_document_name(self):
        """The page's header should be the Document's Name."""
        self.assertPageHeaderEquals(self.document.title)

    def test_document_name_is_active_breadcrumb(self):
        """The Document's name should be active in the breadcrumb menu."""
        self.assertActiveBreadcrumbEquals(self.document.title)

    def test_category_name_is_in_inactive_breadcrumbs(self):
        """The Document's Category's name should be an inactive breadcrumb."""
        self.assertInactiveBreadcrumbEquals(self.document.category.title)

    def test_categorys_parent_is_in_inactive_breadcrumbs(self):
        """The Category's parent's name should be an inactive breadcrumb."""
        self.assertInactiveBreadcrumbEquals(
            self.document.category.parent.title)

    def test_page_contains_document_contents(self):
        """The Document's content should appear on the page."""
        contents = self.selenium.find_element_by_css_selector(
            "#document-contents")
        self.assertEqual(self.document.contents, contents.text)

    def test_tag_link_is_valid(self):
        """Entries with a Tag should have a valid link to a Tag page.

        The link should use the Tag's slug, in case there are spaces in the
        Tag's title. See issue #785.
        """
        self.tag, _ = Keyword.objects.get_or_create(title='Tag With Spaces')
        self.document.keywords.add(AssignedKeyword(keyword=self.tag))
        self.selenium.refresh()
        tag_link_is_valid(self)


def tag_link_is_valid(obj):
    """A generic test that ensures a Document's Tag link returns a 200."""
    tag_link = obj.selenium.find_element_by_css_selector(
        ".document-keywords a")
    response = obj.client.get(tag_link.get_attribute('href'))

    obj.assertEqual(response.status_code, 200)
