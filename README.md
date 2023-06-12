# COMP636-Web-Application-Project
COMP636 Web App

## Outline of the structure of the Web App

- <h2>the default / interface</h2>
  <h3>the base page</h3>
  
  | route | function | template | data passed | explanation |
  | --- | --- | --- | --- | --- |
  | **@app.route("/")** | <ins>home()</ins> | *base.html* | None | render the base page |
  | **@app.route("/listmembers")** | <ins>listmembers()</ins> | *memberlist.html* | `memberlist` | <ins>listmembers()</ins> pass `memberlist`<sub>(members table information in database)</sub> to *memberlist.html* |
  | **@app.route("/listevents")** | <ins>listevents()</ins> | *eventlist.html* | `eventlist` | <ins>listevents()</ins> pass `eventlist`<sub>(events table information in database)</sub> to *eventlist.html* |
  <h3>the athlete interface</h3>
  
  | route | function | template | data passed | explanation |
  | --- | --- | --- | --- | --- |
  | **@app.route("/listmembers/< name>")** | <ins>athleteinterface(name)</ins> | *memberlist.html, athleteinterface.html* | `name`, `upcomingevents`, `previousresult` | *memberlist.html* pass `name` to <ins>athleteinterface(name)</ins> to locate the athlete; <ins>athleteinterface(name)</ins> then get data `previousresult`<sub>(athletes previous results)</sub> and `upcomingevents`<sub>(upcoming events)</sub> from database and pass them to *athleteinterface.html* to render | 
- <h2>the admin interface</h2>
  <h3>the admin base page</h3>
  
  | route | function | template | data passed | explanation |
  | --- | --- | --- | --- | --- |
  | **@app.route("/admin")** | <ins>admin()</ins> | *admin.html* | None | render the base page |
  <h3>search members or/and events using partial match</h3>
  
  | route | function | template | data passed | explanation |
  | --- | --- | --- | --- | --- |
  | **@app.route("/admin/search")** | <ins>search()</ins> | *search.html* | None | render the search page  |
  | **@app.route("/admin/results")** | <ins>results()</ins> | *search.html, results.html, memberresults.html, eventresults.html* | `name`, `member`, `event`, `memberresults`, `eventresults` | Depending on the search bar user chooses, *search.html* passes `name`or `member`or `event` <sub>(user input data)</sub> to <ins>search()</ins>; <ins>search()</ins> get `memberresults` and/or `eventresults`from database and pass them to *results.html* or *memberresults.html* or *eventresults.html* to render the search results|
  <h3>add new members</h3>
  
  | route | function | template | data passed | explanation |
  | --- | --- | --- | --- | --- |
  | **@app.route("/admin/addmembers")** | <ins>addmembers()</ins> | *addmembers.html* | `team` | <ins>addmembers()</ins> pass `team`<sub>(teams table in database)</sub> to *addmembers.html* so that *addmembers.html* could render the form with a selection of available teams for user to choose | 
  | **@app.route("/admin/members/add")** | <ins>membersadd()</ins> | *addmembers.html* | `teamid`, `firstname`, `lastname`, `city`, `birthdate` | *addmembers.html* pass the input data to <ins>membersadd()</ins>; <ins>membersadd()</ins> then insert the data into database |
  | **@app.route("/admin/listmembers")** | <ins>adminlistmembers()</ins> | *adminmemberlist.html* | `memberlist` | <ins>adminlistmembers()</ins> get the updated data `memberlist` from database and pass it to *adminmemberlist.html* to render |
  <h3>edit existing members</h3>
  
  | route | function | template | data passed | explanation |
  | --- | --- | --- | --- | --- |
  | **@app.route("/admin/members/edit/< memberid>")** | <ins>editmember()</ins> | *adminmemberlist.html, results.html, editmember.html* | `memberid`, `membertoedit`, `team` | *adminmemberlist.html* or *results.html* pass `memberid` to <ins>editmember()</ins> to locate the member to edit; <ins>editmember()</ins> gets `team`(<sub>a list of the teams</sub>) and `membertoedit`(<sub>member with the required member ID</sub>) from database and pass them to *editmember.html* to render the form with the member information for user to edit|
  | **@app.route("/admin/updatemembers")** | <ins>updatemember()</ins> | *editmember.html* | `teamid`, `memberid`, `firstname`, `lastname`, `city`, `birthdate` | *editmember.html* pass the edited data to <ins>updatemember()</ins> which then update the database with the data | 
  <h3>add new events</h3>
  
  | route | function | template | data passed | explanation |
  | --- | --- | --- | --- | --- |
  | **@app.route("/admin/addevents")** | <ins>addevents()</ins> | *addevents.html* | `team` | <ins>addevents()</ins> pass `team`<sub>(teams table in database)</sub> to *addevents.html* so that *addevents.html* could render the form with a selection of available teams for user to choose |
  | **@app.route("/admin/event/add")** | <ins>eventadd()</ins> | *addevents.html* | `eventname`, `sport`, `teamid` | *addevents.html* pass the input data to <ins>eventadd()</ins>; <ins>eventadd()</ins> then insert the data into database  |
  | **@app.route("/admin/listevents")** | <ins>adminlistevents()</ins> | *admineventlist.html* | `eventlist` | <ins>adminlistevents()</ins> get the updated data `eventlist` from database and pass it to *admineventlist.html* to render |
 
  <h3>add new event stages</h3>
  
  | route | function | template | data passed | explanation |
  | --- | --- | --- | --- | --- |
  | **@app.route("/admin/addstages")** | <ins>addstages()</ins> | *addstages.html* | `event` | <ins>addstages()</ins> pass `event`<sub>(events table in database)</sub> to *addstages.html* so that *addstagess.html* could render the form with a selection of available events for user to choose  |
  | **@app.route("/admin/stage/add")** | <ins>stageadd()</ins> | *addstages.html* | `stagename`, `eventid`, `location`, `stagedate`, `qualifying`, `pointstoqualify` | *addstages.html* pass the user input data to <ins>stageadd()</ins> , which then insert the data into database |
  | **@app.route("/admin/liststages")** | <ins>liststages()</ins> | *stagelist.html* | `stagelist` | <ins>liststages()</ins> get the updated data `stagelist` from database and pass it to *stagelist.html* to render |
  <h3>add scores and position</h3>
  
  | route | function | template | data passed | explanation |
  | --- | --- | --- | --- | --- |
  | **@app.route("/admin/addscores")** | <ins>addscores()</ins> | *addscores.html* | `stage`, `member` | <ins>addscores()</ins> pass `stage`<sub>(event_stage table in database)</sub> and `member` <sub>(members talbe in database)</sub> to *addscores.html* so that *addscores.html* could render the form with a selection of available stages and members for user to choose  |
  | **@app.route("/admin/score/add")** | <ins>scoreadd()</ins> | *addscores.html* | `stageid`, `memberid`, `pointsscored`, `position` | *addscores.html* pass the user input data to <ins>scoreadd()</ins>, which then insert the data into database |
  | **@app.route("/admin/listscores")** | <ins>listscores()</ins> | *listscores.html* | `scorelist` | <ins>listscores()</ins> get the updated data `scorelist` from database and pass it to *listscores.html* to render |
  <h3>show the medal reports</h3>
  
  | route | function | template | data passed | explanation |
  | --- | --- | --- | --- | --- |
  | **@app.route("/admin/showmedals")** | <ins>showmedals()</ins> | *showmedals.html* | `num_medals`, `num_gold`, `num_silver`, `num_bronze`, `gold_members`, `silver_members`, `bronze_members` | <ins>showmedals()</ins> get the data from database and then pass them to *showmedals.html* to render |
  <h3>show the team member reports</h3>
  
  | route | function | template | data passed | explanation |
  | --- | --- | --- | --- | --- |
  | **@app.route("/admin/showmembers")** | <ins>showmembers()</ins> | None | None | redirect to **@app.route("/admin/listmembers")** to render the member list |


## Assumptions
- **Clickable Name on Member List:** The project requirement asks to make the member name on member list clickable and links to athlete interface, but it does not specify FirstName or LastName, or both. I just made the FirstName clickable and I assumed that all the firstnames are different.
- **Upcoming Events in Athlete Interface:** Due to the lack of linking information between each athlete/member and the event/stage that does not have a score (upcoming events/stages), I changed the output from the specified athlete's upcoming events/stages to the athlete's team's upcoming events/stages. So the specified athlete could attend 0, 1, or many of the upcoming events/stages listed.
- **Search Function in Admin Interface:** Here I designed 3 ways of searching: searching from both members and events database at the same time in just one click, searching just for members and searching just for events. It accepts any length of strings, splits the input strings into seperate words by space, searches each words in members and/or events database and then returns the results in the corresponding page.
- **Base Page Template between Public and Admin Interface:** I chose to create another page template for admin interface instead of using the one for public interface. The reason is that admin interface involves more functions than public interface and I want to just create one base page to contain those function links and let all the admin interface pages inheritate from it.
- **GET or POST Method:** I did not explicitly detect the methods used as my code does not involve returning different pages according to different methods. I used POST method for most of the form submissions that involve adding or editing data to the database. I used Get method in searching function.
- **Adding Data with Auto Increment Primary Key:** Noticing that all the tables in the database have auto increment primary key, in the adding data user interface I chose not to ask the user to input the primary key such as member ID or event ID, which might lead to collision of primary keys and need extra effort to detect and validate it, but left it and let it increate by itself.
- **Showing the Team Member Report:** Here I let this function redirect to the list team members function and share the same member list html page instead of creating a specific html page for the report. To meet the requirement I let the member list ordered according to the requirement.
- **Adding Position Corresponding to the Stage:** I expected the best solution would be to limit the selection choice of Position according to the previous selection of Stage name, so if the selected stage was not final, then Position selection would not be available. But this seems to be involving complicated Javascript which is beyond my current knowledge. At last, I provided a compromise solution, which is that if the input of stage name and position does not meet the check at the server, the input page will be reloaded with no pop up reminding message and user just need to input the data again.
- **Using Javascript together with Bootstrap to validate the input:** I found it's tricky to validate the input after the data has been passed to the server side. I was expecting to validate some input before it's been passed to the server. After some searching I found a piece of useful Javascript code which could do this job which is as follows. I put it into the base page *admin.html* so it could help validate all the inputs under the admin interface. It can both validate if the require field is empty and if the input is number at Pointstoqualify and Score field.
```Javascript
            <script>
              // Enable form validation
              (function () {
                'use strict';
            
                // Fetch all the forms we want to apply custom Bootstrap validation styles to
                var forms = document.querySelectorAll('.needs-validation');
            
                // Loop over them and prevent submission
                Array.prototype.slice.call(forms).forEach(function (form) {
                  form.addEventListener('submit', function (event) {
                    if (!form.checkValidity()) {
                      event.preventDefault();
                      event.stopPropagation();
                    }
            
                    form.classList.add('was-validated');
            
                    var numberInput = document.getElementById('numberInput');
                    if (!isValidNumber(numberInput.value.trim())) {
                      event.preventDefault();
                      event.stopPropagation();
                      numberInput.classList.add('is-invalid');
                    } else {
                      numberInput.classList.remove('is-invalid');
                    }
                  }, false);
                });
              })();
            
              // Custom validation function to check if the input is a valid number
              function isValidNumber(input) {
                if (input === '') {
                  return true; // Allow empty input
                }
            
                var numberPattern = /^\d+(\.\d+)?$/;
                return numberPattern.test(input);
              }
            </script>
```
## Changes required if the Web App was to support multiple different Olympics
- **Database Tables Change:**
  - A new talbe Olympics that could store different Olympics' Name and it's ID and maybe some other information such as season(summer or winter), location(country), year, etc.
  - The existing events table needs to include a new column of Olympics ID to indicate which Olympics each event associates to.
  - The event_stage table needs an extra column of Olympics ID to specify which Olympics each event stage associates to.
  - The foreign key references in some tables need to be modified to reflect the changes in table names and structure.
- **Design and Implementation of the Web App:**
  - There needs a function to list all the Olypmpics with the name clickable that links to another interface like the 'NZ Winter Olympics' public interface.
  - Update the SQL queries throughout the code to reference the tables for different Olympics.
  - Update the route modifiers to handle requests specific to each type of Olympics. For example, there could be separate routes for listing summer events and winter events.
  - Need some new html templates and base page template to display information specific to each type of Olympics.
