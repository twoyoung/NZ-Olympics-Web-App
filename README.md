# COMP636-Web-Application-Project
COMP636 Web App

## Outline of the structure of the Web App

- **the default / interface**
  - **the base page**
  
  | route | function | template | data passed | explanation |
  | --- | --- | --- | --- | --- |
  | @app.route("/") | home() | base.html | none | - |
  | @app.route("/listmembers") | listmembers() | memberlist.html | `memberlist` | - |
  | @app.route("/listevents") | listevents() | eventlist.html | `eventlist` | - |
  - **the athlete interface**
  
  | route | function | template | data passed | explanation |
  | --- | --- | --- | --- | --- |
  | @app.route("/listmembers/<name>") | athleteinterface(name) | athleteinterface.html | `name`, `athleteinfo`, `eventinfo` | - | 
- **the admin interface**
  - **the admin base page**
  
  | route | function | template | data passed | explanation |
  | --- | --- | --- | --- | --- |
  | @app.route("/admin") | admin() | admin.html | none | - |
  | @app.route("/admin/listmembers") | adminlistmembers() | adminmemberlist.html | `memberlist` | display the most recently updated member list |
  - **search members or/and events using partial match**
  
  | route | function | template | data passed | explanation |
  | --- | --- | --- | --- | --- |
  | @app.route("/admin/results") | search()| results.html| `name`, `memberresults`, `eventresults` | - |
  - **add new members**
  
  | route | function | template | data passed | explanation |
  | --- | --- | --- | --- | --- |
  | @app.route("/admin/addmembers") | addmembers() | addmembers.html | `teamid` | addmembers() pass the available team id in database (`teamid`) to addmembers.html to display the form with limited team id choice for users to input the data | 
  | @app.route("/admin/members/add", methods=["POST"]) | membersadd() | addmembers.html | `memberid`, `teamid`, `firstname`, `lastname`, `city`, `birthdate` | admembers.html pass the input data to membersadd(), membersadd() then insert the data into database |
  - **edit existing members**
  
  | route | function | template | data passed | explanation |
  | --- | --- | --- | --- | --- |
  | @app.route("/admin/members/edit/<memberid>") | editmember(memberid) | editmember.html | `membertoedit`, `teamid` |   adminmemberlist.html or results.html pass the `memberid` to editmember(memberid) to locate the member to edit; editmember(memberid) finds the member data with the same member id from database and the available team id list and pass them to editmember.html which could display the form with the member information for user to edit|
  | @app.route("/admin/updatemembers", methods=["POST"]) | updatemember() | editmember.html | `memberid`, `teamid`, `firstname`, `lastname`, `city`, `birthdate` | editmember.html pass the edited data to updatemember() which update the database | 
  - **add new events**
  
  | route | function | template | data passed | explanation |
  | --- | --- | --- | --- | --- |
  | @app.route("/admin/addevents") | addevents() | addevents.html | teamid | - |
  | @app.route("/admin/event/add", methods = ['POST']) | eventadd() | addevents.html | `eventid`, `eventname`, `sport`, `teamid` | - |
  | @app.route("/admin/listevents") | listevents() | eventlist.html | `eventlist` | - |
 
  - **add new event_stages**
  @app.route("/admin/addstages")
  @app.route("/admin/stage/add", methods = ['POST'])
  @app.route("/admin/liststages")
  - **add scores and position**
  @app.route("/admin/addscores")
  @app.route("/admin/score/add", methods = ['POST'])
  @app.route("/admin/listscores")
  - **show the medal reports**
  @app.route("/admin/showmedals")


## Assumptions


## Changes required if the Web App was to support multiple different Olympics
