django-voter
##############

Application for Django framework that contains generic rating\vote system. Requires modifications in the model, that will be used for voting, to optimize number of database queries.

.. contents::

Quick overview
==============

More later.

Requirements
==============

- python >= 2.5
- pip >= 0.8
- django >= 1.2
- django-misc (https://github.com/ilblackdragon/django-misc)

Installation
=============

**Django voter** should be installed using pip: ::

    pip install git+git://github.com/ilblackdragon/django-voter.git


Setup
============

- Add 'blog' to INSTALLED_APPS ::

    INSTALLED_APPS += ( 'django_voter', )

- Add RatingField to models you want to allow voting for: ::


    from django_voter.models import RatingField
    
    class SomeModle(models.Model):
       ...
       rating = RatingField()
    

Configure django-voter
===============

Will be later.

Contributing
============

Development of django-voter happens at github: https://github.com/ilblackdragon/django-voter
Please, if you have any insight how to patch existing models - let me know. At this point, having a rating field at model that this field will be required at is the best solution I see from point of number database queries.

License
============

Copyright (C) 2013 Illia Polosukhin
This program is licensed under the MIT License (see LICENSE)
