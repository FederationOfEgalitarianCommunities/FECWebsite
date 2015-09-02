# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20150527_1555'),
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('keywords_string', models.CharField(max_length=500, editable=False, blank=True)),
                ('title', models.CharField(max_length=500, verbose_name='Title')),
                ('slug', models.CharField(help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, null=True, verbose_name='URL', blank=True)),
                ('_meta_title', models.CharField(help_text='Optional title to be used in the HTML title tag. If left blank, the main title field will be used.', max_length=500, null=True, verbose_name='Title', blank=True)),
                ('description', models.TextField(verbose_name='Description', blank=True)),
                ('gen_description', models.BooleanField(default=True, help_text='If checked, the description will be automatically generated from content. Uncheck if you want to manually set a custom description.', verbose_name='Generate description')),
                ('created', models.DateTimeField(null=True, editable=False)),
                ('updated', models.DateTimeField(null=True, editable=False)),
                ('status', models.IntegerField(default=2, help_text='With Draft chosen, will only be shown for admin users on the site.', verbose_name='Status', choices=[(1, 'Draft'), (2, 'Published')])),
                ('publish_date', models.DateTimeField(help_text="With Published chosen, won't be shown until this time", null=True, verbose_name='Published from', db_index=True, blank=True)),
                ('expiry_date', models.DateTimeField(help_text="With Published chosen, won't be shown after this time", null=True, verbose_name='Expires on', blank=True)),
                ('short_url', models.URLField(null=True, blank=True)),
                ('in_sitemap', models.BooleanField(default=True, verbose_name='Show in sitemap')),
                ('profile_image', models.ImageField(help_text=b'The main image to use for the Community.', null=True, upload_to=b'communities/profile_images/', blank=True)),
                ('short_description', models.TextField(help_text=b'A short paragraph about the community. This is used on the Our Communities page.', blank=True)),
                ('full_description', mezzanine.core.fields.RichTextField(help_text=b"A long description about the community. This is used on the Community's detail page.", blank=True)),
                ('general_location', models.CharField(help_text=b'The general area of the Community, like "Rural Virginia".', max_length=50, blank=True)),
                ('year_founded', models.PositiveSmallIntegerField(help_text=b'The year the community was founded.', null=True, blank=True)),
                ('number_of_adults', models.PositiveSmallIntegerField(default=0, help_text=b'The number of adults living in the Community.')),
                ('number_of_children', models.PositiveSmallIntegerField(default=0, help_text=b'The number of children living in the Community.')),
                ('membership_status', models.CharField(default=b'community-in-dialog', help_text=b"The Community's current status with the FEC.", max_length=30, verbose_name=b'FEC Membership Status', choices=[(b'member', b'Full Member'), (b'community-in-dialog', b'Community in Dialog'), (b'ally', b'Ally')])),
                ('date_joined', models.DateField(help_text=b'The date this Community joined the FEC. Leave blank if not a member', null=True, verbose_name=b'FEC Member Since', blank=True)),
                ('address', models.TextField(help_text=b'The full address of the Community.', verbose_name=b'Full Address', blank=True)),
                ('website', models.URLField(help_text=b"The Community's website.", blank=True)),
                ('email', models.EmailField(help_text=b'The contact email for the Community.', max_length=254, verbose_name=b'Contact Email', blank=True)),
                ('phone', models.CharField(help_text=b'The phone number of the Community.', max_length=20, verbose_name=b'Phone Number', blank=True)),
                ('blog_category', models.ForeignKey(to='blog.BlogCategory', blank=True)),
                ('site', models.ForeignKey(editable=False, to='sites.Site')),
            ],
            options={
                'ordering': ['title'],
                'verbose_name_plural': 'communities',
            },
        ),
        migrations.CreateModel(
            name='CommunityFeed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_order', mezzanine.core.fields.OrderField(null=True, verbose_name='Order')),
                ('url', models.URLField(help_text=b"The Feed's URL.")),
                ('post_limit', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('community', models.ForeignKey(related_name='feeds', to='communities.Community')),
            ],
            options={
                'ordering': ('_order',),
                'verbose_name': 'Feed',
                'verbose_name_plural': 'Feeds',
            },
            bases=(models.Model, object),
        ),
        migrations.CreateModel(
            name='CommunityImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_order', mezzanine.core.fields.OrderField(null=True, verbose_name='Order')),
                ('file', mezzanine.core.fields.FileField(max_length=200, verbose_name=b'File')),
                ('description', models.CharField(max_length=1000, verbose_name=b'Description', blank=True)),
                ('community', models.ForeignKey(related_name='images', to='communities.Community')),
            ],
            options={
                'ordering': ('_order',),
                'verbose_name': 'Image',
                'verbose_name_plural': 'Images',
            },
            bases=(models.Model, object),
        ),
    ]
