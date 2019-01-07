###################################################################
########################## Create Database ########################
###################################################################
DROP DATABASE IF EXISTS nurse;
CREATE DATABASE nurse;
USE nurse;

###################################################################
############################## Drop Tables ########################
###################################################################

DROP TABLE IF EXISTS day_off;
DROP TABLE IF EXISTS employee;
DROP TABLE IF EXISTS need;
DROP TABLE IF EXISTS schedule;
DROP TABLE IF EXISTS employee_available_shift_count;


###################################################################
########################### Employee Table ########################
###################################################################

CREATE TABLE IF NOT EXISTS employee(
    firstName VARCHAR(20),
    lastName VARCHAR(20),
    wage VARCHAR(15),
    emptype VARCHAR(20),
    cellphone VARCHAR(20),
    homephone VARCHAR(20),
    ftpt VARCHAR(10),
    preferred_shift VARCHAR(20),
    dept_cert VARCHAR(100)
);



LOAD DATA INFILE '/opt/lampp/htdocs/cs431/final_project/dataset/431_FINAL_DATA_SET/employee_final.csv'
INTO TABLE employee fields terminated by ',' lines terminated by '\r\n';
ALTER TABLE employee ADD COLUMN pre_shift_start INT;
ALTER TABLE employee ADD COLUMN empid SERIAL PRIMARY KEY;


UPDATE employee SET wage = REPLACE(wage, '$', '');
UPDATE employee SET dept_cert = REPLACE(dept_cert, ' ', '');
UPDATE employee SET firstName = REPLACE(firstName, '"', '');
UPDATE employee SET lastName = REPLACE(lastName, '"', '');
UPDATE employee SET wage = REPLACE(wage, '"', '');
UPDATE employee SET emptype = REPLACE(emptype, '"', '');
UPDATE employee SET cellphone = REPLACE(cellphone, '"', '');
UPDATE employee SET homephone = REPLACE(homephone, '"', '');
UPDATE employee SET ftpt = REPLACE(ftpt, '"', '');
UPDATE employee SET preferred_shift = REPLACE(preferred_shift, '"', '');
UPDATE employee SET dept_cert = REPLACE(dept_cert, '"', '');



###################################################################
#################### Department Need Table ########################
###################################################################

CREATE TABLE IF NOT EXISTS need(
    dept VARCHAR(20),
    datechar VARCHAR(20),
    shiftchar VARCHAR(20),
    emptype VARCHAR(10),
    emp_need INT
);

LOAD DATA INFILE '/opt/lampp/htdocs/cs431/final_project/dataset/431_FINAL_DATA_SET/needs_final.csv'
INTO TABLE need
fields terminated by ',' lines terminated by '\r\n';
ALTER TABLE need ADD COLUMN needid SERIAL PRIMARY KEY;
ALTER TABLE need ADD COLUMN date date;
ALTER TABLE need ADD COLUMN start_time VARCHAR(20);

###################################################################
########################### DayOff Table ##########################
###################################################################

CREATE TABLE IF NOT EXISTS day_off(
    firstName VARCHAR(20),
    lastName VARCHAR(20),
    datechar VARCHAR(20)
);

LOAD DATA INFILE '/opt/lampp/htdocs/cs431/final_project/dataset/431_FINAL_DATA_SET/daysoffrequests_final.csv'
INTO TABLE day_off
fields terminated by ',' lines terminated by '\r\n';
ALTER TABLE day_off ADD COLUMN empid INT;
ALTER TABLE day_off ADD COLUMN offid SERIAL PRIMARY KEY;
ALTER TABLE day_off ADD COLUMN date date;
UPDATE day_off SET firstName = REPLACE(firstName, ' ', '');


###################################################################
########################### Schedule Table ########################
###################################################################


CREATE TABLE IF NOT EXISTS schedule(
    date DATE,
    empid INT,
    dept VARCHAR(20),
    start_time VARCHAR(10));

ALTER TABLE schedule ADD COLUMN schid SERIAL PRIMARY KEY;



