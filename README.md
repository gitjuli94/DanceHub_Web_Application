# DanceHub_Web_Application
---current status:
* user or admin can create an account
* database created for dance schools and dance events, not yet functioning properly
* web page layout is the final form but needs improving
  
* install:
    1) clone the repository
    2) install the dependencies in the requirements file
    3) run the application within a Flask environment


-----

A platform to search for dance classes, read reviews and discover social dance events. 

The application displays dance schools in a specific area, where users can search for dance classes and social dance events based on a specific dance style (e.g. salsa, tango or rock). Clarification: dance class is a guided session with an instructor and social dancing events are informal gatherings where people freely dance with each other and mingle to meet new people. Both are organized in dance schools. In the application it's possible to check the schedules for these events and read their reviews. Each user is either a basic user or an administrator.

* The user can log in and out, as well as create a new account.
* The user sees dance schools on the map and can select a school to view more information (such as dance styles and schedules for classes and socials).
* The user can provide a review (stars and comments) for a school and read reviews from others.
* The administrator can add and remove schools and specify the information displayed about the school.
* The user can search for all schools whose description contains a given word (e.g. dance style "Tango").
* The user also sees a list where schools are ranked from best to worst according to reviews.
* The administrator can, if necessary, delete a review provided by a user.
* The administrator can create groups to classify schools. A school can belong to one or more groups. Groups can be e.g. "Latin", "Ballroom" or "Hip-Hop".
