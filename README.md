asit@asit-laptop:~/rb/py/jojo$ python redis-dump.py -h
Usage: redis-dump.py [options]

Dump specific keys from a redis to a file.

Load data from a file to redis.

Options:
  -h, --help            show this help message and exit
  -m HOST, --host=HOST  connect to HOST
  -p PORT, --port=PORT  connect to PORT
  -w PASSWORD, --password=PASSWORD
                        connect with PASSWORD
  -d DB, --db=DB        dump DATABASE (0-N, default 0)
  -l LOAD, --load=LOAD  Load from dump file
  -s SAVE, --save=SAVE  Save to dump file
  -k KEY, --key=KEY     Search Key

asit@asit-laptop:~/rb/py/jojo$ python redis-dump.py -s data.js -k "asit*"
14  keys found
List type :  asit_2013-11-13_1
List type :  asit_2013-11-13_2
List type :  asit_2013-11-07_3
List type :  asit_2013-11-06_4
List type :  asit_2013-11-06_5
List type :  asit_2013-11-06_6
List type :  asit_2013-11-07_7
List type :  asit_2013-10-31_8
List type :  asit_2013-10-31_9
List type :  asit-2013-11-06_10
List type :  asit_2013-11-07_11
List type :  asit_2013-11-06_12
List type :  asit_2013-11-14_13
List type :  asit_2013-11-06_14
asit@asit-laptop:~/rb/py/jojo$ python redis-dump.py -l data.js
14  keys inserted
asit@asit-laptop:~/rb/py/jojo$ 
