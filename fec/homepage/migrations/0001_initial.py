# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomepageContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('intro_text', mezzanine.core.fields.RichTextField(help_text=b'The large text below the navigation')),
                ('content_title', models.CharField(default=b'Our Principles', help_text=b'The title of the custom content section', max_length=200)),
                ('content', mezzanine.core.fields.RichTextField(help_text=b'The custom text')),
                ('communities_conference_text', mezzanine.core.fields.RichTextField(help_text=b'The text for the Communities Conference sidebar widget.', verbose_name=b'Communities Conference Widget Text', blank=True)),
                ('show_news', models.BooleanField(default=True, help_text=b'Display the "News" block?')),
                ('show_newest_communities', models.BooleanField(default=True, help_text=b'Display the "Newest Communities" block?')),
                ('site', models.ForeignKey(editable=False, to='sites.Site')),
            ],
            options={
                'verbose_name': 'Homepage Content',
                'verbose_name_plural': 'Homepage Content',
            },
        ),
    ]
