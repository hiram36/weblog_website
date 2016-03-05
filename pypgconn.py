#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import psycopg2
import sys
from prettytable import PrettyTable

 
def pg_conn(conn_string):
    #Define our connection string
    #conn_string = "host='localhost' dbname='daysbaydb' user='hshl' password='hshl123'"
 
    # print the connection string we will use to connect
    #print ("Connecting to database\n	->%s" % (conn_string))
 
    # get a connection, if a connect cannot be made an exception will be raised here
    try:
        conn = psycopg2.connect(conn_string)
    except psycopg2.Error as e:
        print ("Connect to the postgresql database failed!!!\n")
        print (e.pgerror)
        print (e.diag.message_detail)
        sys.exit(1)
    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    print ("Connected to postgresql database successfully.\n")
   
    return conn


def pg_dml(conn):
    cur = conn.cursor()
    try:
        cur.execute('''CREATE TABLE COMPANY
           (
               ID INT PRIMARY KEY     NOT NULL,
               NAME           TEXT    NOT NULL,
               AGE            INT     NOT NULL,
               ADDRESS        CHAR(50),
               SALARY         REAL
           );''')
    except:
        print ("DDL execute failed!!!\n")

    print ("Table created successfully")
    conn.commit()


def pg_metadata(conn, query_stmt): 
    cursor = conn.cursor()
    try:
        cursor.execute(query_stmt)
        #cursor.execute("select * from bs_position_account limit 10;")
    except psycopg2.DatabaseError as e:
        print ("Execute failed!!!")
        print (e.pgerror)
        print (e.diag.message_detail)
        sys.exit(1)

    table_col_names = [tcn[0] for tcn in cursor.description]
    rows = cursor.fetchall()

    pretty_table_row = PrettyTable()
    pretty_table_row.field_names = table_col_names

    for row in rows:
        pretty_table_row.add_row(row)

    #print format
    pretty_table_row.align[table_col_names[0]] = "r"
    pretty_table_row.align[table_col_names[1]] = "l"
    pretty_table_row.align[table_col_names[2]] = "r"
    pretty_table_row.align[table_col_names[3]] = "l"
    pretty_table_row.align[table_col_names[4]] = "r"

    print (pretty_table_row)


def pg_ddl(conn):
    pass

def pg_copy_fromfile(conn, filename, tablename):
    try:
        cur = conn.cursor()
        fp = open(filename, 'r')
        cur.copy_from(fp, tablename, sep='|')
        conn.commit()
    except psycopg2.DatabaseError as e:
        print ("Execute failed!!!")
        print (e.pgerror)
        print (e.diag.message_detail)
        if conn:
            conn.rollback()
    except IOError as e:
        errno, strerror = e.args
        print ("I/O error(%s):%s" %(errno,strerror))
    except:
        print ("Unexpected error:",sys.exc_info()[0])
        raise
    finally:
        if fp:
            fp.close()

def pg_copy_tofile(conn, filename, tablename):
    try:
        cur = conn.cursor()
        fp = open(filename, 'w')
        cur.copy_to(fp, tablename, sep='|')
        conn.commit()
    except psycopg2.DatabaseError as e:
        print ("Execute failed!!!")
        print (e.pgerror)
        print (e.diag.message_detail)
        if conn:
            conn.rollback()
    except IOError as e:
        errno, strerror = e.args
        print ("I/O error(%s):%s" %(errno,strerror))
    except:
        print ("Unexpected error:",sys.exc_info()[0])
        raise
    finally:
        if fp:
            fp.close()

def pg_execute(conn, sql_stmt, idict):
    cursor = conn.cursor()
    try:
        #cursor.executemany("INSERT INTO testem VALUES (%s, %s);", [(i, i) for i in range(10)])
        cursor.execute("TRUNCATE TABLE company;")
        cursor.executemany(sql_stmt, idict)
    except psycopg2.DatabaseError as e:
        print ("Execute failed!!!")
        print (e.pgerror)
        print (e.diag.message_detail)

        if conn:
            conn.rollback()

    conn.commit()

def pg_close(conn):
    if conn:
        conn.close()

def main():
    conn_string = "host='localhost' dbname='daysbaydb' user='hshl' password='hshl123'"
    conn = pg_conn(conn_string)

    query_stmt = "SELECT id, name, age, address, salary FROM company ORDER BY id LIMIT 10;" 
    #pg_execute(conn, query_stmt)

    idict = ((1, 'Paul' , 32, 'California', 20000.00),
             (2, 'Allen', 25, 'Texas',      15000.00),
             (3, 'Teddy', 23, 'Norway',     20000.00))

    sql_stmt = "INSERT INTO company(id, name, age, address, salary) VALUES(%s, %s, %s, %s, %s)"
    pg_execute(conn, sql_stmt, idict)

    srcfilename = "companylist"
    destfilename = "copytofile.rlt"
    tablename = "company"
    #pg_copy_fromfile(conn, srcfilename, tablename)
    #pg_copy_tofile(conn, destfilename, tablename)
    
    pg_metadata(conn, query_stmt)

    pg_close(conn)

if __name__ == "__main__":
    main()
