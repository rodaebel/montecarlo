===================================
Distributed Monte Carlo Integration
===================================

This application uses Google App Engine and HTML5 Web Workers to compute
Monte Carlo Simulations in a highly distributed way.


Copyright and License
---------------------

Copyright 2010, 2011 Tobias Rodaebel

This software is released under the Apache License, Version 2.0. You may obtain
a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0


Online Demo
-----------

In order to try an online demo, access the following URL with a HTML5 Web
Workers capable browser like Google Chrome or Safari:

  http://montecarlo-integration.appspot.com


Requirements
------------

The GAE SDK will be installed by zc.buildout. See the buildout.cfg file.

Buildout needs Python and the tools contained in /bin and /usr/bin of a
standard installation of the Linux operating environment. You should ensure
that these directories are on your PATH and following programs can be found:

* Python 2.7+ (3.x is not supported!)
* virtualenv (optional)


Building and Running the Application
------------------------------------

We recommend to install this buildout into a virtualenv in order to obtain
isolation from any 'system' packages you've got installed in your Python
version.

Install virtualenv::

  $ virtualenv --distribute montecarlo-env
  $ cd montecarlo-env
  $ git clone http://github.com/rodaebel/montecarlo.git

Build and run the application::

  $ cd montecarlo
  $ ../bin/python bootstrap.py --distribute
  $ ./bin/buildout
  $ ./bin/dev_appserver parts/montecarlo

Then access the application using a web browser with the following URL::

  http://localhost:8080/


Uploading and Managing
----------------------

To upload application files, run::

  $ ./bin/appcfg update parts/montecarlo

For a more detailed documentation follow this url::

  http://code.google.com/appengine/docs/python/tools/uploadinganapp.html
