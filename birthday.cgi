#!/usr/bin/python
import cgi
import cgitb

form = cgi.FieldStorage()
if "birthday" not in form:
    print "<H1>Error</H1>"
    print "Please fill in the name and addr fields."
else:
  bday = form['birthday'].value
  # Print header
  print 'Content-Type: text/html'
  print
  # Your HTML body
  print "Your birthday is %s.\n" % bday