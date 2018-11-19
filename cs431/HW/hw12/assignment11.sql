# 2. Load this datainto your 3NFtablesstructure.
CREATE TABLE department_need
(
  department_name  VARCHAR(10) NOT NULL,
  date             TEXT        NULL,
  period           VARCHAR(10) NULL,
  emptype          VARCHAR(10) NULL,
  number_of_employees  INT         NULL
);

CREATE TABLE employees
(
  firstname VARCHAR(20) NULL,
  lastname  VARCHAR(20) NULL,
  wage      VARCHAR(10) NULL,
  emptype   VARCHAR(10) NULL,
  phone1    VARCHAR(20) NULL,
  phone2    VARCHAR(20) NULL,
  ftpt      VARCHAR(10)  NULL
);


CREATE TABLE daysoff
(
  firstname VARCHAR(20) NOT NULL,
  lastname  VARCHAR(20) NOT NULL,
  date  TEXT NULL
);



LOAD DATA INFILE '/home/karen/workspace/Datasci_Fall_18/cs431/HW/hw11/project_asgn_11_data/needs.csv' INTO TABLE department_need
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n';


LOAD DATA INFILE '/home/karen/workspace/Datasci_Fall_18/cs431/HW/hw11/project_asgn_11_data/employee2.csv' INTO TABLE employees
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n';


LOAD DATA INFILE '/home/karen/workspace/Datasci_Fall_18/cs431/HW/hw11/project_asgn_11_data/daysoffrequests.csv' INTO TABLE daysoff
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n';


UPDATE daysoff SET firstname = REPLACE(firstname, ' ', '');
UPDATE employees SET firstname = REPLACE(firstname, '"', '');
UPDATE employees SET lastname = REPLACE(lastname, '"', '');
UPDATE employees SET wage = REPLACE(wage, '"', '');
UPDATE employees SET wage = REPLACE(wage, '$', '');
UPDATE employees SET emptype = REPLACE(emptype, '"', '');
UPDATE employees SET phone1 = REPLACE(phone1, '"', '');
UPDATE employees SET phone2 = REPLACE(phone2, '"', '');
UPDATE employees SET ftpt = REPLACE(ftpt, '"', '');


ALTER TABLE employees ADD empid INT NOT NULL AUTO_INCREMENT PRIMARY KEY;

CREATE TABLE daysoff_tmp
(
  empid INT  NOT NULL,
  date  TEXT NULL
) SELECT e.empid, d.date
  FROM employees as e, daysoff as d
  WHERE (d.firstname, d.lastname) = (e.firstname, e.lastname);

DROP TABLE daysoff;
RENAME TABLE daysoff_tmp TO daysoff;

SHOW TABLES;
DESCRIBE department_need;
DESCRIBE employees;
DESCRIBE daysoff;



# 3. Calculate the total needs of all departments, all days, all shifts by employee type. For example: RNs: 3214 hours, LPNs: 2735 hours, etc.

SELECT emptype, cast(SUM(shifthrs) AS INT) AS total_working_hrs
FROM
  (SELECT emptype,
    8*number_of_employees AS shifthrs
   FROM department_need) as tmp
GROUP BY emptype;


# 4. Calculate the total available hours per employee type. For example: RNs: 3000 hours, LPNs: 2800 hours.
# Note that a part-time person is limited to 24 hours per week. Also note that requested time off is not figured into this calculation.

SELECT emptype, cast(sum(each_hrs) AS INT) as total_available_hrs
FROM (SELECT empid, emptype, ftpt, if(ftpt='FT', available_days*8, available_days*(24/7)) as each_hrs
       FROM (SELECT e.empid, e.emptype, e.ftpt,
             if(isnull(agg_daysoff.dayoff), 0, agg_daysoff.dayoff) as requested_day_off,
             if(isnull(agg_daysoff.dayoff), 14, 14 - agg_daysoff.dayoff) as available_days
             FROM employees as e
             LEFT JOIN (SELECT empid, count(*) as dayoff
                        FROM daysoff
                        GROUP BY empid) as agg_daysoff
             ON e.empid=agg_daysoff.empid) as tmp1) as tmp2
GROUP BY emptype;



# 5. List (via PHP/SQL code) which employee types are short-staffed (you don’t have enough possible hours to fill the needs for that employee type).

SELECT table1.emptype,
       table1.total_working_hrs,
       table2.total_available_hrs,
       if(table2.total_available_hrs<table1.total_working_hrs, 'YES', 'NO') as short_staffed
FROM (SELECT emptype, cast(SUM(shifthrs) AS INT) AS total_working_hrs
      FROM
        (SELECT emptype,
           8*number_of_employees AS shifthrs
         FROM department_need) as tmp
      GROUP BY emptype) as table1
INNER JOIN
  (SELECT emptype, cast(sum(each_hrs) AS INT) as total_available_hrs
   FROM (SELECT empid, emptype, ftpt, if(ftpt='FT', available_days*8, available_days*(24/7)) as each_hrs
         FROM (SELECT e.empid, e.emptype, e.ftpt,
                 if(isnull(agg_daysoff.dayoff), 0, agg_daysoff.dayoff) as requested_day_off,
                 if(isnull(agg_daysoff.dayoff), 14, 14 - agg_daysoff.dayoff) as available_days
               FROM employees as e
                 LEFT JOIN (SELECT empid, count(*) as dayoff
                            FROM daysoff
                            GROUP BY empid) as agg_daysoff
                   ON e.empid=agg_daysoff.empid) as tmp1) as tmp2
   GROUP BY emptype) as table2
ON table1.emptype=table2.emptype;


# 6. Calculate the average cost per hour for each employee type, then use that number to estimate the total cost
# for each employee type for the entire schedule.

SELECT table1.emptype,
       table2.total_working_hrs,
       concat('$', table1.avg_wage) as avg_wage,
       concat('$', table2.total_working_hrs*table1.avg_wage) as total_cost
FROM (SELECT emptype, round(avg(wage), 3) as avg_wage
      FROM employees
      GROUP BY emptype) as table1
INNER JOIN
  (SELECT emptype, cast(SUM(shifthrs) AS INT) AS total_working_hrs
            FROM
              (SELECT emptype,
                 8*number_of_employees AS shifthrs
               FROM department_need) as tmp
            GROUP BY emptype) as table2
ON table1.emptype = table2.emptype;


# 7. For all full time employees, calculate the total cost of giving them the day off. This assumes that they
# get paid time off, and that they will be paid for one, 8-hour shift.

SELECT table1.empid, table1.firstname, table1.lastname,
       table1.wage as wage_per_hour,
       table2.dayoff as number_of_daysoff,
       round(table2.dayoff*table1.wage*8,3) as cost_of_paid_dayoff
FROM
  (SELECT empid, firstname, lastname, wage
   FROM employees
   WHERE ftpt='FT') as table1
INNER JOIN
  (SELECT empid, count(*) as dayoff
   FROM daysoff
   GROUP BY empid) as table2
ON table1.empid=table2.empid;






