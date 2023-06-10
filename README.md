# COMP636-Web-Application-Project
COMP636 Web App

## Outline of the structure of the Web App

- the default / interface
  - the base page
  
  | route | function | template | data passed | explanation |
  | --- | --- | --- | --- | --- |
  | @app.route("/") | home() | base.html | none | - |
  | @app.route("/listmembers") | listmembers() | memberlist.html | `memberlist` | - |
  | @app.route("/listevents") | listevents() | eventlist.html | `eventlist` | - |
  - the athlete interface
  
  | route | function | template | data passed | explanation |
  | --- | --- | --- | --- | --- |
  | @app.route("/listmembers/<name>") | athleteinterface(name) | athleteinterface.html | `name`, `athleteinfo`, `eventinfo` | - | 
- the admin interface
  - the admin base page
  
  | route | function | template | data passed | explanation |
  | --- | --- | --- | --- | --- |
  | @app.route("/admin") | admin() | admin.html | none | - |
  - search members or/and events using partial match
  
  | route | function | template | data passed | explanation |
  | --- | --- | --- | --- | --- |
  | @app.route("/admin/results") | search()| results.html| `name`, `memberresults`, `eventresults` | - |
  - add new members
  
  | route | function | template | data passed | explanation |
  | --- | --- | --- | --- | --- |
  | @app.route("/admin/addmembers") | addmembers() | addmembers.html | `teamid` | - | 
  | @app.route("/admin/members/add", methods=["POST"]) | membersadd() | - | `memberid`, `teamid`, `firstname`, `lastname`, `city`, `birthdate` | insert the data into database |
  | @app.route("/admin/listmembers") | adminlistmembers() | adminmemberlist.html | `memberlist` | display the updated member list |
  - edit existing members
  @app.route("/admin/members/edit/<memberid>")
  @app.route("/admin/updatemembers", methods=["POST"])
  - add new events
  @app.route("/admin/addevents")
  @app.route("/admin/event/add", methods = ['POST'])
  @app.route("/admin/listevents")
  - add new event_stages
  @app.route("/admin/addstages")
  @app.route("/admin/stage/add", methods = ['POST'])
  @app.route("/admin/liststages")
  - add scores and position
  @app.route("/admin/addscores")
  @app.route("/admin/score/add", methods = ['POST'])
  @app.route("/admin/listscores")
  - show the medal reports
  @app.route("/admin/showmedals")


## Assumptions


## Changes required if the Web App was to support multiple different Olympics
