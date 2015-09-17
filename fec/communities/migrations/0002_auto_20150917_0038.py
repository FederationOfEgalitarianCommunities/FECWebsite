# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='date_joined',
            field=models.DateField(help_text=b"The date this Community became a Community in Dialog. You can leave this blank if it's an Ally. This field is used to sort the Newest Communities widget on the homepage.", null=True, verbose_name=b'In FEC Since', blank=True),
        ),
    ]
