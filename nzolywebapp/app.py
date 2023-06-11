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

@app.route("/")
def home():
    return render_template("base.html")

@app.route("/listmembers")
def listmembers():
    connection = getCursor()
    connection.execute("SELECT members.MemberID, teams.TeamName, members.FirstName, members.LastName, members.City, members.Birthdate FROM members JOIN teams on members.TeamID = teams.TeamID;")
    memberList = connection.fetchall()
    # print(memberList)
    return render_template("memberlist.html", memberlist = memberList)


@app.route("/listevents")
def listevents():
    connection = getCursor()
    connection.execute("SELECT * FROM events;")
    eventList = connection.fetchall()
    return render_template("eventlist.html", eventlist = eventList)


@app.route("/listmembers/<name>")
def athleteinterface(name):
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
    return render_template("athleteinterface.html", name = name, upcomingevents = upcomingevents, previousresult = previousresult)

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/admin/listmembers")
def adminlistmembers():
    connection = getCursor()
    connection.execute("SELECT members.MemberID, teams.TeamName, members.FirstName, members.LastName, members.City, members.Birthdate FROM members JOIN teams on members.TeamID = teams.TeamID;")
    memberList = connection.fetchall()
    # print(memberList)
    return render_template("adminmemberlist.html", memberlist = memberList)


@app.route("/admin/listevents")
def adminlistevents():
    connection = getCursor()
    connection.execute("SELECT EventID, EventName, Sport, TeamName, NZTeam FROM events LEFT JOIN teams ON events.NZTeam = teams.TeamID;")
    eventList = connection.fetchall()
    return render_template("admineventlist.html", eventlist = eventList)

@app.route("/admin/liststages")
def liststages():
    connection = getCursor()
    connection.execute("SELECT event_stage.EventID, EventName, StageID, StageName, Location, StageDate, Qualifying, PointsToQualify FROM event_stage LEFT JOIN events ON event_stage.EventID = events.EventID;")
    stageList = connection.fetchall()
    return render_template("stagelist.html", stagelist = stageList)

@app.route("/admin/search")
def search():
    return render_template("search.html")

@app.route("/admin/results", methods = ['get'])
def results():
    name=request.args.get('searchinfo')
    str = name.split()
    memberResults = list()
    eventResults = list()
    connection = getCursor()
    for item in str:
        sql1 = """SELECT * 
                FROM members 
                WHERE members.FirstName LIKE %s OR members.LastName LIKE %s;"""
        parameters = (f"%{item}%")
        connection.execute(sql1, (parameters, parameters))
        memberResults.extend(connection.fetchall())
        memberResults = list(set(memberResults))
        sql2 = """SELECT *
                FROM events
                WHERE events.EventName LIKE %s;"""
        connection.execute(sql2, (parameters,))
        eventResults.extend(connection.fetchall())
        eventResults = list(set(eventResults))
    return render_template("results.html", name = name, memberresults = memberResults, eventresults = eventResults)

        
        
@app.route("/admin/addmembers")
def addmembers():
    connection = getCursor()
    sql = """SELECT * FROM teams;"""
    connection.execute(sql)
    team = connection.fetchall()
    return render_template("addmembers.html", team = team)

@app.route("/admin/members/add", methods=["POST"])
def membersadd():
    connection = getCursor()
    teamid = request.form.get('team')
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    city = request.form.get('city')
    birthdate = request.form.get('birthdate')
    sql = "INSERT INTO members (TeamID, FirstName, LastName, City, Birthdate) VALUES (%s, %s, %s, %s, %s);"
    parameters = (teamid, firstname, lastname, city, birthdate)
    connection.execute(sql, parameters)
    return redirect("/admin/listmembers")

@app.route("/admin/members/edit/<memberid>")
def editmember(memberid):
    connection = getCursor()
    sql = "SELECT * FROM teams;"
    connection.execute(sql)
    team = connection.fetchall()
    sql = "SELECT * FROM members WHERE MemberID = %s;"
    parameters = (memberid,)
    connection.execute(sql, parameters)
    membertoedit = connection.fetchone()
    return render_template("editmember.html", membertoedit=membertoedit, team = team)

@app.route("/admin/updatemembers", methods=["POST"])
def updatemember():
    teamid = request.form.get('team')
    memberid = int(request.form.get('memberid'))
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    city = request.form.get('city')
    birthdate = request.form.get('birthdate')
    sql = '''UPDATE members 
            SET TeamID = %s, FirstName = %s, LastName = %s, City = %s, Birthdate= %s
            WHERE MemberID = %s;'''
    parameters = (teamid, firstname, lastname, city, birthdate, memberid)
    connection = getCursor()
    connection.execute(sql, parameters)
    return redirect("/admin/listmembers")

@app.route("/admin/addevents")
def addevents():
    connection = getCursor()
    sql = """SELECT * FROM teams;"""
    connection.execute(sql)
    team = connection.fetchall()
    return render_template("addevents.html", team=team)

@app.route("/admin/event/add", methods = ['POST'])
def eventadd():
    connection = getCursor()
    teamid = request.form.get('team')
    eventname = request.form.get('eventname')
    sport = request.form.get('sport')
    sql = "INSERT INTO events (EventName, Sport, NZTeam) VALUES (%s, %s, %s);"
    parameters = (eventname, sport, teamid)
    connection.execute(sql, parameters)
    return redirect("/admin/listevents")

@app.route("/admin/addstages")
def addstages():
    connection = getCursor()
    sql = """SELECT DISTINCT events.EventID, EventName
            FROM events
            LEFT JOIN event_stage
            ON event_stage.EventID = events.EventID
            WHERE events.EventID NOT IN (SELECT EventID FROM event_stage WHERE event_stage.Qualifying = 0);"""
    connection.execute(sql)
    event = connection.fetchall()
    return render_template("addstages.html", event=event)

@app.route("/admin/stage/add", methods = ['POST'])
def stageadd():
    eventid = request.form.get('event')
    stagename = request.form.get('stagename').lower()
    location = request.form.get('location')
    stagedate = request.form.get('stagedate')
    pointstoqualify = request.form.get('pointstoquality')
    if stagename == 'final':
        qualifying = 0 
        pointstoqualify = None
    else:
        qualifying = 1
        if pointstoqualify == "":
            pointstoqualify = 0
    sql = "INSERT INTO event_stage (StageName, EventID, Location, StageDate, Qualifying, PointsToQualify) VALUES (%s, %s, %s, %s, %s, %s);"
    parameters = (stagename.title(), eventid, location.title(), stagedate, qualifying, pointstoqualify)
    connection = getCursor()
    connection.execute(sql, parameters)
    return redirect("/admin/liststages")


@app.route("/admin/addscores")
def addscores():
    connection = getCursor()
    sql = '''SELECT *
            FROM event_stage
            LEFT JOIN events
            ON event_stage.EventID = events.EventID 
            WHERE StageID NOT IN (SELECT event_stage_results.StageID FROM event_stage_results WHERE PointsScored IS NOT NULL);'''  
    connection.execute(sql)
    stage = connection.fetchall()
    connection.execute("SELECT * FROM members;")
    member = connection.fetchall()
    return render_template("addscores.html", stage = stage, member=member)

@app.route("/admin/score/add", methods = ['POST'])
def scoreadd():
    stageid = request.form.get('stage')
    memberid = request.form.get('member')
    pointsscored = request.form.get('pointsscored')
    position = request.form.get('position')
    if position == "" or position == "0":
        position = None
    sql = "SELECT StageName FROM event_stage WHERE event_stage.StageID = %s"
    connection = getCursor()
    connection.execute(sql, (stageid,))
    stagename = connection.fetchone()[0]
    if (stagename.lower() == "final" and position == None) or (stagename.lower() != "final" and position != None):
        return render_template("addscores.html", stageid=stageid, memberid=memberid, pointsscored=pointsscored)
    else:
        sql = "INSERT INTO event_stage_results (StageID, MemberID, PointsScored, Position) VALUES (%s, %s, %s, %s);"
        parameters = (stageid, memberid, pointsscored, position)
        connection.execute(sql, parameters)
        return redirect("/admin/listscores")

@app.route("/admin/listscores")
def listscores():
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
    return render_template("listscores.html", scorelist = scorelist)

@app.route("/admin/showmedals")
def showmedals():
    connection = getCursor()
    connection.execute("SELECT COUNT(Position) FROM event_stage_results WHERE Position > 0 AND Position < 4;")
    num_medals = connection.fetchall()
    connection.execute("SELECT COUNT(Position) FROM event_stage_results WHERE Position=1")
    num_gold = connection.fetchall()
    connection.execute("SELECT COUNT(Position) FROM event_stage_results WHERE Position=2")
    num_silver = connection.fetchall()
    connection.execute("SELECT COUNT(Position) FROM event_stage_results WHERE Position=3")
    num_bronze = connection.fetchall()
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
    return render_template("showmedals.html", num_medals=num_medals, num_gold=num_gold, num_silver=num_silver, num_bronze=num_bronze, gold_members=gold_members, silver_members=silver_members, bronze_members=bronze_members)
