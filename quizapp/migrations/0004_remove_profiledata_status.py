# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizapp', '0003_profiledata_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profiledata',
            name='status',
        ),
    ]
