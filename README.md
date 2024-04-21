# DanceHub_Web_Application
-----
**välipalautus 3 status**
* user or admin can create an account
* admin user can create new schools
* all users can create reviews
* all visitors can see the schools and reviews
  
* **missing :**
  * **grouping of schools by style**
  * **search function**
  * **page for all the schedules, sorted by city**
  * **add and remove function of schools and reviews**
-----
**how to install:**
1) clone the repository
    
```bash
git clone
```
2) create env file in the folder

```bash
touch .env
```
3) write these lines in the file:
```bash
DATABASE_URL=postgresql:///(your_database_address)

SECRET_KEY=(create own)
```
4) activate virtual environment and install the dependencies in the requirements file

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
5) Define the SQL schema:
```bash
psql < schema.sql
```
6) run the application within a Flask environment
```bash
flask run
```


-----
**final version will include:**

A platform to search for dance classes, read reviews and discover social dance events. 

The application displays dance schools in a specific area, where users can search for dance classes based on a specific dance style (e.g. salsa, tango or rock). In the application it's possible to check the schedules for these events and read their reviews. Each user is either a basic user or an administrator.

* The user can log in and out, as well as create a new account.
* The user sees dance schools as a list and can select a school to view more information (such as dance styles and reviews).
* The user can provide a review (stars and comments) for a school and read reviews from others.
* The administrator can add and remove schools and specify the information displayed about the school.
* The user can search for all schools whose description contains a given word (e.g. dance style "Tango").
* The user also sees a list where schools are ranked from best to worst according to reviews.
* The administrator can, if necessary, delete a review provided by a user.
* The administrator can create groups to classify schools. A school can belong to one or more groups. Groups can be e.g. "Latin", "Ballroom" or "Hip-Hop".
