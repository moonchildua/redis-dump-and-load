redis-dumpy help
--------------------------------------------------
<pre>
(tut)redis-dump-and-load-$ python redis-dump.py -h
Usage: redis-dump.py [options]

Dump specific keys from a redis to a file.

Load data from a file to redis.

Options:
  -h, --help            show this help message and exit
  -m HOST, --host=HOST  connect to HOST(default is localhost)
  -p PORT, --port=PORT  connect to PORT(default is 6379)
  -w PASSWORD, --password=PASSWORD
                        connect with PASSWORD(default is None
  -d DB, --db=DB        dump DATABASE (0-N, default 0)
  -e SSL, --ssl=SSL     connect with SSL(default is False) 
  -l LOAD, --load=LOAD  Load from dump file
  -s SAVE, --save=SAVE  Save to dump file
  -k KEY, --key=KEY     Search Key(default is *)

(tut)redis-dump-and-load-$ python redis-dump.py -s data.js -k asit*
475  keys dumped into the file

(tut)redis-dump-and-load-$ python redis-dump.py -l data.js
475  keys inserted into redis
</pre>

origin of redis-dump-and-load without SSL you can find follow the link https://github.com/asit-dhal/redis-dump-and-load