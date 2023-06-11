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
  | **@app.route("/admin/members/add")** | <ins>membersadd()</ins> | *addmembers.html* | `teamid`, `firstname`, `lastname`, `city`, `birthdate` | *addmembers.html* pass the input data to <ins>membersadd()</ins>; <ins>membersadd()</ins> then insert the data into database |
  | **@app.route("/admin/listmembers")** | <ins>adminlistmembers()</ins> | *adminmemberlist.html* | `memberlist` | <ins>adminlistmembers()</ins> get the updated data `memberlist` from database and pass it to *adminmemberlist.html* to render |
  - **edit existing members**
  
  | route | function | template | data passed | explanation |
  | --- | --- | --- | --- | --- |
  | **@app.route("/admin/members/edit/< memberid>")** | <ins>editmember()</ins> | *adminmemberlist.html, results.html, editmember.html* | `memberid`, `membertoedit`, `team` | *adminmemberlist.html* or *results.html* pass `memberid` to <ins>editmember()</ins> to locate the member to edit; <ins>editmember()</ins> gets `team`(<sub>a list of the teams</sub>) and `membertoedit`(<sub>member with the required member ID</sub>) from database and pass them to *editmember.html* to render the form with the member information for user to edit|
  | **@app.route("/admin/updatemembers")** | <ins>updatemember()</ins> | *editmember.html* | `teamid`, `memberid`, `firstname`, `lastname`, `city`, `birthdate` | *editmember.html* pass the edited data to <ins>updatemember()</ins> which then update the database with the data | 
  - **add new events**
  
  | route | function | template | data passed | explanation |
  | --- | --- | --- | --- | --- |
  | **@app.route("/admin/addevents")** | <ins>addevents()</ins> | *addevents.html* | `team` | <ins>addevents()</ins> pass `team`<sub>(teams table in database)</sub> to *addevents.html* so that *addevents.html* could render the form with a selection of available teams for user to choose |
  | **@app.route("/admin/event/add")** | <ins>eventadd()</ins> | *addevents.html* | `eventname`, `sport`, `teamid` | *addevents.html* pass the input data to <ins>eventadd()</ins>; <ins>eventadd()</ins> then insert the data into database  |
  | **@app.route("/admin/listevents")** | <ins>adminlistevents()</ins> | *admineventlist.html* | `eventlist` | <ins>adminlistevents()</ins> get the updated data `eventlist` from database and pass it to *admineventlist.html* to render |
 
  - **add new event_stages**
  
  | route | function | template | data passed | explanation |
  | --- | --- | --- | --- | --- |
  | **@app.route("/admin/addstages")** | <ins>addstages()</ins> | *addstages.html* | `event` | <ins>addstages()</ins> pass `event`<sub>(events table in database)</sub> to *addstages.html* so that *addstagess.html* could render the form with a selection of available events for user to choose  |
  | **@app.route("/admin/stage/add")** | <ins>stageadd()</ins> | *addstages.html* | `stagename`, `eventid`, `location`, `stagedate`, `qualifying`, `pointstoqualify` | *addstages.html* pass the user input data to <ins>stageadd()</ins> , which then insert the data into database |
  | **@app.route("/admin/liststages")** | <ins>liststages()</ins> | *stagelist.html* | `stagelist` | <ins>liststages()</ins> get the updated data `stagelist` from database and pass it to *stagelist.html* to render |
  - **add scores and position**
  
  | route | function | template | data passed | explanation |
  | --- | --- | --- | --- | --- |
  | **@app.route("/admin/addscores")** | <ins>addscores()</ins> | *addscores.html* | `stage`, `member` | <ins>addscores()</ins> pass `stage`<sub>(event_stage table in database)</sub> and `member` <sub>(members talbe in database)</sub> to *addscores.html* so that *addscores.html* could render the form with a selection of available stages and members for user to choose  |
  | **@app.route("/admin/score/add")** | <ins>scoreadd()</ins> | *addscores.html* | `stageid`, `memberid`, `pointsscored`, `position` | *addscores.html* pass the user input data to <ins>scoreadd()</ins>, which then insert the data into database |
  | **@app.route("/admin/listscores")** | <ins>listscores()</ins> | *listscores.html* | `scorelist` | <ins>listscores()</ins> get the updated data `scorelist` from database and pass it to *listscores.html* to render |
  - **show the medal reports**
  
  | route | function | template | data passed | explanation |
  | --- | --- | --- | --- | --- |
  | **@app.route("/admin/showmedals")** | <ins>showmedals()</ins> | *showmedals.html* | `num_medals`, `num_gold`, `num_silver`, `num_bronze`, `gold_members`, `silver_members`, `bronze_members` | <ins>showmedals()</ins> get the data from database and then pass them to *showmedals.html* to render |


## Assumptions


## Changes required if the Web App was to support multiple different Olympics
