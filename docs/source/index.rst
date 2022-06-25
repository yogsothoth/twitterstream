TwitterStream documentation
===========================

This project presents a way to stream tweets from twitter to a web client in real-time.

Quick start
-----------

.. code-block:: sh

   $ python -m venv default
   $ source default/bin/activate
   $ echo "MY_BEARER_KEY" > bearer.txt
   $ python -m pip install tox
   $ tox # to run the tests, coverage and build the documentation
   $ python -m pip install -r requirements
   $ python webapp.py # starts the webapp
   # in a different term
   $ python -m tweeterstream.streamer --help
   $ python -m tweeterstream.streamer --tag coop # starts the streaming server

It relies on the following technologies:

- Languages: Python, Javascript
- Web frameworks: Flask, SocketIO
- CLI: Typer
- Build: tox
- Documentation: Sphinx
- Tests: pytest, coverage

Architecture
------------
Even though the specifications mention only the need to stream tweets to a web client in real-time, the architecture takes a few steps to anticipate on future changes:

- Propagate tweets to other consumer types: a bus, a database, a generic consumer
- Propagate tweets to more than one web server, database, etc.
- Apply transformations (or filters, e.g. sensitive content)

The module ``tweeterstream.connectors.connector`` provides a base class that can be derived to implement various consumer protocol: REST, gRPC, SQL, a bus, etc. The base class is designed to ensure connectors remain as self-contained as possible, avoid coupling with the server. This is mainly achieved with the NVI pattern.

*Note: the main package is called tweeterstream for copyright reasons. :)*
  
streamer
********
The module ``streamer`` is a script with the following responsibilities:

- Load the configuration
- Configure the default logging subsystem
- Create the streamer itself
- Apply the rules passed on the command line and start the streamer

webapp
******
The module ``webapp`` is a standard Flask/SocketIO webapp, with the following responsibilities:

- Accept incoming ``POST`` requests from the streamer for each new tweet
- Push new tweets to connected clients through SocketIO


Why not everything on the client-side?
**************************************
It is entirely possible to stream tweets purely on the client-side. Such an approach presents two advantages: it helps keep the architecture to a minimum (i.e., a web server and a small bundle of code run in the browser) and transfers the work to the client-side. This is fine if clients are expected to work fully autonomously.

However, this approach also presents some limitations: control is also transfered to the client. This means that tracking users activity and preparing the content is made harder. Inserting calls to the server in the client-side callbacks would result in the server performing the same work multiple times, and would not scale well. Additionally, this approach would lock the architecture down to a single consumer type, as propagating tweets to other systems would be difficult.

Limitations
***********
In a real-life setting, this project would require a few changes to be considered production-ready:

- The default web server provided with Flask is mono-thread/mono-worker; consider using another web server (e.g. a pre-fork web server, such as gunicorn)
- The bearer key is obtained from a simulated store; consider using a real store like Vault 
- Logging is printed on stdout to remain practical; consider writing to files and shipping to an ELK, for example
- The tests give some ideas as to how to design them: happy and unhappy scenarios, expected failures, inclusion in the default automated build. Consider increasing the coverage, adding integration and 2e2 tests, etc.
- The scripts are run directly from the command line and remain in the foreground to remain practical; consider migrating them to a service (systemd or rc, etc.)

Languages
---------
The server-side is written in Python 3.8. Python was chosen for its simplicity, maturity and its large support in terms of libraries and documentation.

The client-side is written in Javascript, as the needs so far do not call for a more involved framework.

Tools
-----
In order to provide a unified interface to users and CI, and group code, tests and documentation activities, the project relies on ``tox``. ``tox`` in turn invokes various tools like ``pytest`` and ``sphinx`` to do the actual work, and provides an easy way to swap tools here in the future.

Tests
-----
The project comes with a small set of unit tests. In a real-world scenario, integration tests would be required here, as well as e2e tests. Coverage is calculated during the build, and in a real-world scenario, an acceptable level of coverage should be defined and compared with.

Compatibility
-------------
Due to time constraints, this project has only been tested on FreeBSD 13.0-RELEASE-p11, with Python 3.8.10 and Firefox 92.0.

Modules documentation
----------------------

tweeterstream.streamer
**********************
.. automodule:: tweeterstream.streamer
		:members:
		:special-members:

tweeterstream.tweetstreamer
****************************
.. automodule:: tweeterstream.tweetstreamer
		:members:
		:special-members:
		   
tweeterstream.connectors.connector
**********************************
.. automodule:: tweeterstream.connectors.connector
		:members:
		:private-members:
		:special-members: __init__

tweeterstream.connectors.rest_connector
****************************************
.. automodule:: tweeterstream.connectors.rest_connector
		:members:
		:private-members:
		:special-members:

tweeterstream.secret
********************
.. automodule:: tweeterstream.secret
		:members:
		:special-members:
   
		   
.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
