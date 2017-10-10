# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizapp', '0002_remove_profiledata_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='profiledata',
            name='status',
            field=models.IntegerField(default=-1),
            preserve_default=True,
        ),
    ]
