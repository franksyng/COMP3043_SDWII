#!C:\Users\frank\AppData\Local\Programs\Python\Python37\python.exe
import cgi
import cgitb

form = cgi.FieldStorage()

# Fetch username text
username = form.getvalue('uname')

# Skills checkbox
if form.getvalue('wd'):
    wdFlag = "Web Design"
else:
    wdFlag = ""
if form.getvalue('java'):
    javaFlag = "Java"
else:
    javaFlag = ""
if form.getvalue('db'):
    dbFlag = "Database"
else:
    dbFlag = ""

# Cities radio
if form.getvalue('city'):
    city = form.getvalue('city')
else:
    city = ""

# Working experience textarea
if form.getvalue('workexp'):
    workexp = form.getvalue('workexp')
else:
    workexp = ""

# Recent job select multiple
if form.getvalue('jobs'):
    jobs = form.getvalue('jobs')
    if type(jobs) == str:
        jobList = jobs
    else:
        jobList = ""
        for i in range(len(jobs)):
            jobList = jobList + jobs[i] + " "

# Position select
if form.getvalue('position'):
    position = form.getvalue('position')
else:
    position = "No position selected"

if form.getvalue('uploadFile'):
    file = form.getvalue('uploadFile')
else:
    file = "No file uploaded"

print("Content-type:text/html")
print()
print("<html>")
print("<head>")
print("<meta charset=\"utf-8\">")
print("<title>Candidates Info.</title>")
print("</head>")
print("<body>")
print("<h2>%s</h2>" % username)
print("<h2>Your current skills: %s %s %s</h2>" % (wdFlag, javaFlag, dbFlag))
print("<h2>Your city expected: %s </h2>" % city)
print("<h2>You have %s as experience</h2>" % workexp)
print("<h2>Your recent job(s): ")
print(jobList)
print("</h2>")
print("<h2>Your position selected: %s" % position)
print("<h2>Your file uploaded: %s" % file)
print("</body>")
print("</html>")

