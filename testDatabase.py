## Test data for checking if the database properly works
from database import *

# Testing
createUser('hsolis', 'Hector', 'Solis', "{[{'Day':'Fri', 'Time': '12:00'}]}")
createUser('gwan', 'Gerry')
createUser('bargotta', unacceptableTimes="{[{'Day':'Fri', 'Time': '12:00'}]}")
createUser('ksha', 'Sha', acceptableTimes="{[{'Day':'Fri', 'Time': '12:00'}]}")
createUser('kl9', 'Katherine', 'Lee', "{[{'Day':'Mon', 'Time': '18:00'}]}', '{[{'Day':'Tue', 'Time': '12:00'}]}', '{[{'Day':'Sat', 'Time': '9:00'}']}")

createMeeting('Colonial Dinner', 1, '[2,4]')

createResponse(1, 1, "{[{'Day':'Fri', 'Time': '6:00'}]}")
createResponse(1, 2, "{[{'Day':'Fri', 'Time': '6:00'}]}")
createResponse(1, 3, "{[{'Day':'Fri', 'Time': '6:00'}]}")

updateUser('hsolis', 'Hector', 'Solis', "{[{'Day':'Fri', 'Time': '12:00'}]}", "{[{'Day':'Mon', 'Time': '11:00'}]}", "{[{'Day':'Wed', 'Time': '3:00'}]}")

updateMeeting(1, True, "{[{'Day': 'Fri', 'Time': '18:00'}]}")
