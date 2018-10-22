#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from datetime import datetime
import pymysql

# Load the data

department = pd.read_csv('departments.csv', sep=',')
department.columns = ['department_name']
shift = pd.read_csv('shifts.csv', sep=',')
shift.columns = ['from_time', 'length']
employees = pd.read_csv('employees.csv', sep=',')
employees.emptype = employees.emptype.fillna('')
schedule = pd.read_csv('schedule.csv', sep=',')
schedule.columns = ['date', 'empid', 'dept', 'start_time', 'shift_length']


# Manipulate the data

class DataSqlLoader:
    def __init__(self, database):
        # connect to mysql local server
        self.db = pymysql.Connect('localhost',
                                  'root',
                                  '',
                                  database)
        self.c = self.db.cursor()

    # convert the shift and schedule time to `time` format compatible in MySQL
    def convert_time_format(self, time):
        return datetime.strptime('{}'.format(time), '%I%p').strftime('%H:%M:%S')

    # convert schedule date to `date` format compatible in MySQL
    def convert_date_format(self, time):
        return datetime.strptime('{}'.format(time), '%m/%d/%Y').strftime('%Y-%m-%d')

    def creat_tables(self):
        self.c.execute('''
                create table if not exists department
                (
                  department_id  int auto_increment
                    primary key,
                  department_name varchar(50) not null
                );
                ''')
        self.c.execute('''
            create table if not exists shift
            (
              shift_id int auto_increment
                primary key,
              from_time   time not null,
              length   int  not null
            );
            ''')
        self.c.execute('''
            create table if not exists schedule
            (
              schedule_id  int auto_increment
                primary key,
              date         date        not null,
              empid        varchar(10) not null,
              dept         varchar(50) not null,
              start_time   time        not null,
              shift_length int         not null
            );
            ''')
        self.c.execute('''
            create table if not exists employees
            (
              empid     varchar(10) not null primary key,
              lastname  varchar(20) not null,
              firstname varchar(20) not null,
              emptype   varchar(3)  null,
              cellphone varchar(20) null,
              homephone varchar(20) null,
              ftpt      varchar(2)  not null,
              constraint employee_empid_uindex
              unique (empid)
            );
        ''')

    def insert_into_tables(self, table, table_name):
        for i in range(len(table)):
            attributes = '{}'.format(tuple(table.columns.tolist())).replace("'", "")
            query = "insert into {} {} values {};".format(
                table_name, attributes, tuple(table.iloc[i, :].values))
            query = query.replace("(none)", "")
            query = query.replace(r",)", ")")
            # print(query)
            try:
                self.c.execute(query)
                self.db.commit()
            except Exception as e:
                print(e)

    def close(self):
        self.db.close()


dsl = DataSqlLoader('cs431_project')
dsl.creat_tables()

# # convert time format
# schedule['start_time'] = list(map(lambda x: dsl.convert_time_format(x),
#                                   schedule['start_time']))
# shift['from_time'] = list(map(lambda x: dsl.convert_time_format(x),
#                               shift['from_time']))
# schedule['date'] = list(map(lambda x: dsl.convert_date_format(x),
#                             schedule['date']))
#
# # insert into tables
# dsl.insert_into_tables(department, 'department')
# dsl.insert_into_tables(shift, 'shift')
# dsl.insert_into_tables(schedule, 'schedule')
# dsl.insert_into_tables(employees, 'employees')
#
#
# SQL Query
query = '''
    select e.lastname as LAST, e.firstname as FIRST, e.cellphone as CELL,
       s.date as DATE, d.department_name as DEPT, 
       date_format(s.start_time, "%I%p") as START, s.shift_length as SHIFT_LENGTH
from department as d, employees as e, schedule as s
where s.dept=d.department_name
and s.empid=e.empid
order by LAST, FIRST, DATE, START, SHIFT_LENGTH, DEPT asc limit 50;
'''

df = pd.read_sql(query, dsl.db)
print(df)
# print(df.to_latex())
