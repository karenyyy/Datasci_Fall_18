#!/usr/bin/env python
# coding: utf-8

#  DS 220 Final Project: Exploratory Analysis of the Crime Reporting Pattern in Oakland using MySQL and Jupyter Notebook
#  Team: Jiarong Ye, Yichi Qian, Han Shao

#  Contents
# --------------------
# 1. [Pipeline to insert dataset into MySQL Database](#1)
# 2. [Exploratory analysis](#2)
#
#     2.1 [What crime has the highest occurrence all across Oakland?]
#     2.2 [What crime has the highest occurrence in each location?]
#         3.2.1 [What crime has the highest occurrence in International Blvd?]
#     2.3 [What is the incident solving time for each incident?]


# ### Import Packages

import pandas as pd
import re
import os
import numpy as np
import pymysql
from datetime import datetime
import matplotlib.pyplot as plt

PATH = os.getcwd()
PATH += '/oakland-crime-statistics-2011-to-2016'
FILE_2011 = PATH + '/records-for-2011.csv'
FILE_2012 = PATH + '/records-for-2012.csv'
FILE_2013 = PATH + '/records-for-2013.csv'
FILE_2014 = PATH + '/records-for-2014.csv'
FILE_2015 = PATH + '/records-for-2015.csv'
FILE_2016 = PATH + '/records-for-2016.csv'


# ### Data Preparing

# #### clean address for data in 2012 and 2014

def convert_location_col(df, filename):
    reg_pattern = '\"address\":\"([A-Za-z0-9\s./#\(\),-]+)\"'
    address_lst = list(map(lambda x: re.findall(pattern=reg_pattern, string=df['Location 1'][x].replace('&amp;', ' ')),
                           range(len(df))))
    address_lst_flattened = []
    for i in range(len(address_lst)):
        try:
            address_lst_flattened.append(address_lst[i][0])
        except Exception as e:
            address_lst_flattened.append(np.nan)
    df['Location'] = address_lst_flattened
    df = df.drop(columns=['Location 1'])
    df = pd.concat([df.iloc[:, :2], df.Location, df.iloc[:, 2:-1]], axis=1)
    df.to_csv(filename, index=None)
    return df


# #### convert time format to be MySQL compatible

def convert_time_sql_format():
    columns = ['Create Time', 'Closed Time']
    for y in range(1, 7):
        filename = PATH + '/records-for-201{}.csv'.format(y)
        df = pd.read_csv(filename)
        for column in columns:
            tmp = []
            df = df.iloc[df[column].dropna().index, :].reset_index(drop=True)
            for i in df[column]:
                ymy = i.split('T')[0]
                hms = i.split('T')[1]
                splited_lst = ymy.split('-')
                year = splited_lst[0]
                month = splited_lst[1][1:] if splited_lst[1].startswith('0') else splited_lst[1]
                day = splited_lst[2][1:] if splited_lst[2].startswith('0') else splited_lst[2]

                splited_lst = hms.split(':')
                hour = splited_lst[0][1:] if splited_lst[0].startswith('0') else splited_lst[0]
                minute = splited_lst[1][1:] if splited_lst[1].startswith('0') else splited_lst[1]
                second = splited_lst[2][1:] if splited_lst[2].startswith('0') else splited_lst[2]

                tmp.append(datetime(int(year), int(month), int(day), int(hour), int(minute), int(second)))

            df[column] = pd.DataFrame(tmp)
        df['Days to Resolve'] = pd.DataFrame(list(map(lambda x: x.days, df[columns[1]] - df[columns[0]])))
        df['Area Id'] = df['Area Id'].fillna(value=0)
        df['Priority'] = df['Priority'].dropna(axis=0)
        df['Incident Type Id'] = df['Incident Type Id'].dropna(axis=0)
        df['Event Number'] = df['Event Number'].dropna(axis=0)
        df.to_csv(filename, index=None)


# ### Load data into MySQL

class DataSqlLoader:
    def __init__(self, database):
        # connect to mysql local server
        self.database = database
        self.db = pymysql.Connect(
            host='localhost',
            user='root',
            passwd='',
            db=self.database)
        self.c = self.db.cursor()

    def creat_tables(self):
        for year in range(1, 7):
            try:
                self.c.execute('''
                        CREATE TABLE IF NOT EXISTS crimedata_201{}
                            (
                              `Agency`                   VARCHAR(5)   NULL,
                              `Create Time`              DATETIME     NULL,
                              Location                   VARCHAR(100) NULL,
                              `Area Id`                  VARCHAR(5)   NULL,
                              Beat                       VARCHAR(10)  NULL,
                              Priority                   Double       NULL,
                              `Incident Type Id`         VARCHAR(10)  NULL,
                              `Incident Type Description` TEXT         NULL,
                              `Event Number`             VARCHAR(30)  NOT NULL
                                PRIMARY KEY,
                              `Closed Time`              DATETIME     NULL,
                              `Days to Resolve`          INT          NULL,
                              CONSTRAINT crimedata_2011_EventNumber_uindex
                              UNIQUE (`Event Number`)
                            );
                        '''.format(year))
            except Exception as e:
                print(e)

    def insert_into_tables(self, filename, tablename):
        """might fail, please do it manually if you can (-_-)"""
        query = repr("LOAD DATA INFILE '{}' INTO TABLE {} fields terminated by ',' lines terminated by '\r\n' ignore "
                     "1 lines".format(filename, tablename))
        query = query.replace('"', '')
        try:
            print(query)
            self.c.execute(query)
        except Exception as e:
            print(e)

    def drop_table(self, tablename):
        try:
            self.c.execute("drop table {}".format(tablename))
        except Exception as e:
            print(e)

    def get_sample(self, table, limit=None):
        if limit == None:
            query = 'SELECT * FROM {};'.format(table)
        else:
            query = 'SELECT * FROM {} limit {};'.format(table, limit)
            pd.read_sql(sql=query, con=self.db)
        return pd.read_sql(sql=query, con=self.db)

    def sql_query(self, query):
        try:
            return pd.read_sql(sql=query, con=self.db)
        except Exception as e:
            print(e)

    def close(self):
        self.db.close()


# ## Exploratory analysis

# #### What crime has the highest occurrence all across Oakland?

def most_frequent_crime(dsl):
    query = '''
    select t1.tag, t1.cnt, t2.cnt, t3.cnt, t4.cnt, t5.cnt, t6.cnt
        from
            (select `Incident Type Desciption` as tag, count(*) as cnt
             from crimedata_2011
                group by `Incident Type Desciption`
                order by cnt desc
                limit 10) as t1
            inner join
                      (select `Incident Type Desciption` as tag, count(*) as cnt
                       from crimedata_2012
                       group by `Incident Type Desciption`
                       order by cnt desc
                       limit 10) as t2
            inner join (select `Incident Type Desciption` as tag, count(*) as cnt
                        from crimedata_2013
                        group by `Incident Type Desciption`
                        order by cnt desc
                        limit 10) as t3
            inner join (select `Incident Type Desciption` as tag, count(*) as cnt
                        from crimedata_2014
                        group by `Incident Type Desciption`
                        order by cnt desc
                        limit 10) as t4
            inner join (select `Incident Type Desciption` as tag, count(*) as cnt
                        from crimedata_2015
                        group by `Incident Type Desciption`
                        order by cnt desc
                        limit 10) as t5
            inner join (select `Incident Type Desciption` as tag, count(*) as cnt
                        from crimedata_2016
                        group by `Incident Type Desciption`
                        order by cnt desc
                        limit 10) as t6
            on t1.tag=t2.tag
            and t2.tag=t3.tag
            and t3.tag=t4.tag
            and t4.tag=t5.tag
            and t5.tag=t6.tag;
    '''
    highest_freq_crime_all_6_years = dsl.sql_query(query=query)
    highest_freq_crime_all_6_years = highest_freq_crime_all_6_years.set_index('tag').transpose()
    highest_freq_crime_all_6_years.plot(legend=True, figsize=(15, 15), marker='.', lw=3, mew=15,
                                        title='The most frequent crime from 2011 to 2016')
    plt.show()


# #### What crime has the highest occurrence in each location?

def most_frequent_crime_each_loc(dsl):
    plt.figure(figsize=(17, 18))
    for year in range(1, 7):
        location_cnt = dsl.sql_query("""select Location,
                                           `Incident Type Desciption`,
                                           count(*) cnt
                                    from crimedata_2011
                                        group by Location
                                        order by cnt desc
                                      limit 10;
                                    """.format(year))
        print('The top 3 location with highest crime rate in year 201{}:'.format(year))
        print(location_cnt.iloc[:3, :].values)
        print('\n')

        plt.subplot(2, 3, year)
        plt.bar(x=location_cnt.Location, height=location_cnt.cnt)
        plt.xticks(rotation=90)
        plt.ylabel('Crime Occurence Number Count')
        plt.title('201{}'.format(year))
        plt.tight_layout()
    plt.show()

    ## trend in 6 years
    query = '''
    select t1.Location, 
            t1.cnt as count_2011, 
            t2.cnt as count_2012, 
            t3.cnt as count_2013, 
            t4.cnt as count_2014, 
            t5.cnt as count_2015, 
            t6.cnt as count_2016
    from
        (select Location,
                 count(*) cnt
          from crimedata_2011
          group by Location
          order by cnt desc limit 10) as t1
        inner join
                  (select Location,
                           count(*) cnt
                    from crimedata_2012
                    group by Location
                    order by cnt desc limit 10) as t2
        inner join (select Location,
                           count(*) cnt
                    from crimedata_2013
                    group by Location
                    order by cnt desc limit 10) as t3
        inner join (select Location,
                           count(*) cnt
                    from crimedata_2014
                    group by Location
                    order by cnt desc limit 10) as t4
        inner join (select Location,
                           count(*) cnt
                    from crimedata_2015
                    group by Location
                    order by cnt desc limit 10) as t5
        inner join (select Location,
                           count(*) cnt
                    from crimedata_2016
                    group by Location
                    order by cnt desc limit 10) as t6
        on t1.Location=t2.Location
        and t2.Location=t3.Location
        and t3.Location=t4.Location
        and t4.Location=t5.Location
        and t5.Location=t6.Location;
'''
    highest_freq_crime_location_all_6_years = dsl.sql_query(query=query)
    highest_freq_crime_location_all_6_years = highest_freq_crime_location_all_6_years.set_index('Location').transpose()
    highest_freq_crime_location_all_6_years.plot(legend=True, figsize=(15, 15), marker='.', lw=3, mew=15,
                                                 title='The location with highest crime rate from 2011 to 2016')
    plt.show()


# #### What crime has the highest occurrence in __International Blvd__?

def most_frequent_crime_international_blvd(dsl):
    query = '''
    select t1.tag, t1.cnt, t2.cnt, t3.cnt, t4.cnt, t5.cnt, t6.cnt
    from
        (select `Incident Type Desciption` as tag, count(*) as cnt
         from crimedata_2011
            where Location='INTERNATIONAL BLVD'
            group by `Incident Type Desciption`
            order by cnt desc
            limit 10) as t1
        inner join
                  (select `Incident Type Desciption` as tag, count(*) as cnt
                   from crimedata_2012
                   where Location='INTERNATIONAL BLVD'
                   group by `Incident Type Desciption`
                   order by cnt desc
                   limit 10) as t2
        inner join (select `Incident Type Desciption` as tag, count(*) as cnt
                    from crimedata_2013
                    where Location='INTERNATIONAL BLVD'
                    group by `Incident Type Desciption`
                    order by cnt desc
                    limit 10) as t3
        inner join (select `Incident Type Desciption` as tag, count(*) as cnt
                    from crimedata_2014
                    where Location='INTERNATIONAL BLVD'
                    group by `Incident Type Desciption`
                    order by cnt desc
                    limit 10) as t4
        inner join (select `Incident Type Desciption` as tag, count(*) as cnt
                    from crimedata_2015
                    where Location='INTERNATIONAL BLVD'
                    group by `Incident Type Desciption`
                    order by cnt desc
                    limit 10) as t5
        inner join (select `Incident Type Desciption` as tag, count(*) as cnt
                    from crimedata_2016
                    where Location='INTERNATIONAL BLVD'
                    group by `Incident Type Desciption`
                    order by cnt desc
                    limit 10) as t6
        on t1.tag=t2.tag
        and t2.tag=t3.tag
        and t3.tag=t4.tag
        and t4.tag=t5.tag
        and t5.tag=t6.tag;
'''
    highest_freq_crime_internationalblvd_all_6_years = dsl.sql_query(query=query)
    highest_freq_crime_internationalblvd_all_6_years = pd.concat([highest_freq_crime_internationalblvd_all_6_years.tag,
                                                                  highest_freq_crime_internationalblvd_all_6_years.sum(
                                                                      axis=1)], axis=1)
    highest_freq_crime_internationalblvd_all_6_years.columns = ['crime type', 'occurrence']

    # high frequency crime type in the location with the highest crime rate
    plt.figure(figsize=(10, 10))
    plt.pie(highest_freq_crime_internationalblvd_all_6_years.occurrence,
            labels=highest_freq_crime_internationalblvd_all_6_years['crime type'],
            autopct='%.2f',
            shadow=True)
    plt.title('The most frequent crime type occurred in INTERNATIONAL BLVD from 2011-2016')
    plt.tight_layout()
    plt.show()


# #### What is the incident solving time for each incident?
def crime_solving_time(dsl):
    plt.figure(figsize=(15, 15))
    for year in range(1, 7):
        query = '''
            SELECT `Incident Type Id`,
                   `Incident Type Desciption`,
                   concat(`Incident Type Id`, ' : ', `Incident Type Desciption`) as tag,
                    avg(`Days to Resolve`) as avg_day_to_resolve
            FROM crimedata_201{}
                GROUP BY `Incident Type Id`
                order by avg_day_to_resolve desc
              limit 20;
        '''.format(year)
        df_tmp = dsl.sql_query(query)
        print('The top 3 crime that took the longest time to resolve in year 201{}:'.format(year))
        print(df_tmp.iloc[:3, :].values)
        print('\n')
        plt.subplot(2, 3, year)
        plt.bar(x=df_tmp['tag'].astype('str').values, height=df_tmp['avg_day_to_resolve'].values)
        plt.xticks(rotation=90)
        # plt.xlabel(xlabel='Incident Type Id')
        plt.ylabel('avg_day_to_resolve')
        plt.title('201{}'.format(year))
        plt.tight_layout()
    plt.show()

    ## trend in 6 years
    query = '''
    select t1.`Incident Type Desciption`, 
       t1.avg_day_to_resolve, 
       t2.avg_day_to_resolve, 
       t3.avg_day_to_resolve, 
       t4.avg_day_to_resolve, 
       t5.avg_day_to_resolve, 
       t6.avg_day_to_resolve from
        (SELECT `Incident Type Id`,
                `Incident Type Desciption`,
                 avg(`Days to Resolve`) as avg_day_to_resolve
          FROM crimedata_2011
            GROUP BY `Incident Type Id`
            order by avg_day_to_resolve desc
            limit 50) as t1
        inner join
                  (SELECT `Incident Type Id`,
                          `Incident Type Desciption`,
                          avg(`Days to Resolve`) as avg_day_to_resolve
                   FROM crimedata_2012
                   GROUP BY `Incident Type Id`
                   order by avg_day_to_resolve desc
                   limit 50) as t2
        inner join (SELECT `Incident Type Id`,
                           `Incident Type Desciption`,
                           avg(`Days to Resolve`) as avg_day_to_resolve
                    FROM crimedata_2013
                    GROUP BY `Incident Type Id`
                    order by avg_day_to_resolve desc
                    limit 50) as t3
        inner join (SELECT `Incident Type Id`,
                           `Incident Type Desciption`,
                           avg(`Days to Resolve`) as avg_day_to_resolve
                    FROM crimedata_2014
                    GROUP BY `Incident Type Id`
                    order by avg_day_to_resolve desc
                    limit 50) as t4
        inner join (SELECT `Incident Type Id`,
                           `Incident Type Desciption`,
                           avg(`Days to Resolve`) as avg_day_to_resolve
                    FROM crimedata_2015
                    GROUP BY `Incident Type Id`
                    order by avg_day_to_resolve desc
                    limit 50) as t5
        inner join (SELECT `Incident Type Id`,
                           `Incident Type Desciption`,
                           avg(`Days to Resolve`) as avg_day_to_resolve
                    FROM crimedata_2016
                    GROUP BY `Incident Type Id`
                    order by avg_day_to_resolve desc
                    limit 50) as t6
        on t1.`Incident Type Id`=t2.`Incident Type Id`
        and t2.`Incident Type Id`=t3.`Incident Type Id`
        and t3.`Incident Type Id`=t4.`Incident Type Id`
        and t4.`Incident Type Id`=t5.`Incident Type Id`
        and t5.`Incident Type Id`=t6.`Incident Type Id`;
'''

    avg_day_resolve_df = dsl.sql_query(query=query)

    avg_day_resolve_df_top_5 = avg_day_resolve_df.iloc[:5, :]
    avg_day_resolve_df_top_5 = avg_day_resolve_df_top_5.set_index('Incident Type Desciption').transpose()
    avg_day_resolve_df_top_5.plot(legend=True, figsize=(15, 15), marker='.', lw=3, mew=15,
                                  title='The tendency of crime resolving time from 2011 to 2016')
    plt.show()


if __name__ == '__main__':

    '''1. Pipeline to insert dataset into MySQL Database'''

    '''1.1 clean address for data in 2012 and 2014'''
    convert_location_col(pd.read_csv(FILE_2012), FILE_2012)
    convert_location_col(pd.read_csv(FILE_2014), FILE_2014)
    print('Address extracted!')

    '''1.2 convert time format to be MySQL compatible '''
    convert_time_sql_format()
    print('Time format converted!')

    '''1.3 load data into MySQL'''
    dsl = DataSqlLoader('ds220')
    dsl.creat_tables()
    dsl.insert_into_tables(FILE_2011, 'crimedata_2011')
    dsl.insert_into_tables(FILE_2012, 'crimedata_2012')
    dsl.insert_into_tables(FILE_2013, 'crimedata_2013')
    dsl.insert_into_tables(FILE_2014, 'crimedata_2014')
    dsl.insert_into_tables(FILE_2015, 'crimedata_2015')
    dsl.insert_into_tables(FILE_2016, 'crimedata_2016')
    print('Data loaded!')

    '''2. Exploratory analysis'''

    '''2.1 What crime has the highest occurrence all across Oakland?'''
    most_frequent_crime(dsl)
    print('2.1 done!')

    '''2.2 What crime has the highest occurrence in each location?'''
    most_frequent_crime_each_loc(dsl)
    print('2.2 done!')

    '''2.2.1 What crime has the highest occurrence in __International Blvd__?'''
    most_frequent_crime_international_blvd(dsl)
    print('2.2.1 done!')

    '''2.3 What is the incident solving time for each incident?'''
    crime_solving_time(dsl)
    print('2.3 done!')