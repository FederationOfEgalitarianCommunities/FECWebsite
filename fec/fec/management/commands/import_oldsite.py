"""Import Data from the Old FEC Drupal database.

Communities, Documents & their Categories, Pages, Users and Blog Posts are all
imported.

* Documents have some tags applied.
* Pages are sorted under a hidden 'Imported' page.
* Only Users who have created Blog Posts are imported. Passwords are random.
* Many blog posts are just duplicates of original content from other sites.

"""
import datetime
from getpass import getpass
import pytz
import re
import sys

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.html import linebreaks
from mezzanine.blog.models import BlogPost
from mezzanine.generic.models import Keyword, AssignedKeyword
from mezzanine.pages.models import RichTextPage
try:
    import MySQLdb
except ImportError:
    sys.exit('You must have MySQL-python installed.')


from communities.models import Community
from documents.models import Document, DocumentCategory


DB_NAME = 'old_fec'
DB_USER = 'root'

COMMUNITIES = ['Acorn Community', 'East Wind Community',
               'Emma Goldman Finishing School', 'The Midden', 'Sandhill Farm',
               'Twin Oaks Community', 'Living Energy Farm']

PAGES_TO_EXCLUDE = [
    'Acorn', 'East Wind', 'Emma Goldman Finishing School', 'Sandhill Farm',
    'Skyhouse', 'Twin Oaks', 'Shantagani', 'Meadowdance', 'Ganas',
    'Terra Nova', 'Walnut Street Co-op', 'Our Communities',
    'Systems and Structures', 'Contact Us', 'Permissions Denied', 'Hub System',
]

COMMUNITY_DATA = {}
CATEGORY_IDS = {}
USER_IDS = {}
PAGE_IDS = []
TERM_IDS = {}


class Command(BaseCommand):
    '''Run the import.'''
    help = 'Connect to and import the old Drupal Database'

    def handle(self, *args, **options):
        cursor = _get_cursor()
        print 'Creating Communities...'
        create_communities(cursor)
        print 'Creating Documents & Categories...'
        create_documents_and_categories(cursor)
        print 'Creating Pages...'
        create_pages(cursor)
        print 'Creating Users...'
        create_users(cursor)
        print 'Creating Blog Posts...'
        create_blog_posts(cursor)


def _get_cursor():
    '''Prompt for a password & return a cursor to the MySQL DB.'''
    passw = getpass('Enter password for mySQL user {0}: '.format(DB_USER))
    conn = MySQLdb.connect(host='localhost', user=DB_USER, passwd=passw,
                           db=DB_NAME, charset='utf8')
    return conn.cursor()


def create_communities(cursor):
    '''Create a Community.'''
    for community_name in COMMUNITIES:
        community_term_query = '''
            SELECT tid, description
            FROM `term_data`
            WHERE `name` = '{}'
        '''.format(community_name)
        cursor.execute(community_term_query)
        term_id, description = cursor.fetchone()
        COMMUNITY_DATA[community_name] = {'tid': term_id}
        TERM_IDS[str(term_id)] = community_name
        Community.objects.create(
            title=community_name, membership_status=Community.MEMBER,
            full_description=description,
        )


def create_documents_and_categories(cursor):
    '''Create DocumentCategories & Documents.'''
    create_child_categories(25, None, cursor)
    create_documents(cursor)


def create_child_categories(parent_term_id, parent_category, cursor):
    '''Create DocumentCategories from a parent term_id.'''
    categories_query = '''
        SELECT tid FROM `term_hierarchy` WHERE `parent` = '{}'
    '''.format(parent_term_id)
    cursor.execute(categories_query)
    child_categories = cursor.fetchall()
    for (catergory_id,) in child_categories:
        category_query = '''
            SELECT name FROM `term_data` WHERE `tid` = '{}'
        '''.format(catergory_id)
        cursor.execute(category_query)
        term_data = cursor.fetchone()
        title = re.sub(r'(\d|\.)+ ', '', term_data[0])
        new_category = DocumentCategory.objects.create(
            title=title, parent=parent_category
        )
        CATEGORY_IDS[str(catergory_id)] = new_category
        create_child_categories(catergory_id, new_category, cursor)


def create_documents(cursor):
    '''Create Documents from added Categories.'''
    policy, _ = Keyword.objects.get_or_create(title='Policies')
    irs, _ = Keyword.objects.get_or_create(title='IRS')
    visit, _ = Keyword.objects.get_or_create(title='Visits and Visitors')
    search_text_to_keyword = {
        'Agreement': policy,
        'Policy': policy,
        'IRS': irs,
        'Visit': visit,
    }
    for (category_id, category) in CATEGORY_IDS.items():
        documents_query = '''
            SELECT nid, vid FROM `term_node` where `tid` = '{}'
        '''.format(category_id)
        cursor.execute(documents_query)
        documents = cursor.fetchall()
        for (node_id, version_id) in documents:
            revision_query = '''
                SELECT title, body FROM `node_revisions` WHERE `nid` = '{}'
                AND `vid` = '{}'
            '''.format(node_id, version_id)
            cursor.execute(revision_query)
            title, body = cursor.fetchone()
            PAGE_IDS.append(node_id)
            doc = Document.objects.create(
                title=title, contents=linebreaks(body), category=category)
            for search_text, keyword in search_text_to_keyword.items():
                if search_text in title:
                    doc.keywords.add(AssignedKeyword(keyword=keyword))
            for community_name in COMMUNITIES:
                name = community_name.replace(
                    'Community', '').replace('Farm', '').strip()
                if name in title:
                    doc.community = Community.objects.get(title=community_name)
                    doc.save()


def create_users(cursor):
    '''Create users for blog posts.'''
    users_query = '''
        SELECT uid FROM `node` WHERE `type` = 'blog' GROUP BY `uid`
    '''
    cursor.execute(users_query)
    ids = cursor.fetchall()
    for (user_id,) in ids:
        user_query = '''
            SELECT name, mail FROM `users` WHERE `uid`='{}'
        '''.format(user_id)
        cursor.execute(user_query)
        name, mail = cursor.fetchone()
        if name != '' and not User.objects.filter(username=name).exists():
            new_user = User.objects.create_user(
                username=name, email=mail,
                password=User.objects.make_random_password()
            )
            USER_IDS[str(user_id)] = new_user


def create_blog_posts(cursor):
    '''Create blog posts.'''
    posts_query = '''
        SELECT node.nid, node.title, node.uid, body, node_revisions.timestamp
        FROM `node`
        LEFT JOIN `node_revisions` ON `node`.vid=`node_revisions`.vid
        WHERE node.type = 'blog'
    '''
    eastern = pytz.timezone('US/Eastern')
    cursor.execute(posts_query)
    posts = cursor.fetchall()
    for (_, title, user_id, body, timestamp) in posts:
        time = eastern.localize(datetime.datetime.fromtimestamp(timestamp))
        user = USER_IDS[str(user_id)]
        BlogPost.objects.create(
            user_id=user.id, title=title, publish_date=time,
            content=linebreaks(body),
        )


def create_pages(cursor):
    '''Create a base Imported Page & Generic Pages under it.'''
    pages_query = '''
        SELECT `node`.nid, `node`.title, `node_revisions`.body
        FROM `node`
        LEFT JOIN `node_revisions` on `node`.vid=`node_revisions`.vid
        WHERE node.type = 'page'
    '''
    cursor.execute(pages_query)
    pages = cursor.fetchall()
    root = RichTextPage.objects.create(
        title='Imported', content='Pages imported from the old website.',
        in_menus=[])
    unsorted = RichTextPage.objects.create(
        title='Unsorted', content='Unsorted Pages from the old website.',
        parent=root)
    assemblies = RichTextPage.objects.create(
        title='Assembly Notes',
        content='Assembly Notes Pages from the old website.', parent=root)
    budgets = RichTextPage.objects.create(
        title='Budgets',
        content='Budget Pages from the old website.', parent=root)
    conference_calls = RichTextPage.objects.create(
        title='Conference Calls',
        content='Conference Call Pages from the old website.', parent=root)
    info = RichTextPage.objects.create(
        title='Info',
        content='General Info Pages from the old website.', parent=root)
    jobs = RichTextPage.objects.create(
        title='Jobs', content='Job Pages from the old website.', parent=root)
    search_text_to_parent_node = {
        'About the FEC': info,
        'Accounting': info,
        'Become a Friend': info,
        'Becoming': info,
        'Businesses': info,
        'CONSTITUTION': info,
        'Events': info,
        'Formula': info,
        'Fund': info,
        'History': info,
        'Hosting Assemblies': info,
        'In the Media': info,
        'Internships': info,
        'Joining': info,
        'LEX': info,
        'List': info,
        'NASCO': info,
        'Networks': info,
        'Newsletter': info,
        'Opportunities': info,
        'PEACH': info,
        'Publications': info,
        'Resources': info,
        'Support': info,
        'Video': info,
        'Web Sites': info,
        'What is the': info,
        'get involved': info,

        'Coordinator': jobs,
        'Job Description': jobs,
        'Maintainer': jobs,
        'Manager': jobs,
        'Meta': jobs,
        'Oreo': jobs,
        'Secretary': jobs,
        'Treasurer': jobs,

        'Assembly': assemblies,
        'Budget': budgets,
        'Conference Call': conference_calls,
    }
    for (node_id, title, body) in pages:
        if node_id not in PAGE_IDS and title not in PAGES_TO_EXCLUDE:
            PAGE_IDS.append(node_id)
            parent_node = unsorted
            for search_text, parent in search_text_to_parent_node.items():
                if search_text in title:
                    parent_node = parent
                    break
            RichTextPage.objects.create(
                title=title, content=linebreaks(body),
                parent=parent_node)
