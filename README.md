# DanceHub_Web_Application
-----

A platform to search for dance schools, read their reviews and socialize on the dance community forum. Dance enthusiasts often face the challenge of not having a centralized platform to access information about different dance opportunities in their area. Dancehub platform gathers the necessary information for all dancers and provides a community forum to share events, seek advice or chat with fellow dancers.

The application displays dance schools registered in Dancehub. Users can search for dance schools based on school name, city, description or a specific dance style. In the application it's possible to add or read reviews of the schools. Each user is either a basic user or an administrator.

* The user can log in and out, as well as create a new account.
* The user sees dance schools as a list and can select a school to view more information (such as dance styles, location, URL and reviews).
* The dance schools are listed according to their ranking from best to worst according to reviews.
* The user can provide a review (stars and comments) for a school and read reviews from others.
* The administrator can, if necessary, delete a review provided by a user.
* The user can search for all schools whose name, city, description or one of its dance styles contain a given word ("Tango" or "Helsinki").
* The administrator can add and remove schools and specify the information displayed about the school. A school can belong to one or more dance style groups. Groups are  e.g. "Latin", "Ballroom" and "Hip Hop".
* The user or administrator can chat on the forum page

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
DATABASE_URL=postgresql:///(your_database_name)

SECRET_KEY=(create own)
```
4) activate virtual environment and install the dependencies in the requirements file

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
5) Connect to your database, if default database not used:
```bash
psql
\c (your_database_name)
```

6) Define the SQL schema:
```bash
\i schema.sql
```
7) run the application within a Flask environment
```bash
flask run
```