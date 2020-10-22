# coding=utf8
# Copyright (c) 2019 GVF
# Author: Chenglin(Niko) Lu
# Version: V1.0.0
"""GDB Package

GDB Package is a bridge that handles database connections.

Update History:
    V1.0.0: Comes with working GMySQLConnector and GLog

    APIs:

    class GMySQLConnector():

        constructor(dict CONFIG)          -Init a connector with CONFIG

        ---ACCESSORS---
        dict example_config()             -Get a example CONFIG
        dict get_config()                 -Get CONFIG
        void set_config()                 -Set CONFIG
        void enable_quiet_mode()          -No Console Write
        void disable_quiet_mode()         -Console Write

        ---AUTO MODE---
        dict    auto_query(String sql_line, String sql_data=Null)            - Perform query and return data
        Boolean auto_write(String sql_line, String sql_data=Null)            - Write to Database
        Boolean auto_write_many(List[String sql_line, String sql_data=Null]) - Write Multiple Lines to Database

        ---MANUAL MODE---
        Boolean start()                   -Start Connection
        Boolean execute()                 -Execute SQL statements
        Boolean fetch()                   -Fetch Query Results
        Boolean commit()                  -Commit changes to database
        Boolean rollback()                -Discard changes
        Boolean close()                   -Close Connection


    class GLog():

        @Static
        print_result(title, result)           - Default Viewer of Log (Using Print)

        constructor()                         - Init a GLog (Auto Quiet Mode)

        ---ADMIN---
        Boolean restore_schema()              - Dangerous, re-create the database. DROP ALL APP LOGS
        Boolean register_app(string app_name) - Register a LOG space for certain app
        Boolean delete_app(string app_name)   - Remove LOG space for certain app, DROP LOGS OF THAT APP

        ---LOGGING---
        Boolean log(string app_name,          - log a record with corresponding information.
                    string user,                All fields can leave Null except app_name
                    string action,
                    string subject,
                    Boolean reuslt,
                    string comment)

        ---READING---
        Dict fetch(string app_name            - Fetch one or more records of app_name
                      string min_id             Following arguments are optional
                      string max_id             Use them as search conditions.
                      string min_datetime
                      string max_datetime
                      string min_unix_timestamp
                      string max_unix_timestamp
                      string user,
                      string action,
                      string subject,
                      Boolean result,
                      string comment,
                      )

        ---AUTO MODE---
        dict    auto_query(String sql_line, String sql_data=Null)            - Perform query and return data
        Boolean auto_write(String sql_line, String sql_data=Null)            - Write to Database
        Boolean auto_write_many(List[String sql_line, String sql_data=Null]) - Write Multiple Lines to Database

        ---MANUAL MODE---
        Boolean start()                   -Start Connection
        Boolean execute()                 -Execute SQL statements
        Boolean fetch()                   -Fetch Query Results
        Boolean commit()                  -Commit changes to database
        Boolean rollback()                -Discard changes
        Boolean close()                   -Close Connection

"""
import mysql.connector
import time
from datetime import datetime
from mysql.connector import errorcode


class GMySQLConnector(object):
    @staticmethod
    def example_config():
        """This function returns a example/template CONFIG

        Returns:
            A template config dictionary

        """
        return {
            'user': None,
            'password': None,
            'host': None,
            'database': None,
        }

    def __init__(self, connection_config=None):
        """This is the constructor that you will use.

        Args:
            dict connection_config: the config, you can require from example_config()
        """

        self.config = None
        self.conn = None
        self.cursor = None
        self.quiet_mode = False
        self.set_config(connection_config)

    def get_config(self):
        """Regular Getter

        Returns: dict CONFIG

        """
        return self.config

    def set_config(self, config):
        """Regular Setter

        Args:
            dict config: you can require one from example_config()

        """
        if config:
            self.config = config
        else:
            self.config = self.example_config()

    def enable_quiet_mode(self):
        """Enable No-Console Write Feature"""
        self.quiet_mode = True

    def disable_quiet_mode(self):
        """Disable No-Console Write Feature"""
        self.quiet_mode = False

    def error_display(self, error_string):
        """Private Print Function"""
        if not self.quiet_mode:
            print(error_string)

    def auto_query(self, sql_line, sql_data=None):
        """Feed in the READ-ONLY SQL Line, Hand back the result. Easy.

        Args:
            str sql_line: where you usually put the sql query line

        Returns:
            Boolean/Dict Result

            If Fail: False
            If Success:
                [{line1},{line2},{line3}]

        """
        return_value = False
        connection = None

        try:
            connection = mysql.connector.connect(**self.config)
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql_line, sql_data)
            return_value = cursor.fetchall()
        except mysql.connector.Error as e:
            self.error_display("GDB.MySQL.auto_query => SQL ERROR\n{}".format(e))
        except Exception as e:
            self.error_display("GDB.MySQL.auto_query => PYTHON ERROR\n{}".format(e))
        finally:
            try:
                connection.close()
            except Exception as e:
                self.error_display("GDB.MySQL.auto_query => CONN CLOSE FAILED\n{}".format(e))

        return return_value

    def auto_write(self, sql_line, sql_data=None):
        """Feed in one WRITE-ONLY SQL line, boom, easy

        Args:
            str sql_line: One SQL line that WRITE into databse

        Returns:
            Boolean: True if success, False if failed.

        """
        return_value = False
        connection = None

        try:
            connection = mysql.connector.connect(**self.config)
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql_line, sql_data)
            connection.commit()
            return_value = True
        except mysql.connector.Error as e:
            self.error_display("GDB.MySQL.auto_write => SQL ERROR\n{}".format(e))
        except Exception as e:
            self.error_display("GDB.MySQL.auto_write => PYTHON ERROR\n{}".format(e))
        finally:
            try:
                if not return_value:
                    connection.rollback()
                    self.error_display("GDB.MySQL.auto_write => ROLLBACK")
            except Exception as e:
                self.error_display("GDB.MySQL.auto_write => AUTO ROLLBACK FAILED\n{}".format(e))
            try:
                connection.close()
            except Exception as e:
                self.error_display("GDB.MySQL.auto_write => CONN CLOSE FAILED\n{}".format(e))

        return return_value

    def auto_write_many(self, sql_lines=None):
        """Feed in a list of WRITE-ONLY SQL lines, On Error Auto Rollback, Cool, yeah?

        Args:
            str sql_lines: [SQL_Line1, SQL_Line2, ...]

        Returns:
            Boolean: True if success, False if any of them failed.

        """
        return_value = False
        connection = None

        if not isinstance(sql_lines, list):
            self.error_display("GDB.MySQL.auto_write_many => SQL lines must pack in List")
            return False

        try:
            connection = mysql.connector.connect(**self.config)
            cursor = connection.cursor(dictionary=True)
            for sql_line_obj in sql_lines:
                sql_line = None
                sql_data = None
                if isinstance(sql_line_obj, str):
                    sql_line = sql_line_obj
                elif isinstance(sql_line_obj, list) and len(sql_line_obj) == 2:
                    sql_line = sql_line_obj[0]
                    sql_data = sql_line_obj[1]
                else:
                    raise ValueError('SQL line must a String or [sql_line, sql_data]')
                cursor.execute(sql_line, sql_data)
            connection.commit()
            return_value = True
        except mysql.connector.Error as e:
            self.error_display("GDB.MySQL.auto_write_many => SQL ERROR\n{}".format(e))
        except Exception as e:
            self.error_display("GDB.MySQL.auto_write_many => PYTHON ERROR\n{}".format(e))
        finally:
            try:
                if not return_value:
                    connection.rollback()
                    self.error_display("GDB.MySQL.auto_write_many => AUTO ROLLBACK")
            except Exception as e:
                self.error_display("GDB.MySQL.auto_write_many => ROLLBACK FAILED\n{}".format(e))
            try:
                connection.close()
            except Exception as e:
                self.error_display("GDB.MySQL.auto_write_many => CONN CLOSE FAILED\n{}".format(e))

        return return_value

    def start(self):
        """Manually Starting the Connection

        You shouldn't be using this unless you really know what you are doing.

        Returns:
            Boolean: True if success, False if any of them failed.

        """
        return_value = False

        try:
            self.conn = mysql.connector.connect(**self.config)
            self.cursor = self.conn.cursor(dictionary=True)
            return_value = True
        except mysql.connector.Error as e:
            self.error_display("GDB.MySQL.start => SQL ERROR\n{}".format(e))
        except Exception as e:
            self.error_display("GDB.MySQL.start => PYTHON ERROR\n{}".format(e))

        return return_value

    def execute(self, sql_line, sql_data=None):
        """Manually Executing SQL

        You shouldn't be using this unless you really know what you are doing.

        Args:
            sql_line: str SQL line or SQL Template
            sql_data: list/dict that holds data

        Returns:
            boolean: True if success, False if failed

        """
        return_value = False

        try:
            self.cursor.execute(sql_line, sql_data)
            return_value = True
        except mysql.connector.Error as e:
            self.error_display("GDB.MySQL.execute => SQL ERROR\n{}".format(e))
        except Exception as e:
            self.error_display("GDB.MySQL.execute => PYTHON ERROR\n{}".format(e))

        return return_value

    def fetch(self):
        """Manually Fetching Query Result

        You shouldn't be using this unless you really know what you are doing.

        Returns:
            dict: if success
            False: if failed

        """
        return_value = False

        try:
            return_value = self.cursor.fetchall()
        except mysql.connector.Error as e:
            self.error_display("GDB.MySQL.fetch => SQL ERROR\n{}".format(e))
        except Exception as e:
            self.error_display("GDB.MySQL.fetch => PYTHON ERROR\n{}".format(e))

        return return_value

    def commit(self):
        """Manually Commit Changes to Database

        You shouldn't be using this unless you really know what you are doing.

        Returns:
            boolean: True if success, False if failed

        """
        return_value = False

        try:
            self.conn.commit()
            return_value = True
        except mysql.connector.Error as e:
            self.error_display("GDB.MySQL.commit => SQL ERROR\n{}".format(e))
        except Exception as e:
            self.error_display("GDB.MySQL.commit => PYTHON ERROR\n{}".format(e))

        return return_value

    def rollback(self):
        """Manually Rollback

        You shouldn't be using this unless you really know what you are doing.

        Returns:
            boolean: True if success, False if failed

        """
        return_value = False

        try:
            self.conn.rollback()
            return_value = True
        except mysql.connector.Error as e:
            self.error_display("GDB.MySQL.rollback => SQL ERROR\n{}".format(e))
        except Exception as e:
            self.error_display("GDB.MySQL.rollback => PYTHON ERROR\n{}".format(e))

        return return_value

    def close(self):
        """Manually Closing the connection

        You shouldn't be using this unless you really know what you are doing.

        Returns:
            boolean: True if success, False if failed

        """
        return_value = False

        try:
            if self.conn:
                self.conn.close()
                self.conn = None
            self.cursor = None
            return_value = True
        except mysql.connector.Error as e:
            self.error_display("GDB.MySQL.rollback => SQL ERROR\n{}".format(e))
        except Exception as e:
            self.error_display("GDB.MySQL.rollback => PYTHON ERROR\n{}".format(e))

        return return_value


class GLog(object):

    @staticmethod
    def print_result(title, results):
        """ Format & Print a fetch() result

        Args:
            title: The title you wanna display
            results: The fetch result from GLog Module

        """
        eqCharLen = int((130 - len(title)) / 2)
        print("=" * eqCharLen + title + "=" * eqCharLen)
        print("%-5s%-35s%-20s%-20s%-30s%-10s%-30s" % (
        "id", "datetime", "user", "action", "subject", "result", "comment"))
        for line in results:
            data = (
                str(line['id']),
                str(line['datetime']) + "(" + str(datetime.fromtimestamp(line['datetime'])) + ")",
                str(line['user']),
                str(line['action']),
                str(line['subject']),
                str(bool(line['result'])),
                str(line['comment'])
            )
            print("%-5s%-35s%-20s%-20s%-30s%-10s%-30s" % data)
        print("=" * 130 + '\n')

    def __init__(self):
        """CONSTRUCTOR

        Connect to DB with GLog unique account.
        Quiet Mode

        """
        self.LOGGER_DB_CONFIG = {
            'user': 'GLogApp',
            'password': 'GLogApp',
            'host': '10.10.20.12',
            'database': 'GLog',
        }

        self.db_connector = GMySQLConnector(self.LOGGER_DB_CONFIG)
        self.db_connector.enable_quiet_mode()

        # self.LOGGER_DB_CONFIG = {
        #     'user': 'root',
        #     'password': 'root',
        #     'host': 'localhost',
        #     'database': 'GLog',
        # }

    def set_demo_data(self):
        """ Insert example data into GLog

        Returns: Boolean - True if success, False if failed

        """
        self.delete_app("GLog")
        self.register_app("GLog")
        sql_line = (
            'INSERT INTO GLog () VALUES '
            '(NULL, "2019-01-01 12:00:00", "Niko",  "Create", "Database", True, "Ok"),'
            '(NULL, "2019-01-01 13:00:00", "Vitaliy",  "Search", "Table", True, "Ok"),'
            '(NULL, "2019-01-01 14:00:00", "Niko",  "Drop", "Function", True, "Ok"),'
            '(NULL, "2019-01-02 12:00:00", "Niko",  "Create", "Database", False, "Bad"),'
            '(NULL, "2019-01-02 13:00:00", "Vitaliy",  "Search", "Table", False, "Bad"),'
            '(NULL, "2019-01-02 14:00:00", "Niko",  "Drop", "Function", False, "Bad"),'
            '(NULL, "2019-01-03 12:00:00", "Niko",  "Create", "Database", True, "Ok"),'
            '(NULL, "2019-01-03 13:00:00", "Vitaliy",  "Search", "Table", True, "Ok"),'
            '(NULL, "2019-01-03 14:00:00", "Niko",  "Drop", "Function", False, "Bad");')
        return self.db_connector.auto_write(sql_line)

    def restore_schema(self):
        """ DANGEROUS RE-CREATE the GLog database WARNING

        Returns: Boolean - True if success, False if failed

        """
        sql_lines = []
        sql_lines.append("DROP DATABASE IF EXISTS GLog;")
        sql_lines.append("CREATE DATABASE GLog;")
        return self.db_connector.auto_write_many(sql_lines)

    def register_app(self, app_name):
        """ Register a Log space for application

        Args:
            app_name: Your applciation name

        Returns:
            Returns: Boolean - True if success, False if failed

        """
        sql_line = ("CREATE TABLE IF NOT EXISTS `" + app_name + "` ("
                                                                "id INT NOT NULL AUTO_INCREMENT,"
                                                                "log_datetime timestamp,"
                                                                "log_user varchar(128),"
                                                                "log_action varchar(16),"
                                                                "log_subject varchar(128),"
                                                                "log_result bool,"
                                                                "log_comment varchar(4096),"
                                                                "PRIMARY KEY(id)"
                                                                ");")

        return self.db_connector.auto_write(sql_line)

    def delete_app(self, app_name):
        """ Delete a Log space for application

        Args:
            app_name: Your applciation name

        Returns:
            Returns: Boolean - True if success, False if failed

        """
        sql_line = ("DROP TABLE IF EXISTS `" + app_name + "`;")
        return self.db_connector.auto_write(sql_line)

    def log(self, app_name="", user="", action="", subject="", result=True, comment=""):
        """ Log into the database

        Args:
            app_name: REQUIRED - your registered app_name
            user:     OPTIONAL - ex. Tom
            action:   OPTIONAL - ex. Play
            subject:  OPTIONAL - ex. Football
            result:   OPTIONAL - ex. True, False
            comment:  OPTIONAL - ex. He also broke his leg on that kick.

        Returns:
            Returns: Boolean - True if success, False if failed

        """
        if not app_name:
            print ("GDB.GLog.log(): app_name can't left blank")
            return False
        else:
            sql_data = {
                "table_name": str(app_name),
                "user": str(user),
                "action": str(action),
                "subject": str(subject),
                "result": result,
                "comment": str(comment)
            }
            sql_line = ('INSERT INTO %(table_name)s () VALUES ('
                        'NULL,'
                        'NOW(),'
                        '"%(user)s",'
                        '"%(action)s",'
                        '"%(subject)s",'
                        '%(result)s,'
                        '"%(comment)s");') % sql_data

            return self.db_connector.auto_write(sql_line)

    def fetch(self,
              app_name=None,
              min_id=None,
              max_id=None,
              min_datetime=None,
              max_datetime=None,
              min_unix_timestamp=None,
              max_unix_timestamp=None,
              user=None,
              action=None,
              subject=None,
              result=None,
              comment=None):
        """ Fetch one or more records from DB

        Args:
            app_name:           REQUIRED - your registered app_name
            min_id:             OPTIONAL - ex. 2
            max_id:             OPTIONAL - ex. 4
            min_datetime:       OPTIONAL - ex. "2019-04-03 12:00:00"
            max_datetime:       OPTIONAL - ex. "2019-04-04 13:00:00"
            min_unix_timestamp: OPTIONAL - ex. 1546495200
            max_unix_timestamp: OPTIONAL - ex. 1546318800
            user:               OPTIONAL - ex. "tom"
            action:             OPTIONAL - ex. "play"
            subject:            OPTIONAL - ex. "football"
            result:             OPTIONAL - ex. True, False
            comment:            OPTIONAL - ex. "break"

        Returns:
            Returns: Boolean - True if success, False if failed
        """

        if not app_name:
            print ("GDB.GLog.fetch(): app_name can't left blank")
            return False

        conditions = []
        if min_id:
            conditions.append(" id >= " + str(min_id) + " ")
        if max_id:
            conditions.append(" id <= " + str(max_id) + " ")
        if min_datetime:
            conditions.append(' log_datetime >= "' + str(min_datetime) + '" ')
        if max_datetime:
            conditions.append(' log_datetime <= "' + str(max_datetime) + '" ')
        if min_unix_timestamp:
            conditions.append(' unix_timestamp(log_datetime) >= ' + str(int(min_unix_timestamp)) + ' ')
        if max_unix_timestamp:
            conditions.append(' unix_timestamp(log_datetime) <= ' + str(int(max_unix_timestamp)) + ' ')
        if user:
            conditions.append(' log_user LIKE "%' + str(user) + '%" ')
        if action:
            conditions.append(' log_action LIKE "%' + str(action) + '%" ')
        if subject:
            conditions.append(' log_subject LIKE "%' + str(subject) + '%" ')
        if result is not None:
            if result:
                conditions.append(' log_result = 1 ')
            else:
                conditions.append(' log_result = 0 ')
        if comment:
            conditions.append(' log_comment LIKE "%' + str(comment) + '%" ')

        sql_line = ("SELECT "
                    "`id` AS `id`, "
                    " UNIX_TIMESTAMP(`log_datetime`) AS `datetime`, "
                    "`log_user` AS `user`, "
                    "`log_action` AS `action`, "
                    "`log_subject` AS `subject`, "
                    "`log_result` AS `result`, "
                    "`log_comment` AS `comment` "
                    "FROM "
                    "GLog")
        if conditions:
            condition_line = " WHERE "
            for idx, condition in enumerate(conditions):
                condition_line += condition
                if idx != len(conditions) - 1:
                    condition_line += " AND "
            sql_line += condition_line

        return self.db_connector.auto_query(sql_line)
