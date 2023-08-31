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

# home page for guests
@app.route("/")
def home():
    return render_template("index.html")

# guests view a list all members
@app.route("/members")
def listMembers():
    connection = getCursor()
    connection.execute("SELECT members.MemberID, teams.TeamName, members.FirstName, members.LastName, members.City, members.Birthdate FROM members JOIN teams on members.TeamID = teams.TeamID;")
    memberList = connection.fetchall()
    return render_template("memberList.html", memberList = memberList)

# guests view a list of all events
@app.route("/events")
def listEvents():
    connection = getCursor()
    connection.execute("SELECT EventID, EventName, Sport, TeamName FROM events LEFT JOIN teams on events.NZTeam = teams.TeamID;")
    eventList = connection.fetchall()
    return render_template("eventList.html", eventList = eventList)

# this page list a selected member's upcoming events/stages and previous results
@app.route("/members/<memberID>")
def memberInfo(memberID):
    # get the upcoming events data from database
    connection = getCursor()
    sql = """SELECT EventName, Sport, StageDate, StageName, Location 
                        FROM events 
                        LEFT JOIN event_stage
                        ON events.EventID = event_stage.EventID
                        LEFT JOIN teams
                        ON teams.TeamID = events.NZTeam
                        LEFT JOIN members
                        ON teams.TeamID = members.TeamID
                        WHERE (StageID IS NULL OR StageID NOT IN (SELECT event_stage_results.StageID FROM event_stage_results)) AND members.MemberID = %s;"""
    parameters = (memberID,)
    connection.execute(sql, parameters)
    upcomingEvents = connection.fetchall()
    connection.execute("SELECT FirstName, LastName from members WHERE MemberID = %s;", (memberID,))
    name = connection.fetchone()
    name = name[0] + " " + name[1]
    # get the member's previous results data from database
    sql = """SELECT EventName, Sport, StageDate, StageName, Location, Qualifying, PointsScored, PointsToQualify, Position
                        FROM event_stage_results
                        LEFT JOIN members
                        ON members.MemberID = event_stage_results.MemberID
                        LEFT JOIN event_stage
                        ON event_stage.StageID = event_stage_results.StageID
                        LEFT JOIN events
                        ON events.EventID = event_stage.EventID
                        Where members.MemberID = %s
                        ORDER BY EventName, StageDate;"""
    connection.execute(sql, parameters)
    previousResult = connection.fetchall()
    return render_template("memberInfo.html", name = name, upcomingEvents = upcomingEvents, previousResult = previousResult)

# admin home page
@app.route("/admin")
def admin():
    return render_template("adminIndex.html")

# admin view a list of all members
@app.route("/admin/members")
def adminListMembers():
    connection = getCursor()
    connection.execute("SELECT members.MemberID, teams.TeamName, members.FirstName, members.LastName, members.City, members.Birthdate FROM members JOIN teams on members.TeamID = teams.TeamID ORDER BY teams.TeamID, LastName, FirstName;")
    memberList = connection.fetchall()
    return render_template("adminMemberList.html", memberList = memberList)

# admin view a list of all events
@app.route("/admin/events")
def adminListEvents():
    connection = getCursor()
    connection.execute("SELECT EventID, EventName, Sport, TeamName, NZTeam FROM events LEFT JOIN teams ON events.NZTeam = teams.TeamID;")
    eventList = connection.fetchall()
    return render_template("adminEventList.html", eventList = eventList)

# admin view a list of all event stages
@app.route("/admin/stages")
def listStages():
    connection = getCursor()
    connection.execute("SELECT event_stage.EventID, EventName, StageID, StageName, Location, StageDate, Qualifying, PointsToQualify FROM event_stage LEFT JOIN events ON event_stage.EventID = events.EventID;")
    stageList = connection.fetchall()
    return render_template("stageList.html", stageList = stageList)

# admin view a list of all scores and position
@app.route("/admin/scores")
def listScores():
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
    scoreList = connection.fetchall()
    return render_template("listScores.html", scoreList = scoreList)

# admin search for members or events with partial match
@app.route("/admin/search", methods = ['post','get'])
def search():
    # receive the input
    info=request.args.get('searchinfo')
    if info:
        str = info.split() # seperate the input string into a list of words
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
            sql2 = """SELECT EventID, EventName, Sport, TeamName
                    FROM events
                    LEFT JOIN teams
                    ON events.NZTeam = teams.TeamID
                    WHERE events.EventName LIKE %s;"""
            connection.execute(sql2, (parameters,))
            eventResults.extend(connection.fetchall())
            eventResults = list(set(eventResults)) # eliminate duplicated events
        return render_template("results.html", info=info, memberResults = memberResults, eventResults = eventResults)
    else:
        return redirect("/admin")

# this page for admin to add members    
@app.route("/admin/add-members", methods = ['GET', 'POST'])
def addMembers():
    # get team data from database
    connection = getCursor()
    sql = """SELECT * FROM teams;"""
    connection.execute(sql)
    team = connection.fetchall()
    if request.method == 'POST' and 'birthdate' in request.form and 'firstname' in request.form and 'lastname' in request.form:
        # receive input data from addMembers.html page
        connection = getCursor()
        teamID = request.form.get('team')
        firstName = request.form.get('firstname')
        lastName = request.form.get('lastname')
        city = request.form.get('city')
        birthdate = request.form.get('birthdate')
        # insert the input data into database
        sql = "INSERT INTO members (TeamID, FirstName, LastName, City, Birthdate) VALUES (%s, %s, %s, %s, %s);"
        parameters = (teamID, firstName, lastName, city, birthdate)
        connection.execute(sql, parameters)
        return redirect("/admin/members")
    # pass 'team' data to addMembers.html page for users to select
    return render_template("addMembers.html", team = team)

# this page for admin to edit members
@app.route("/admin/members/edit/<memberID>", methods = ['GET', 'POST'])
def editMember(memberID):
    # get team data from database
    connection = getCursor()
    sql = "SELECT * FROM teams;"
    connection.execute(sql)
    team = connection.fetchall()
    # get member data from database
    sql = "SELECT * FROM members WHERE MemberID = %s;"
    parameters = (memberID,)
    connection.execute(sql, parameters)
    memberToEdit = connection.fetchone()
    if request.method == 'POST' and 'birthdate' in request.form and 'firstname' in request.form and 'lastname' in request.form:
        # receive the input data from editMember.html page
        teamID = request.form.get('team')
        memberID = int(request.form.get('memberid'))
        firstName = request.form.get('firstname')
        lastName = request.form.get('lastname')
        city = request.form.get('city')
        birthdate = request.form.get('birthdate')
        # insert the data to the database
        sql = '''UPDATE members 
                SET TeamID = %s, FirstName = %s, LastName = %s, City = %s, Birthdate= %s
                WHERE MemberID = %s;'''
        parameters = (teamID, firstName, lastName, city, birthdate, memberID)
        connection = getCursor()
        connection.execute(sql, parameters)
        return redirect("/admin/members")
    # pass member and team data to editMember.html page for user to select
    return render_template("editMember.html", memberToEdit=memberToEdit, team = team)

# this page for admin to add events
@app.route("/admin/add-events", methods = ['GET', 'POST'])
def addEvents():
    # get team data from database
    connection = getCursor()
    sql = """SELECT * FROM teams;"""
    connection.execute(sql)
    team = connection.fetchall()
    if request.method == 'POST' and 'eventName' in request.form and 'sport' in request.form:
        # receive the input from addEvents.html page
        connection = getCursor()
        teamID = request.form.get('team')
        eventName = request.form.get('eventName')
        sport = request.form.get('sport')
        # insert the input data into database
        sql = "INSERT INTO events (EventName, Sport, NZTeam) VALUES (%s, %s, %s);"
        parameters = (eventName, sport, teamID)
        connection.execute(sql, parameters)
        return redirect("/admin/events")
    # pass team data to addEvents.html page
    return render_template("addEvents.html", team=team)

# this page for admin to add stages
@app.route("/admin/add-stages", methods = ['GET', 'POST'])
def addStages():
    # get event data from database
    connection = getCursor()
    sql = """SELECT DISTINCT events.EventID, EventName
            FROM events
            LEFT JOIN event_stage
            ON event_stage.EventID = events.EventID
            WHERE events.EventID NOT IN (SELECT EventID FROM event_stage WHERE event_stage.Qualifying = 0);""" # If an event's final stage has already got results, omit it in the event selection list.
    connection.execute(sql)
    event = connection.fetchall()
    if request.method == 'POST' and 'stageName' in request.form and 'location' in request.form and 'stageDate' in request.form:
        # receive user input from addStages.html page
        eventID = request.form.get('event')
        stageName = request.form.get('stageName').lower()
        location = request.form.get('location')
        stageDate = request.form.get('stageDate')
        pointsToQualify = request.form.get('pointsToQuality')
        # deduce the value of Qualifying and pointstoqualify according to the other values
        if stageName == 'final':
            qualifying = 0 
            pointsToQualify = None
        else:
            qualifying = 1
            if pointsToQualify == "":
                pointsToQualify = 0
        # insert the data into database
        sql = "INSERT INTO event_stage (StageName, EventID, Location, StageDate, Qualifying, PointsToQualify) VALUES (%s, %s, %s, %s, %s, %s);"
        parameters = (stageName.title(), eventID, location.title(), stageDate, qualifying, pointsToQualify)
        connection = getCursor()
        connection.execute(sql, parameters)
        return redirect("/admin/stages")
    # pass event data to addStages.html page
    return render_template("addStages.html", event=event)

# this page for admin to add scores
@app.route("/admin/add-scores", methods = ['GET', 'POST'])
def addScores():
    msg=""
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
    # get stage data from database
    if request.method == 'POST' and 'stage' in request.form and 'member' in request.form and 'pointsScored' in request.form:
        print("yes")
        stageID = request.form.get('stage')
        memberID = request.form.get('member')
        pointsScored = request.form.get('pointsScored')
        position = request.form.get('position')
        if position == "" or position == "0":
            position = None
        # get stage name according to stageid from database
        sql = "SELECT StageName FROM event_stage WHERE event_stage.StageID = %s"
        connection = getCursor()
        connection.execute(sql, (stageID,))
        stageName = connection.fetchone()[0]
        # judge if the input stage name and position is valid, if not valid, input again; if valid, insert the data into database
        if stageName.lower() == "final" and position == None:
            msg = "Final stage need a position."
            return render_template("addScores.html", stage = stage, member=member, msg=msg)
        elif stageName.lower() != "final" and position:
            msg = "It's not a final stage. There should be no position"
            return render_template("addScores.html", msg=msg)
        else:
            sql = "INSERT INTO event_stage_results (StageID, MemberID, PointsScored, Position) VALUES (%s, %s, %s, %s);"
            parameters = (stageID, memberID, pointsScored, position)
            connection.execute(sql, parameters)
            return redirect("/admin/scores")
    # pass stage and member to addScores.html page
    return render_template("addScores.html", stage = stage, member=member, msg=msg)


# this page shows the medal reports
@app.route("/admin/show-medals")
def showMedals():
    connection = getCursor()
    # number of medals in total
    connection.execute("SELECT COUNT(Position) FROM event_stage_results WHERE Position > 0 AND Position < 4;")
    numOfMedals = connection.fetchall()
    # number of gold medals
    connection.execute("SELECT COUNT(Position) FROM event_stage_results WHERE Position=1")
    numOfGold = connection.fetchall()
    # number of silver medals
    connection.execute("SELECT COUNT(Position) FROM event_stage_results WHERE Position=2")
    numOfSilver = connection.fetchall()
    # number of bronze medals
    connection.execute("SELECT COUNT(Position) FROM event_stage_results WHERE Position=3")
    numOfBronze = connection.fetchall()
    # get gold medal winners information from database
    sql = '''SELECT members.MemberID, FirstName, LastName, TeamName, EventName, Sport, StageDate, Location, PointsScored
            FROM event_stage_results
            LEFT JOIN members
            ON members.MemberID = event_stage_results.MemberID
            LEFT JOIN teams
            ON teams.TeamID = members.TeamID
            LEFT JOIN event_stage
            ON event_stage.StageID = event_stage_results.StageID
            LEFT JOIN events
            ON events.EventID = event_stage.EventID
            WHERE Position=1
            ORDER BY TeamName, LastName, Firstname'''
    connection.execute(sql)
    goldMembers = connection.fetchall()
    # get silver medal winners information from database
    sql = '''SELECT members.MemberID, FirstName, LastName, TeamName, EventName, Sport, StageDate, Location, PointsScored
            FROM event_stage_results
            LEFT JOIN members
            ON members.MemberID = event_stage_results.MemberID
            LEFT JOIN teams
            ON teams.TeamID = members.TeamID
            LEFT JOIN event_stage
            ON event_stage.StageID = event_stage_results.StageID
            LEFT JOIN events
            ON events.EventID = event_stage.EventID
            WHERE Position=2
            ORDER BY TeamName, LastName, Firstname'''
    connection.execute(sql)
    silverMembers = connection.fetchall()
    # get bronze medal winners information from database
    sql = '''SELECT members.MemberID, FirstName, LastName, TeamName, EventName, Sport, StageDate, Location, PointsScored
            FROM event_stage_results
            LEFT JOIN members
            ON members.MemberID = event_stage_results.MemberID
            LEFT JOIN teams
            ON teams.TeamID = members.TeamID
            LEFT JOIN event_stage
            ON event_stage.StageID = event_stage_results.StageID
            LEFT JOIN events
            ON events.EventID = event_stage.EventID
            WHERE Position=3
            ORDER BY TeamName, LastName, Firstname'''
    connection.execute(sql)
    bronzeMembers = connection.fetchall()
    # print the report
    return render_template("showMedals.html", numOfMedals=numOfMedals, numOfGold=numOfGold, numOfSilver=numOfSilver, numOfBronze=numOfBronze, goldMembers=goldMembers, silverMembers=silverMembers, bronzeMembers=bronzeMembers)

# this page shows the member reports
@app.route("/admin/show-members")
def showMembers():
    return redirect("/admin/members")