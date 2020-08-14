import pymysql

def getDetails(NPnumber):
	print(NPnumber)
	Details = {}
	connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='vehicle_fine',)

	query = 'SELECT owner_name FROM `ownerTable` WHERE Vehicle_Number='+'"'+NPnumber+'"'+';'
	c = connection.cursor()
	row = c.execute(query)
	row = c.fetchall()
	Details['OwnerName']=row[0][0]

	query = 'SELECT license_number FROM `ownerTable` WHERE Vehicle_Number='+'"'+NPnumber+'"'+';'
	row = c.execute(query)
	row = c.fetchall()
	Details['LicenseNumber']=row[0][0]

	query = 'SELECT owner_address FROM `ownerTable` WHERE Vehicle_Number='+'"'+NPnumber+'"'+';'
	row = c.execute(query)
	row = c.fetchall()
	Details['OwnerAddress']=row[0][0]

	query = 'SELECT owner_email FROM `ownerTable` WHERE Vehicle_Number='+'"'+NPnumber+'"'+';'
	row = c.execute(query)
	row = c.fetchall()
	Details['OwnerEmail']=row[0][0]

	query = 'SELECT contactno FROM `ownerTable` WHERE Vehicle_Number=' + '"' + NPnumber + '"' + ';'
	row = c.execute(query)
	row = c.fetchall()
	Details['contactno'] = row[0][0]


	return Details








