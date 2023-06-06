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
    upcomingEvents = """SELECT EventName, StageDate, StageName, Location 
                        FROM events 
                        LEFT JOIN event_stage
                        ON events.EventID = event_stage.EventID
                        LEFT JOIN teams
                        ON teams.TeamID = events.NZTeam
                        LEFT JOIN members
                        ON teams.TeamID = members.TeamID
                        WHERE (StageID IS NULL OR StageID NOT IN (SELECT event_stage_results.StageID FROM event_stage_results)) AND members.FirstName = %s"""
    previousResults = """SELECT EventName, StageDate, StageName, Location, PointsScored
                        FROM event_stage_results
                        LEFT JOIN members
                        ON members.MemberID = event_stage_results.MemberID
                        LEFT JOIN event_stage
                        ON event_stage.StageID = event_stage_results.StageID
                        LEFT JOIN events
                        ON events.EventID = event_stage.EventID
                        Where FirstName = %s"""
    parameters = (name,)
    connection.execute(previousResults, parameters)
    athleteInfo = connection.fetchall()
    connection.execute(upcomingEvents, parameters)
    eventInfo = connection.fetchall()
    return render_template("athleteinterface.html", name = name, athleteinfo = athleteInfo, eventinfo = eventInfo)

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
    connection.execute("SELECT * FROM events;")
    eventList = connection.fetchall()
    return render_template("admineventlist.html", eventlist = eventList)

@app.route("/admin/results")
def search():
    name=request.args['searchinfo']
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
    sql = """SELECT TeamID FROM teams;"""
    connection.execute(sql)
    teamID = connection.fetchall()
    return render_template("addmembers.html", teamid = teamID)

@app.route("/admin/members/add", methods=["POST"])
def membersadd():
    memberid = request.form.get('memberid')
    teamid = request.form.get('teamid')
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    city = request.form.get('city')
    birthdate = request.form.get('birthdate')
    sql = "INSERT INTO members VALUES (%s, %s, %s, %s, %s, %s);"
    parameters = (memberid, teamid, firstname, lastname, city, birthdate)
    connection = getCursor()
    connection.execute(sql, parameters)
    return redirect("/admin/listmembers")

@app.route("/admin/members/edit/<memberid>")
def editmember(memberid):
    connection = getCursor()
    sql = "SELECT * FROM members WHERE MemberID = %s;"
    parameters = (memberid,)
    connection.execute(sql, parameters)
    membertoedit = connection.fetchone()
    sql = "SELECT TeamID FROM teams;"
    connection.execute(sql)
    teamid = connection.fetchall()
    return render_template("editmember.html", membertoedit=membertoedit, teamid = teamid)

@app.route("/admin/updatemembers", methods=["POST"])
def updatemember():
    memberid = request.form.get('memberid')
    teamid = request.form.get('teamid')
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
    sql = """SELECT TeamID FROM teams;"""
    connection.execute(sql)
    teamID = connection.fetchall()
    return render_template("addevents.html", teamid=teamID)

@app.route("/admin/event/add", methods = ['POST'])
def eventadd():
    eventid = request.form.get('eventid')
    eventname = request.form.get('eventname')
    sport = request.form.get('sport')
    teamid = request.form.get('teamid')
    sql = "INSERT INTO events VALUES (%s, %s, %s, %s);"
    parameters = (eventid, eventname, sport, teamid)
    connection = getCursor()
    connection.execute(sql, parameters)
    return redirect("/admin/listevents")

@app.route("/admin/addeventstage")
def addeventstages():
    connection = getCursor()
    sql = """SELECT EventID FROM events;"""
    connection.execute(sql)
    eventID = connection.fetchall()
    return render_template("addeventstage.html", eventid=eventID)

@app.route("/admin/eventstage/add/")
def eventstageadd():
    stageid = request.form.get('stageid')
    stagename = request.form.get('stagename')
    eventid = request.form.get('eventid')
    location = request.form.get('location')
    stagedate = request.form.get('stagedate')
    qualifying = request.form.get('qualifying')
    pointstoqualify = request.form.get('pointstoqualify')
    sql = "INSERT INTO events VALUES (%s, %s, %s, %s, %s, %s, %s);"
    parameters = (stageid, stagename, eventid, location, stagedate, qualifying, pointstoqualify)
    connection = getCursor()
    connection.execute(sql, parameters)
    return redirect("/admin/listeventstages.html")


@app.route("/admin/addscores", methods = ['POST'])
def addscores():
    return None

@app.route("/admin/showreports", methods = ['POST'])
def showreports():
    return None