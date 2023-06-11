# COMP636-Web-Application-Project
COMP636 Web App

## Outline of the structure of the Web App

- **the default / interface**
  - **the base page**
  
  | route | function | template | data passed | explanation |
  | --- | --- | --- | --- | --- |
  | **@app.route("/")** | <ins>home()</ins> | *base.html* | - | render the base page |
  | **@app.route("/listmembers")** | <ins>listmembers()</ins> | *memberlist.html* | `memberlist` | <ins>listmembers()</ins> pass `memberlist`<sub>(members table information in database)</sub> to *memberlist.html* |
  | **@app.route("/listevents")** | <ins>listevents()</ins> | *eventlist.html* | `eventlist` | <ins>listevents()</ins> pass `eventlist`<sub>(events table information in database)</sub> to *eventlist.html* |
  - **the athlete interface**
  
  | route | function | template | data passed | explanation |
  | --- | --- | --- | --- | --- |
  | **@app.route("/listmembers/< name>")** | <ins>athleteinterface(name)</ins> | *memberlist.html, athleteinterface.html* | `name`, `upcomingevents`, `previousresult` | *memberlist.html* pass `name` to <ins>athleteinterface(name)</ins> to locate the athlete; <ins>athleteinterface(name)</ins> then get data `previousresult`<sub>(athletes previous results)</sub> and `upcomingevents`<sub>(upcoming events)</sub> from database and pass them to *athleteinterface.html* to render | 
- **the admin interface**
  - **the admin base page**
  
  | route | function | template | data passed | explanation |
  | --- | --- | --- | --- | --- |
  | **@app.route("/admin")** | <ins>admin()</ins> | *admin.html* | - | render the base page |
  - **search members or/and events using partial match**
  
  | route | function | template | data passed | explanation |
  | --- | --- | --- | --- | --- |
  | **@app.route("/admin/search")** | <ins>search()</ins> | *search.html* | - | render the search page  |
  | **@app.route("/admin/results")** | <ins>results()</ins> | *search.html, results.html* | `name`, `memberresults`, `eventresults` | *search.html* pass `name`<sub>(user input data)</sub> to <ins>search()</ins>; <ins>search()</ins> get `memberresults` and `eventresults`from database and pass them to *results.html* to render the search results|
  - **add new members**
  
  | route | function | template | data passed | explanation |
  | --- | --- | --- | --- | --- |
  | **@app.route("/admin/addmembers")** | <ins>addmembers()</ins> | *addmembers.html* | `team` | <ins>addmembers()</ins> pass `team`<sub>(teams table in database)</sub> to *addmembers.html* so that *addmembers.html* could render the form with a selection of available teams for user to choose | 
  | **@app.route("/admin/members/add")** | <ins>membersadd()</ins> | *addmembers.html* | `teamid`, `firstname`, `lastname`, `city`, `birthdate` | *admembers.html* pass the input data to <ins>membersadd()</ins>; <ins>membersadd()</ins> then insert the data into database |
  | **@app.route("/admin/listmembers")** | <ins>adminlistmembers()</ins> | *adminmemberlist.html* | `memberlist` | <ins>adminlistmembers()</ins> get the updated data `memberlist` from database and pass it to *adminmemberlist.html* to render |
  - **edit existing members**
  
  | route | function | template | data passed | explanation |
  | --- | --- | --- | --- | --- |
  | @app.route("/admin/members/edit/<memberid>") | editmember(memberid) | adminmemberlist.html, results.html, editmember.html | `membertoedit`, `teamid` | adminmemberlist.html or results.html pass the `memberid` to editmember() to locate the member to edit; editmember() finds the member data with the same member id from database and the available team id list and pass them to editmember.html which render the form with the member information for user to edit|
  | @app.route("/admin/updatemembers") | updatemember() | editmember.html | `memberid`, `teamid`, `firstname`, `lastname`, `city`, `birthdate` | editmember.html pass the edited data to updatemember() which update the database | 
  - **add new events**
  
  | route | function | template | data passed | explanation |
  | --- | --- | --- | --- | --- |
  | @app.route("/admin/addevents") | addevents() | addevents.html | `teamid` | addevents() pass the existing team id list (`teamid`) to adevents.html to render the form for user to input the data |
  | @app.route("/admin/event/add") | eventadd() | addevents.html | `eventid`, `eventname`, `sport`, `teamid` | addevents.html pass the user input data to eventadd(), which then insert the data to database |
  | @app.route("/admin/listevents") | listevents() | eventlist.html | `eventlist` | listevents() pass the updated event list(`eventlist`) to eventist.html |
 
  - **add new event_stages**
  
  | route | function | template | data passed | explanation |
  | --- | --- | --- | --- | --- |
  | @app.route("/admin/addstages") | addstages() | addstages.html | `eventid` | addstages() pass the existing event id list (`eventid`) to addstages.html to render the form for user to input the data |
  | @app.route("/admin/stage/add") | stageadd() | addstages.html | `stageid`, `stagename`, `eventid`, `location`, `stagedate`, `qualifying`, `pointstoqualify` | addstages.html pass the user input data to stageadd(), which then insert the data to database |
  | @app.route("/admin/liststages") | liststages() | stagelist.html | `stagelist` | liststages() pass the updated stage list (`stagelist`) to stagelist.html |
  - **add scores and position**
  
  | route | function | template | data passed | explanation |
  | --- | --- | --- | --- | --- |
  | @app.route("/admin/addscores") | addscores() | addscores.html | `stageid`, `memberid` | addscores() pass the existing stage id list (`stageid`) and member id list (`memberid`) to addscores.html to render the form for user to input the data |
  | @app.route("/admin/score/add") | scoreadd() | addscores.html | `resultid`, `stageid`, `memberid`, `pointsscored`, `position` | addscores.html pass the user input data to scoreadd(), which then insert the data to database |
  | @app.route("/admin/listscores") | listscores() | listscores.html | `scorelist` | listscores() pass the updated score list (`scorelist`) to listscores.html |
  - **show the medal reports**
  
  | route | function | template | data passed | explanation |
  | --- | --- | --- | --- | --- |
  | @app.route("/admin/showmedals") | showmedals() | showmedals.html | `num_medals`, `num_gold`, `num_silver`, `num_bronze`, `gold_members`, `silver_members`, `bronze_members` | showmedals() pass the data to showmedals.html to render |


## Assumptions


## Changes required if the Web App was to support multiple different Olympics
