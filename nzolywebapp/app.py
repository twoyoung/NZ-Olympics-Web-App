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
def abc():
    return render_template("admin.html") 

#@app.route("/admin")
#def adminpage():
#    return render_template("admin.html")


#@app.route("/admin/<str>", methods=["GET", "POST"])
#def admin(str):
#    if not str:
#        return render_template("admin.html")
#    else:
#        request.method == "POST"
#        name = request.form.get("str")
#        sql = """SELECT * FROM members WHERE members.FirstName LIKE '%'+%s+'%' OR members.LastName LIKE '%'+%s+'%';"""
#        parameters = (name,)
#        connection.execute(sql, parameters)
#        searchResults = connection.fetchall()
#        return render_template("searchinfo.html", athlete = name, searchresults = searchResults)
        
        
