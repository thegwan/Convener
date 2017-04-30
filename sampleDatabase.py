## Sample database
import database as db


# Testing

# Sample time strings
sample1 = "[{'date': '04-22-2017', 'time': '9:00am'}, {'date': '04-23-2017', 'time': '10:00am'}, {'date': '04-24-2017', 'time': '11:30am'}, {'date': '04-25-2017', 'time': '12:30pm'}, {'date': '04-26-2017', 'time': '1:00pm'}, {'date': '04-23-2017', 'time': '9:00am'}, {'date': '04-22-2017', 'time': '10:00am'}, {'date': '04-22-2017', 'time': '11:30am'}, {'date': '04-23-2017', 'time': '11:30am'}, {'date': '04-22-2017', 'time': '12:30pm'}, {'date': '04-23-2017', 'time': '12:30pm'}, {'date': '04-24-2017', 'time': '12:30pm'}, {'date': '04-22-2017', 'time': '1:00pm'}, {'date': '04-23-2017', 'time': '1:00pm'}, {'date': '04-24-2017', 'time': '1:00pm'}, {'date': '04-25-2017', 'time': '1:00pm'}]"
sample2 = "[{'date': '04-22-2017', 'time': '9:00am'}, {'date': '04-23-2017', 'time': '10:00am'}, {'date': '04-24-2017', 'time': '11:30am'}, {'date': '04-25-2017', 'time': '12:30pm'}, {'date': '04-26-2017', 'time': '1:00pm'}]"
sample3 = "[{'date': '04-23-2017', 'time': '10:00am'}, {'date': '04-24-2017', 'time': '11:30am'}, {'date': '04-23-2017', 'time': '11:30am'}, {'date': '04-23-2017', 'time': '12:30pm'}, {'date': '04-24-2017', 'time': '12:30pm'}, {'date': '04-23-2017', 'time': '1:00pm'}, {'date': '04-24-2017', 'time': '1:00pm'}]"


sample4 = "[{'date': '04-22-2017', 'time': '9:00am'}, {'date': '04-22-2017', 'time': '10:00am'}, {'date': '04-22-2017', 'time': '11:30am'}, {'date': '04-22-2017', 'time': '12:30pm'}, {'date': '04-22-2017', 'time': '1:00pm'}, {'date': '04-23-2017', 'time': '9:00am'}, {'date': '04-23-2017', 'time': '10:00am'}, {'date': '04-23-2017', 'time': '11:30am'}, {'date': '04-23-2017', 'time': '12:30pm'}, {'date': '04-23-2017', 'time': '1:00pm'}]"
sample5 = "[{'date': '04-22-2017', 'time': '9:00am'}, {'date': '04-22-2017', 'time': '10:00am'}, {'date': '04-22-2017', 'time': '11:30am'}, {'date': '04-22-2017', 'time': '12:30pm'}]"
sample6 = "[{'date': '04-22-2017', 'time': '10:00am'}, {'date': '04-22-2017', 'time': '11:30am'}, {'date': '04-23-2017', 'time': '1:00pm'}]"


## Create users ###########################################
db.createUser('hsolis', 'Hector', 'Solis')
db.createUser('gwan', 'Gerry')
db.createUser('bargotta')

hector = db.getUser('hsolis')
gerry = db.getUser('gwan')
aaron = db.getUser('bargotta')


## Create meetings  ########################################

db.createMeeting('test1', hector.uid, "[2, 3]", "04-21-2017")
db.createMeeting('test2', hector.uid, "[2, 3]", "04-21-2017")
db.createMeeting('test3', gerry.uid, "[1, 3]", "04-21-2017")
db.createMeeting('test4', gerry.uid, "[1, 3]", "04-21-2017")
db.createMeeting('test5', aaron.uid, "[2]", "04-21-2017")

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

db.createResponse(5, aaron.uid, sample1)


