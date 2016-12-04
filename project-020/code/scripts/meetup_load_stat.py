import sys
from meetup_mysql_load import MySQLUpdate



def main(config):
    print 'main() method'
    mySQLUpdate = MySQLUpdate(config)
    mySQLUpdate.run()




if __name__ == "__main__":

    config = {
	"db_config" : {
		"host": "localhost",
		"port": 3306,
		"user": "meetup",
		"passwd": "passw0rd",
		"db": "meetup"
	    }
    }

    table_name = sys.argv[1]
    file_name = sys.argv[2]

    config['table_name'] = table_name
    config['file_name'] = file_name
    main(config)
