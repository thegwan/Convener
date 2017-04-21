## Sample database
import database as db


# Testing

# Sample time strings
sample1 = "[{'date': '04-22-2017', 'time': '9am'}, {'date': '04-23-2017', 'time': '10am'}, {'date': '04-24-2017', 'time': '11am'}, {'date': '04-25-2017', 'time': '12pm'}, {'date': '04-26-2017', 'time': '1pm'}, {'date': '04-23-2017', 'time': '9am'}, {'date': '04-22-2017', 'time': '10am'}, {'date': '04-22-2017', 'time': '11am'}, {'date': '04-23-2017', 'time': '11am'}, {'date': '04-22-2017', 'time': '12pm'}, {'date': '04-23-2017', 'time': '12pm'}, {'date': '04-24-2017', 'time': '12pm'}, {'date': '04-22-2017', 'time': '1pm'}, {'date': '04-23-2017', 'time': '1pm'}, {'date': '04-24-2017', 'time': '1pm'}, {'date': '04-25-2017', 'time': '1pm'}]"
sample2 = "[{'date': '04-22-2017', 'time': '9am'}, {'date': '04-23-2017', 'time': '10am'}, {'date': '04-24-2017', 'time': '11am'}, {'date': '04-25-2017', 'time': '12pm'}, {'date': '04-26-2017', 'time': '1pm'}]"
sample3 = "[{'date': '04-23-2017', 'time': '10am'}, {'date': '04-24-2017', 'time': '11am'}, {'date': '04-23-2017', 'time': '11am'}, {'date': '04-23-2017', 'time': '12pm'}, {'date': '04-24-2017', 'time': '12pm'}, {'date': '04-23-2017', 'time': '1pm'}, {'date': '04-24-2017', 'time': '1pm'}]"


sample4 = "[{'date': '04-22-2017', 'time': '9am'}, {'date': '04-22-2017', 'time': '10am'}, {'date': '04-22-2017', 'time': '11am'}, {'date': '04-22-2017', 'time': '12pm'}, {'date': '04-22-2017', 'time': '1pm'}, {'date': '04-23-2017', 'time': '9am'}, {'date': '04-23-2017', 'time': '10am'}, {'date': '04-23-2017', 'time': '11am'}, {'date': '04-23-2017', 'time': '12pm'}, {'date': '04-23-2017', 'time': '1pm'}]"
sample5 = "[{'date': '04-22-2017', 'time': '9am'}, {'date': '04-22-2017', 'time': '10am'}, {'date': '04-22-2017', 'time': '11am'}, {'date': '04-22-2017', 'time': '12pm'}]"
sample6 = "[{'date': '04-22-2017', 'time': '10am'}, {'date': '04-22-2017', 'time': '11am'}, {'date': '04-23-2017', 'time': '1pm'}]"


## Create users ###########################################
db.createUser('hsolis', 'Hector', 'Solis')
db.createUser('gwan', 'Gerry')
db.createUser('bargotta')

hector = db.getUser('hsolis')
gerry = db.getUser('gwan')
aaron = db.getUser('bargotta')


## Create meetings  ########################################

db.createMeeting('test1', hector.uid, "[2]", "04-21-2017")
db.createMeeting('test2', hector.uid, "[2]", "04-21-2017")
db.createMeeting('test3', gerry.uid, "[1]", "04-21-2017")
db.createMeeting('test4', gerry.uid, "[1]", "04-21-2017")

## Create responses  ################################################################


db.createResponse(1, hector.uid, sample1)
db.createResponse(2, hector.uid, sample4)
db.createResponse(1, gerry.uid, sample2)
db.createResponse(2, gerry.uid, sample5)
db.createResponse(1, aaron.uid, sample3)
db.createResponse(2, aaron.uid, sample6)

db.createResponse(3, gerry.uid, sample1)
db.createResponse(4, gerry.uid, sample4)
db.createResponse(3, hector.uid, sample2)
db.createResponse(4, hector.uid, sample5)
db.createResponse(3, aaron.uid, sample3)
db.createResponse(4, aaron.uid, sample6)


