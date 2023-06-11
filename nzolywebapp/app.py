from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import re
from datetime import datetime
import mysql.connector
from mysql.connector import FieldType
import connect

app = Flask(__name__)

dbconn = None
connection = None

def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, \
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn

# default / base page
@app.route("/")
def home():
    return render_template("base.html")

# public interface list members
@app.route("/listmembers")
def listmembers():
    # get the members' data from members table in database
    connection = getCursor()
    connection.execute("SELECT members.MemberID, teams.TeamName, members.FirstName, members.LastName, members.City, members.Birthdate FROM members JOIN teams on members.TeamID = teams.TeamID;")
    memberList = connection.fetchall()
    # print(memberList)
    return render_template("memberlist.html", memberlist = memberList)

# public interface list events
@app.route("/listevents")
def listevents():
    # get the events' data from events table in database
    connection = getCursor()
    connection.execute("SELECT * FROM events;")
    eventList = connection.fetchall()
    # print(eventList)
    return render_template("eventlist.html", eventlist = eventList)

# member list clickable name linking to athlete interface
@app.route("/listmembers/<name>")
def athleteinterface(name):
    # get the upcoming events data from database
    connection = getCursor()
    sql = """SELECT EventName, StageDate, StageName, Location 
                        FROM events 
                        LEFT JOIN event_stage
                        ON events.EventID = event_stage.EventID
                        LEFT JOIN teams
                        ON teams.TeamID = events.NZTeam
                        LEFT JOIN members
                        ON teams.TeamID = members.TeamID
                        WHERE (StageID IS NULL OR StageID NOT IN (SELECT event_stage_results.StageID FROM event_stage_results)) AND members.FirstName = %s"""
    parameters = (name,)
    connection.execute(sql, parameters)
    upcomingevents = connection.fetchall()
    # get the athlete's previous results data from database
    sql = """SELECT EventName, StageDate, StageName, Location, Qualifying, PointsScored, PointsToQualify, Position
                        FROM event_stage_results
                        LEFT JOIN members
                        ON members.MemberID = event_stage_results.MemberID
                        LEFT JOIN event_stage
                        ON event_stage.StageID = event_stage_results.StageID
                        LEFT JOIN events
                        ON events.EventID = event_stage.EventID
                        Where FirstName = %s
                        ORDER BY EventName, StageDate;"""
    connection.execute(sql, parameters)
    previousresult = connection.fetchall()
    # print(upcomingevents)
    # print(previousresults)
    return render_template("athleteinterface.html", name = name, upcomingevents = upcomingevents, previousresult = previousresult)

# admin interface base page
@app.route("/admin")
def admin():
    return render_template("admin.html")

# admin interface list members
@app.route("/admin/listmembers")
def adminlistmembers():
    # get members data from database
    connection = getCursor()
    connection.execute("SELECT members.MemberID, teams.TeamName, members.FirstName, members.LastName, members.City, members.Birthdate FROM members JOIN teams on members.TeamID = teams.TeamID ORDER BY teams.TeamID, LastName, FirstName;")
    memberList = connection.fetchall()
    # print(memberList)
    return render_template("adminmemberlist.html", memberlist = memberList)

# admin interface list events
@app.route("/admin/listevents")
def adminlistevents():
    # get events data from database
    connection = getCursor()
    connection.execute("SELECT EventID, EventName, Sport, TeamName, NZTeam FROM events LEFT JOIN teams ON events.NZTeam = teams.TeamID;")
    eventList = connection.fetchall()
    # print(eventList)
    return render_template("admineventlist.html", eventlist = eventList)

# admin interface list event stages
@app.route("/admin/liststages")
def liststages():
    # get event stage data from database
    connection = getCursor()
    connection.execute("SELECT event_stage.EventID, EventName, StageID, StageName, Location, StageDate, Qualifying, PointsToQualify FROM event_stage LEFT JOIN events ON event_stage.EventID = events.EventID;")
    stageList = connection.fetchall()
    # print(stageList)
    return render_template("stagelist.html", stagelist = stageList)

# admin interface search for members or/and events
@app.route("/admin/search")
def search():
    # print the search page with search bar
    return render_template("search.html")

@app.route("/admin/results", methods = ['get'])
def results():
    # receive the input from user
    name=request.args.get('searchinfo')
    member=request.args.get('searchmember')
    event=request.args.get('searchevent')
    # if search members and/or events
    if name:
        str = name.split() # seperate the input string into a list of words
        # empty list for extending later
        memberResults = list()
        eventResults = list()
        
        connection = getCursor()
        # for loop to find all members and events whose name contains each word in the list
        for item in str:
            sql1 = """SELECT * 
                    FROM members 
                    WHERE members.FirstName LIKE %s OR members.LastName LIKE %s;"""
            parameters = (f"%{item}%")
            connection.execute(sql1, (parameters, parameters))
            memberResults.extend(connection.fetchall())
            memberResults = list(set(memberResults)) # eliminate duplicated members
            sql2 = """SELECT *
                    FROM events
                    WHERE events.EventName LIKE %s;"""
            connection.execute(sql2, (parameters,))
            eventResults.extend(connection.fetchall())
            eventResults = list(set(eventResults)) # eliminate duplicated events
        # print(memberResults)
        # print(eventResults)
        return render_template("results.html", name = name, memberresults = memberResults, eventresults = eventResults)
    # if only search members
    elif member:

        str = member.split()  # seperate the input string into a list of words
        memberResults = list()  # empty member list for extending later
        connection = getCursor()
        # for loop to find all members whose name contains each word in the list
        for item in str:
            sql = """SELECT *
                    FROM members
                    WHERE members.FirstName LIKE %s OR members.LastName LIKE %s;"""
            parameters = (f"%{item}%")
            connection.execute(sql, (parameters, parameters))
            memberResults.extend(connection.fetchall())
            memberResults = list(set(memberResults)) # eliminate duplicated members
        # print(memberResults)
        return render_template("memberresults.html", str = str, name = member, memberresults = memberResults)
    # if only search events
    elif event:
        str = event.split() # seperate the input string into a list of words
        eventResults = list() # empty event list for extending later
        connection = getCursor()
        # for loop to find all events whose name contains each word in the list
        for item in str:
            sql = """SELECT *
                    FROM events
                    WHERE events.EventName LIKE %s;"""
            parameters = (f"%{item}%")
            connection.execute(sql, (parameters, ))
            eventResults.extend(connection.fetchall())
            eventResults = list(set(eventResults)) # eliminate duplicated events
        # print(eventResults)
        return render_template("eventresults.html", name = event, eventresults = eventResults)

# admin interface add members     
@app.route("/admin/addmembers")
def addmembers():
    # get team data from database
    connection = getCursor()
    sql = """SELECT * FROM teams;"""
    connection.execute(sql)
    team = connection.fetchall()
    # pass 'team' data to addmembers.html page for users to select
    return render_template("addmembers.html", team = team)

# function to receive input data and insert the data into database
@app.route("/admin/members/add", methods=["POST"])
def membersadd():
    # receive input data from addmembers.html page
    connection = getCursor()
    teamid = request.form.get('team')
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    city = request.form.get('city')
    birthdate = request.form.get('birthdate')
    # insert the input data into database
    sql = "INSERT INTO members (TeamID, FirstName, LastName, City, Birthdate) VALUES (%s, %s, %s, %s, %s);"
    parameters = (teamid, firstname, lastname, city, birthdate)
    connection.execute(sql, parameters)
    # print(memberList)
    return redirect("/admin/listmembers")

# admin interface edit members
@app.route("/admin/members/edit/<memberid>")
def editmember(memberid):
    # get team data from database
    connection = getCursor()
    sql = "SELECT * FROM teams;"
    connection.execute(sql)
    team = connection.fetchall()
    # get member data from database
    sql = "SELECT * FROM members WHERE MemberID = %s;"
    parameters = (memberid,)
    connection.execute(sql, parameters)
    membertoedit = connection.fetchone()
    # pass member and team data to editmember.html page for user to select
    return render_template("editmember.html", membertoedit=membertoedit, team = team)

# function to receive input data and insert the data into database
@app.route("/admin/updatemembers", methods=["POST"])
def updatemember():
    # receive the input data from editmember.html page
    teamid = request.form.get('team')
    memberid = int(request.form.get('memberid'))
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    city = request.form.get('city')
    birthdate = request.form.get('birthdate')
    # insert the data to the database
    sql = '''UPDATE members 
            SET TeamID = %s, FirstName = %s, LastName = %s, City = %s, Birthdate= %s
            WHERE MemberID = %s;'''
    parameters = (teamid, firstname, lastname, city, birthdate, memberid)
    connection = getCursor()
    connection.execute(sql, parameters)
    # print(memberList)
    return redirect("/admin/listmembers")

# admin interface add events
@app.route("/admin/addevents")
def addevents():
    # get team data from database
    connection = getCursor()
    sql = """SELECT * FROM teams;"""
    connection.execute(sql)
    team = connection.fetchall()
    # pass team data to addevents.html page
    return render_template("addevents.html", team=team)

# function to receive the event data and insert the data into database
@app.route("/admin/event/add", methods = ['POST'])
def eventadd():
    # receive the input from addevents.html page
    connection = getCursor()
    teamid = request.form.get('team')
    eventname = request.form.get('eventname')
    sport = request.form.get('sport')
    # insert the input data into database
    sql = "INSERT INTO events (EventName, Sport, NZTeam) VALUES (%s, %s, %s);"
    parameters = (eventname, sport, teamid)
    connection.execute(sql, parameters)
    # print(eventList)
    return redirect("/admin/listevents")

# admin interface add stages
@app.route("/admin/addstages")
def addstages():
    # get event data from database
    connection = getCursor()
    sql = """SELECT DISTINCT events.EventID, EventName
            FROM events
            LEFT JOIN event_stage
            ON event_stage.EventID = events.EventID
            WHERE events.EventID NOT IN (SELECT EventID FROM event_stage WHERE event_stage.Qualifying = 0);"""
    connection.execute(sql)
    event = connection.fetchall()
    # pass event data to addstages.html page
    return render_template("addstages.html", event=event)

# function to receive stage data and insert the data into database
@app.route("/admin/stage/add", methods = ['POST'])
def stageadd():
    # receive user input from addstages.html page
    eventid = request.form.get('event')
    stagename = request.form.get('stagename').lower()
    location = request.form.get('location')
    stagedate = request.form.get('stagedate')
    pointstoqualify = request.form.get('pointstoquality')
    # deduce the value of Qualifying and pointstoqualify according to the other values
    if stagename == 'final':
        qualifying = 0 
        pointstoqualify = None
    else:
        qualifying = 1
        if pointstoqualify == "":
            pointstoqualify = 0
    # insert the data into database
    sql = "INSERT INTO event_stage (StageName, EventID, Location, StageDate, Qualifying, PointsToQualify) VALUES (%s, %s, %s, %s, %s, %s);"
    parameters = (stagename.title(), eventid, location.title(), stagedate, qualifying, pointstoqualify)
    connection = getCursor()
    connection.execute(sql, parameters)
    # print(stageList)
    return redirect("/admin/liststages")

# admin interface add scores
@app.route("/admin/addscores")
def addscores():
    # get stage data from database
    connection = getCursor()
    sql = '''SELECT *
            FROM event_stage
            LEFT JOIN events
            ON event_stage.EventID = events.EventID 
            WHERE StageID NOT IN (SELECT event_stage_results.StageID FROM event_stage_results WHERE PointsScored IS NOT NULL);'''  
    connection.execute(sql)
    stage = connection.fetchall()
    # get member data from database
    connection.execute("SELECT * FROM members;")
    member = connection.fetchall()
    # pass stage and member to addscores.html page
    return render_template("addscores.html", stage = stage, member=member)

# function to receive input data and insert the data into database
@app.route("/admin/score/add", methods = ['POST'])
def scoreadd():
    # receive input data from addscores.html page
    stageid = request.form.get('stage')
    memberid = request.form.get('member')
    pointsscored = request.form.get('pointsscored')
    position = request.form.get('position')
    if position == "" or position == "0":
        position = None
    # get stage name according to stageid from database
    sql = "SELECT StageName FROM event_stage WHERE event_stage.StageID = %s"
    connection = getCursor()
    connection.execute(sql, (stageid,))
    stagename = connection.fetchone()[0]
    # judge if the input stage name and position is valid, if not valid, input again; if valid, insert the data into database
    if (stagename.lower() == "final" and position == None) or (stagename.lower() != "final" and position != None):
        return redirect("/admin/addscores")
    else:
        sql = "INSERT INTO event_stage_results (StageID, MemberID, PointsScored, Position) VALUES (%s, %s, %s, %s);"
        parameters = (stageid, memberid, pointsscored, position)
        connection.execute(sql, parameters)
        # print(scoreList)
        return redirect("/admin/listscores")

@app.route("/admin/listscores")
def listscores():
    # get the scores data from database
    connection = getCursor()
    sql = '''SELECT ResultID, EventName, StageName, event_stage_results.StageID, FirstName, LastName, event_stage_results.MemberID, PointsScored, Position
            FROM event_stage_results
            LEFT JOIN event_stage
            ON event_stage.StageID = event_stage_results.StageID
            LEFT JOIN events
            ON events.EventID = event_stage.EventID
            LEFT JOIN members
            ON members.MemberID = event_stage_results.MemberID;'''
    connection.execute(sql)
    scorelist = connection.fetchall()
    # print(scoreList)
    return render_template("listscores.html", scorelist = scorelist)

# admin interface show the medal reports
@app.route("/admin/showmedals")
def showmedals():
    connection = getCursor()
    # number of medals in total
    connection.execute("SELECT COUNT(Position) FROM event_stage_results WHERE Position > 0 AND Position < 4;")
    num_medals = connection.fetchall()
    # number of gold medals
    connection.execute("SELECT COUNT(Position) FROM event_stage_results WHERE Position=1")
    num_gold = connection.fetchall()
    # number of silver medals
    connection.execute("SELECT COUNT(Position) FROM event_stage_results WHERE Position=2")
    num_silver = connection.fetchall()
    # number of bronze medals
    connection.execute("SELECT COUNT(Position) FROM event_stage_results WHERE Position=3")
    num_bronze = connection.fetchall()
    # get gold medal winners from database
    sql = '''SELECT members.MemberID, FirstName, LastName, TeamName, members.TeamID
            FROM event_stage_results
            LEFT JOIN members
            ON members.MemberID = event_stage_results.MemberID
            LEFT JOIN teams
            ON teams.TeamID = members.TeamID
            WHERE Position=1
            ORDER BY TeamID, LastName, Firstname'''
    connection.execute(sql)
    gold_members = connection.fetchall()
    # get silver medal winners from database
    sql = '''SELECT members.MemberID, FirstName, LastName, TeamName, members.TeamID
            FROM event_stage_results
            LEFT JOIN members
            ON members.MemberID = event_stage_results.MemberID
            LEFT JOIN teams
            ON teams.TeamID = members.TeamID
            WHERE Position=2
            ORDER BY TeamID, LastName, Firstname'''
    connection.execute(sql)
    silver_members = connection.fetchall()
    # get bronze medal winners from database
    sql = '''SELECT members.MemberID, FirstName, LastName, TeamName, members.TeamID
            FROM event_stage_results
            LEFT JOIN members
            ON members.MemberID = event_stage_results.MemberID
            LEFT JOIN teams
            ON teams.TeamID = members.TeamID
            WHERE Position=3
            ORDER BY TeamID, LastName, Firstname'''
    connection.execute(sql)
    bronze_members = connection.fetchall()
    # print the report
    return render_template("showmedals.html", num_medals=num_medals, num_gold=num_gold, num_silver=num_silver, num_bronze=num_bronze, gold_members=gold_members, silver_members=silver_members, bronze_members=bronze_members)

# admin interface show the member reports
@app.route("/admin/showmembers")
def showmembers():
    # print(memberList)
    return redirect("/admin/listmembers")