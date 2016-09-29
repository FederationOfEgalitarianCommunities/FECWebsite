# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mezzanine.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Decision',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_order', mezzanine.core.fields.OrderField(null=True, verbose_name='Order')),
                ('name', models.CharField(help_text=b'The display name of the Decision.', max_length=50)),
                ('short_description', mezzanine.core.fields.RichTextField(help_text=b'A short introduction description shown on both pages.')),
                ('long_description', mezzanine.core.fields.RichTextField(help_text=b'A long description shown on CiaB and Wiki pages.')),
                ('wiki_article', models.ForeignKey(to='wiki.Article', blank=True)),
            ],
            options={
                'ordering': ('_order',),
            },
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('_order', mezzanine.core.fields.OrderField(null=True, verbose_name='Order')),
                ('name', models.CharField(help_text=b'The display name of the Option.', max_length=50)),
                ('short_description', mezzanine.core.fields.RichTextField(help_text=b'A short introduction description shown on both pages.')),
                ('long_description', mezzanine.core.fields.RichTextField(help_text=b'A long description shown on CiaB and Wiki pages.')),
                ('decision', models.ForeignKey(to='ciab.Decision')),
            ],
            options={
                'ordering': ('_order',),
            },
        ),
    ]
