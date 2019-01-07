README
This project is completed by:
	Jiarong Ye 			jxy225
	Ziheng Liu			zxl381

Statement:
	All of the work submitted here was done by us. We understand that if we submit work from other sources that we are subjecting ourselves to academic integrity charges.

What to be executed:
	1. Edit config/config.php: please input your username and password at line 5&6.
	2. Edit sql/Please_run_these_MYSQL_codes_first.sql: please change the paths of LOAD DATA INFILE statements, at line 37&69&86.
	3. Execute sql/Please_run_these_MYSQL_codes_first.sql: you can copy all the queries in this file, and paste and execute them somewhere. You can also execute the whole file. This step will drop “nurse” database if it exists.
	4. Execute main.php: please execute it on a browser( we don't know how to use terminal). This step will show: (1) Total schedule cost; (2) Happiness report; (3) Unused shifts and utilization for FT report; (4) Unused shifts and utilization for PT report; (5) Unfilled need report; (6) Employee report, including three types of shift counts, cost, happiness and utilization; (7) Average happiness; (8) Average Full-Time employee utilization; (9) Average Part-Time employee utilization; (9) Total execution time.

Total schedule cost: $290778.64

Average employee happiness: 37.05%

Number of unused shifts: 91 full time and 45 part time

Total number of unfilled needs: 253

Utilization: 91.52% Full Time, 81.22% Part Time

Our ways of optimization: 
	We found that these optimizations are not likely to be perfectly fulfilled at the same time. So we firstly consider full-time employees, and then try to consider happiness, and finally the cost. When we want to choose an employee to fulfill a need, we will try to choose someone whose preferred shift is the same shift in the need. After preferred shift is considered, we will try to choose an employee with the lowest wage.
	To implement this optimization, when we SELECT employees that can be filled, we use “ORDER BY ftpt, if(abs(pre_shift_start-23)=0, pre_shift_start-23, 1), wage”.
	Besides, in order to fulfill more needs, we try to schedule for the needs that want more employees, because scheduling is easier for needs that want less employees. After this, we also “order by needid desc”, in case your mysql version is different and would generate different results.

