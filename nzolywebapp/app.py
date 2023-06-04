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

@app.route("/<name>")
def athleteinterface(name):
    connection = getCursor()
#    upcoming = """SELECT EventName, StageDate, StageName, Location 
#           FROM events JOIN event_stage 
#            ON events.EventID = event_stage.EventID 
#            JOIN event_stage_results 
#            ON event_stage_results.StageID = event_stage.StageID 
#            JOIN members 
#            ON members.MemberID = event_stage_results.MemberID 
#            WHERE PointsScored >= PointsToQualify AND FirstName = "Zoi";"""
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
    return render_template("athleteinterface.html", name = name, athleteinfo = athleteInfo)

@app.route("/admin")
def admin():
    return render_template("admin.html")