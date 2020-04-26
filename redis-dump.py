import json
import redis
import sys
import optparse
import datetime

def dump(fp, keys="*", host='localhost', port=6379, password=None, db=0, pretty=False, ssl=False):
    r = redis.Redis(host=host, port=port, password=password, db=db, ssl=ssl)
    kwargs = {}
    if not pretty:
        kwargs['separators'] = (',', ':')
    else:
        kwargs['indent'] = 2
        kwargs['sor_keys'] = True

    encoder = json.JSONEncoder(**kwargs)

    key_count = 0

    for key, type, value in _reader(r, keys, pretty):
        d = {}
        d[key] = {'type':type, 'value':value}
        item = encoder.encode(d)
        fp.write(item)
        fp.write("\n")
        key_count = key_count + 1

    print >> sys.stderr, key_count, ' keys dumped into the file'

def load(fp, host='localhost', port=6379, password=None, db=0, ssl=False):
    r = redis.Redis(host=host, port=port, password=password, db=db, ssl=ssl)
    pipe = r.pipeline()
    size = 0
    key_count = 0
    for s in fp.xreadlines():
        table = json.loads(s)
        size = size + s.__len__()
        for key in table:
            item = table[key]
            type = item['type']
            value = item['value']
            _writer(pipe, key, type, value)
            key_count = key_count + 1
        if size > 1024*1024*5:
            pipe.execute()
            pipe = r.pipeline()
            size = 0
    pipe.execute()
    print >> sys.stderr, key_count, ' keys inserted into redis'

def _reader(r, keys, pretty):
    kys = r.keys(keys)
    #print >> sys.stderr, len(kys), ' keys found'
    for key in kys:
        type = r.type(key)
        if type == 'string':
            value = r.get(key)
            #print >> sys.stderr, 'String type : ', key
        elif type == 'list':
            value = r.lrange(key, 0, -1)
            #print >> sys.stderr, 'List type : ', key
        elif type == 'set':
            value = list(r.smembers(key))
            if pretty:
                value.sort()
            #print >> sys.stderr, 'Set type : ', key
        elif type == 'zset':
            value = r.zrange(key, 0, -1, False, True)
            #print >> sys.stderr, 'ZSet type : ', key
        elif type == 'hash':
            value = r.hgetall(key)
            #print >> sys.stderr, 'Hash type : ', key
        else:
            raise UnknownTypeError('Unknown key type: %s' % type)
        yield key, type, value

def _writer(pipe, key, type, value):
    if type == 'string':
        pipe.set(key, value)
    elif type == 'list':
        for element in value:
            pipe.rpush(key, element)
    elif type == 'set':
        for element in value:
            pipe.sadd(key, element)
    elif type == 'zset':
        for element in value:
            pipe.zadd(key, {element[0]: element[1]})
    elif type == 'hash':
        for element in value.keys():
            pipe.hset(key, element, value[element])
    else:
        raise UnknownTypeError("Unknown key type: %s" % type)


def opions_to_kwargs(options):
    args = {}
    if options.host:
        args['host'] = options.host
    if options.port:
        args['port'] = int(options.port)
    if options.password: 
        args['password'] = options.password
    if options.db:
        args['db'] = int(options.db)
    if options.ssl:
        args['ssl'] = options.ssl
    if options.load:
        args['load'] = options.load
    if options.save:
        args['save'] = options.save
    if options.key:
        args['key'] = options.key
    return args

def generate_filename():
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")

def process(options):

    args = opions_to_kwargs(options)

    if options.save  and options.load:
        print >> sys.stderr, 'either load or save option should be enabled'
    elif options.save:
        if (args['save'] == '-'):
            output = sys.stdout
        else:
            output = open(args['save'], 'w')
        dump(output, args['key'] if options.key else "*", args['host'], args['port'], args.get('password'), args['db'], args['ssl'])
        output.close()
    elif options.load:
        if (args['load'] == '-'):
            input = sys.stdin
        else:
            input = open(args['load'], 'r')
        load(input, args['host'], args['port'], args.get('password'), args['db'], args['ssl'])
        input.close()
    else:
        print >> sys.stderr, 'either load or save option should be enabled'
        return False

    return True

def get_usages():
    usage = "Usage: %prog [options]"
    usage += "\n\nDump specific keys from a redis to a file."
    usage += "\n\nLoad data from a file to redis."
    return usage

if __name__ == '__main__':
    parser = optparse.OptionParser(usage=get_usages())
    parser.add_option('-m', '--host', default='localhost', help='connect to HOST(default is localhost)')
    parser.add_option('-p', '--port', default=6379, help='connect to PORT(default is 6379)')
    parser.add_option('-w', '--password', help='connect with PASSWORD(default is None')
    parser.add_option('-d', '--db', help='dump DATABASE (0-N, default 0)')
    parser.add_option('-e', '--ssl', default=False, help='connect to redis with SSL(default is False)')
    parser.add_option('-l', '--load', help='Load from dump file or stdin if "-" passed in')
    parser.add_option('-s', '--save', help='Save to dump file or stdout if "-" passed in')
    parser.add_option('-k', '--key', help='Search Key(default is *)')

    options, args = parser.parse_args()

    if not process(options):
        parser.print_help()
