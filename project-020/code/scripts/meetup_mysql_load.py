import meetup_utilities as utils
import logging

class MySQLUpdate(object):
    '''
    Author: mbiswas
    '''

    def __init__(self, config):
        """
        Constructor
        """
        self.config = config
        print '\nPort:',self.config['db_config']['port']
        print '\nDatabase:', self.config['db_config']['db']
        self.db_connection = utils.get_db_connection(self.config['db_config'])


        self.insert_stmt = "INSERT INTO %s " % (self.config['table_name'])
        self.insert_stmt += " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '%s')"

    def update_stats(self, stats_update_sql, stat_file):
        # Update statistics into table
        print "query to be executed : " + stats_update_sql
        cursor = self.db_connection.cursor()
        updated_stats = 0

        f =open(stat_file, 'r')
        for line in iter(f):
            this_total_line = line.rstrip('\n')

            this_line = this_total_line.split(',')

            final_query = stats_update_sql % (this_line[0],this_line[1],this_line[2],this_line[3],this_line[4],this_line[5],this_line[6],this_line[7],this_line[8],this_line[9],this_line[10],this_line[11])
            print 'final query : ', final_query
            cursor.execute(final_query)
            updated_stats += 1

        self.db_connection.commit()
        print "Changes committed to database - updated " + str(updated_stats) + " stats."


    def run(self):
        self.update_stats(self.insert_stmt, self.config['file_name'])