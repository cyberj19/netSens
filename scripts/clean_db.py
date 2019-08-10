import sys
import pymongo

mhost = 'localhost'
mport = 27017
mdb = 'netSens'

if len(sys.argv) == 3:
	mhost = sys.argv[1]
	mport = sys.argv[2]
elif len(sys.argv) == 2:
	mhost = sys.argv[1]
	
print 'Connecting to %s:%d/%s...' % (mhost, mport, mdb)
client = pymongo.MongoClient(mhost, mport)

try:
	client.server_info()
except Exception, e:
	print 'Unable to connect to host'
	sys.exit(0)
# if not mdb in client.list_database_names():
	# print 'No db %s on host. Exiting' % mdb
	
print 'Dropping collections...'
for collection in client[mdb].collection_names():
	print 'Dropping collection %s' % collection
	client[mdb][collection].drop()