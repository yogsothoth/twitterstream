# TwitterStream

**TwitterStream** streams tweets from twitter and presents them on a web interface in real-time.

## Getting started
```
$ git clone https://github.com/yogsothoth/twitterstream.git
$ cd twitterstream
$ python -m venv default
$ source default/bin/activate # for a bourne shell
$ echo "MY_BEARER_KEY" > bearer.txt
$ python -m pip install tox
$ tox # to run the tests, coverage and build the documentation
$ python -m pip install -r requirements.txt
$ python webapp.py # starts the webapp
# in a different term
$ python -m tweeterstream.streamer --help
$ python -m tweeterstream.streamer --tag coop # starts the streaming server
```

Then point your browser to `http://127.0.0.1:5000`.


## Documentation
After running `tox`, the documentation will be available in '.tox/docs/tmp/html/', point your browser to the file index.html found in this directory.



