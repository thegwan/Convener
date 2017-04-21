## Sample database
import database as db


# Testing

# Sample time strings
sample1 = "[{'date': '04-22-2017', 'time': '9am'}, {'date': '04-23-2017', 'time': '10am'}, {'date': '04-24-2017', 'time': '11am'}, {'date': '04-25-2017', 'time': '12pm'}, {'date': '04-26-2017', 'time': '1pm'}]"
sample2 = "[{'date': '04-22-2017', 'time': '9am'}, {'date': '04-23-2017', 'time': '9am'}, {'date': '04-22-2017', 'time': '10am'}, {'date': '04-23-2017', 'time': '10m'}, {'date': '04-22-2017', 'time': '11am'}, {'date': '04-23-2017', 'time': '11am'}]"


## Create users ###########################################
db.createUser('hsolis', 'Hector', 'Solis')
db.createUser('gwan', 'Gerry')

hector = db.getUser('hsolis')
gerry = db.getUser('gwan')


## Create meetings  ########################################

db.createMeeting('test1', hector.uid, "[2]", "04-21-2017")
db.createMeeting('test2', hector.uid, "[2]", "04-21-2017")
db.createMeeting('test3', gerry.uid, "[1]", "04-21-2017")
db.createMeeting('test4', gerry.uid, "[1]", "04-21-2017")

## Create responses  ################################################################


db.createResponse(1, 1, sample1)
db.createResponse(2, 1, sample2)
db.createResponse(1, 2, sample2)
db.createResponse(2, 2, sample1)
db.createResponse(3, 2, sample2)
db.createResponse(4, 2, sample1)
db.createResponse(3, 1, sample1)
db.createResponse(4, 1, sample2)


