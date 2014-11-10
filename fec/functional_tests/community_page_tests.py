"""This module contains functional tests that validate Community Pages."""
import time

from django.core.urlresolvers import reverse
from mezzanine.core.templatetags.mezzanine_tags import thumbnail

from core.utils import SeleniumTestCase, create_test_image
from communities.models import Community, CommunityImage, CommunityFeed


class CommunityDetailPageTests(SeleniumTestCase):
    """Test Expectations for the Community Details Page."""
    def setUp(self):
        """Create a Community to test with and visit it's detail's page."""
        self.darmok = Community.objects.create(
            title="Darmok", year_founded=2014,
            general_location="Rural Tenagra", number_of_adults=20,
            short_description="A dude from a Star Trek episode",
            profile_image=create_test_image(), email="darmok@tenagra.com",
            number_of_children=3, phone="(555)555-5555",
            website="http://hello.com",
            address="123 Easy St.\nSomewhere, AK 21030",
            full_description="Hello, I am the full description"
        )
        self.darmok_gallery_image = CommunityImage.objects.create(
            community=self.darmok, file="Test")
        self.darmok_rss_feed = CommunityFeed.objects.create(
            community=self.darmok,
            url="http://www.feedforall.com/sample-feed.xml")

        self.selenium.get(self.live_server_url +
                          self.darmok.get_absolute_url())

    def test_page_title_is_community_name(self):
        """The page's title should the Community's Name."""
        self.assertTitleEquals(self.darmok.title)

    def test_page_header_is_community_name(self):
        """The page header should be the Community's Name."""
        self.assertPageHeaderEquals(self.darmok.title)

    def test_community_name_is_in_breadcrumbs(self):
        """The community name should be active in the breadcrumb menu."""
        active_crumb = self.selenium.find_element_by_css_selector(
            "ul.breadcrumb li.active")
        self.assertEqual(self.darmok.title, active_crumb.text)

    def test_page_contains_profile_image(self):
        """The community's profile picture should be on the page."""
        image_element = self.selenium.find_element_by_css_selector(
            ".profile-image img")

        profile_image_url = thumbnail(self.darmok.profile_image.url, 600, 0)

        self.assertEqual(image_element.get_attribute('src'),
                         self.live_server_url + '/static/media/' +
                         profile_image_url)

    def test_page_contains_year_founded(self):
        """The year the community was founded should appear in it's page."""
        year_founded = self.selenium.find_element_by_css_selector(".founded")
        self.assertEqual('{0}'.format(self.darmok.year_founded),
                         year_founded.text)

    def test_page_contains_population(self):
        """The community's population should appear in it's page."""
        adults = self.selenium.find_element_by_css_selector(".adults")
        children = self.selenium.find_element_by_css_selector(".children")

        self.assertEqual(adults.text, str(self.darmok.number_of_adults))
        self.assertEqual(children.text, str(self.darmok.number_of_children))

    def test_page_contains_email(self):
        """The community's email should appear on the page."""
        email = self.selenium.find_element_by_css_selector(".email")
        self.assertEqual(self.darmok.email, email.text)

    def test_email_is_a_mailto_link(self):
        """The community's email should be a mailto: link."""
        email = self.selenium.find_element_by_css_selector(".email a")
        mailto_link = "mailto:" + self.darmok.email
        self.assertEqual(mailto_link, email.get_attribute("href"))

    def test_page_contains_website(self):
        """The community's website should appear on the page."""
        website = self.selenium.find_element_by_css_selector(".website")
        self.assertEqual(self.darmok.website, website.text)

    def test_page_contains_phone_number(self):
        """The community's phone number should appear on the page."""
        phone = self.selenium.find_element_by_css_selector(".phone")
        self.assertEqual(self.darmok.phone, phone.text)

    def test_page_contains_address(self):
        """The community's address should appear if marked as public."""
        address = self.selenium.find_element_by_css_selector(".address")
        self.assertEqual(self.darmok.address, address.text)

    def test_page_contains_full_description(self):
        """The community's full description should appear in it's page."""
        description = self.selenium.find_element_by_css_selector(
            ".full-description")
        self.assertEqual(self.darmok.full_description, description.text)

    def test_page_contains_image_gallery(self):
        """The community's image gallery should appear on the page."""
        image = self.selenium.find_element_by_css_selector(".gallery img")
        gallery_image_url = thumbnail(
            self.darmok.images.all()[0], 600, 375)
        self.assertEqual(image.get_attribute('src'),
                         self.live_server_url + '/static/media/' +
                         gallery_image_url)

    def test_page_contains_blog_posts(self):
        """The community's blog posts should appear on the page."""
        blog_posts = self.selenium.find_elements_by_css_selector(
            ".community-blog-posts .community-blog-post")
        self.assertNotEqual(blog_posts, [])

    def test_page_contains_latest_blog_post(self):
        """The community's latest blog post should appear first."""
        blog_posts = self.selenium.find_elements_by_css_selector(
            ".community-blog-posts .community-blog-post")
        self.assertIn("FeedScout enables you to view RSS/ATOM/RDF feeds from",
                      blog_posts[0].text)


class CommunityListPageTests(SeleniumTestCase):
    """Test Expectations for the Member Community Listing Page."""
    def setUp(self):
        """Create several Communities and visit the Community Listings Page."""
        self.darmok = Community.objects.create(
            title="Darmok", year_founded=2014,
            general_location="Rural Tenagra", number_of_adults=20,
            number_of_children=3,
            short_description="A dude from a Star Trek episode",
            profile_image=create_test_image()
        )
        self.jalad = Community.objects.create(title="Jalad")
        self.community_in_dialog = Community.objects.create(
            title="Tenagra", is_community_in_dialog=True)
        self.selenium.get(self.live_server_url + reverse('community_list'))

    def test_page_title_is_our_communities(self):
        """The page title should be "Our Communities"."""
        self.assertTitleEquals("Our Communities")

    def test_page_header_is_our_communities(self):
        """The page header should be "Our Communities"."""
        self.assertPageHeaderEquals("Our Communities")

    def test_section_heading_is_community_name(self):
        """The community's name should be it's section's Heading."""
        heading = self.selenium.find_element_by_css_selector(
            ".thumbnail .caption h4")
        self.assertEqual(self.darmok.title,
                         heading.text[:len(self.darmok.title)])

    def test_section_heading_is_link_to_details(self):
        """The community's section heading should link to it's details page."""
        self.selenium.find_element_by_css_selector(
            ".thumbnail .caption h4 a").click()
        time.sleep(0.15)
        community_detail_url = (
            self.live_server_url +
            reverse('community_detail', kwargs={'slug': self.darmok.slug})
        )
        self.assertEqual(self.selenium.current_url, community_detail_url)

    def test_section_contains_profile_image(self):
        """The community's profile picture should appear in it's section."""
        image_element = self.selenium.find_element_by_css_selector(
            ".thumbnail img")

        profile_image_url = thumbnail(self.darmok.profile_image.url, 400, 250)

        self.assertEqual(image_element.get_attribute('src'),
                         self.live_server_url + '/static/media/' +
                         profile_image_url)

    def test_section_contains_year_founded_if_specifed(self):
        """The year the community was founded should appear in it's section."""
        year_founded = self.selenium.find_element_by_css_selector(
            ".thumbnail .caption h4 small")
        self.assertEqual('({0})'.format(self.darmok.year_founded),
                         year_founded.text)

    def test_section_does_not_contain_year_founded_if_not_specifed(self):
        """The year founded should not appear if not set."""
        jalad_heading = self.selenium.find_elements_by_css_selector(
            ".thumbnail .caption h4")[1]
        self.assertElementDoesNotExist(
            jalad_heading.find_element_by_css_selector, "small")

    def test_section_contains_general_location(self):
        """The community's general location should appear in it's section."""
        darmok_caption = self.selenium.find_element_by_css_selector(
            ".thumbnail .caption .location")
        self.assertEqual(self.darmok.general_location, darmok_caption.text)

    def test_section_does_not_contain_general_location_if_not_specified(self):
        """The general location should not appear if not set."""
        jalad_caption = self.selenium.find_elements_by_css_selector(
            ".thumbnail .caption")[1]
        self.assertElementDoesNotExist(
            jalad_caption.find_element_by_css_selector, ".location")

    def test_section_contains_population(self):
        """The community's population should appear in it's section."""
        section_population = self.selenium.find_element_by_css_selector(
            ".thumbnail .caption h5 .population")
        population_string = "{0} Adults and {1} Children".format(
            self.darmok.number_of_adults, self.darmok.number_of_children)
        self.assertEqual(population_string, section_population.text)

    def test_section_does_not_contain_population_if_not_specified(self):
        """The population should not appear if not set."""
        caption = self.selenium.find_elements_by_css_selector(
            ".thumbnail .caption")[1]
        self.assertElementDoesNotExist(
            caption.find_element_by_css_selector, ".population")

    def test_section_contains_short_description(self):
        """The community's shorter description should appear in the section."""
        section_description = self.selenium.find_element_by_css_selector(
            ".thumbnail .caption p")
        self.assertEqual(self.darmok.short_description,
                         section_description.text)
