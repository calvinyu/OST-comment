#!/usr/bin/python 
import cgi
import cgitb
import subprocess
import os, urllib
import random
import numpy
from urllib2 import quote
from urllib2 import unquote
cgitb.enable()
#parsing query string
form = cgi.FieldStorage()

print "Content-type: text/html\n\n";
print "<html>"
print "<head>"
print "   <title>OST Question App</title>"
print "</head>\n";
print "<br>"
print "<body>\n";

path = "./ost-hw4.cgi"
def issueCommand(command):
  p = subprocess.Popen(['/bin/bash', '-c', command], 
  #stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  stdout=subprocess.PIPE)
  return urllib.unquote(p.stdout.read())
def issueCommandWithArg(command):
  p = subprocess.Popen(['/bin/bash', '-c']+command, 
  #stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  stdout=subprocess.PIPE)
  return urllib.unquote(p.stdout.read())
def display(output):
  print output.replace('\n', '<br>')
def createUrl(args, display):
  return "<a href="+path+"?"+args+">"+display+"</a>"
def encodeUrl(url):
  return quote(url, safe="%/:=&?~#+!$,;'@()*[]")
#List all
if "option" not in form:
  print "<span>\nThis is Main Page<br>"
  command = "./question list"
  output = issueCommand(command)
  qs = (output.split("\n"))[:-1]
  #print qs
  print "<ul>"
  for q in qs:
    url=path+"?option=view&u="+(q.split('/'))[0]+"&q="+(q.split('/'))[1]
    url=quote(url, safe="%/:=&?~#+!$,;'@()*[]")
    #url=quote(url.encode('utf-8  '))
    print "<li><a href="+url+">"+q+"</a><br></li>"
  print "</ul>"
  print "<a href="+path+"?option=create>Create a new question</a><br>"
else:
  print createUrl('', "Back to Main Page")
  print "<br>"
  option = form['option'].value
  #view
  if option == 'view':
    u = form['u'].value
    u = unquote(u)
    q = form['q'].value
    q = unquote(q)
    #print 'viewing<br>' + 'User: ' + u + '<br>Question: ' + q + '<br>'
    command = "./question view \"" + u +"/" + q +"\""
    output = issueCommand(command)
    outputArray = output.split('====')
    #print Question
    print outputArray[0].replace('\n','<br>')
    print createUrl("option=vote&u="+u+"&q="+encodeUrl(q)+"&vote=up","UP")
    print " "
    print createUrl("option=vote&u="+u+"&q="+encodeUrl(q)+"&vote=down","DOWN")
    print "<br>----------------------------------------------------------------------------<br>"
    answerDisplay = []
    answerScore = []
    for i in range(1,len(outputArray)):
      #
      #score vu/va
      #content
      lines = outputArray[i].split('\n')
      line2 = lines[1].split(' ')
      score = line2[0]
      vuva = line2[1].split('/')
      vu = vuva[0]
      va = lines[1][len(score)+len(vu)+2:]
      answerCotent = ''
      for index in range(2,len(lines)-1):
        answerCotent =answerCotent +  '<br>' + lines[index]
      display =  "<tr><td  style=\"word-wrap: break-word\">" + answerCotent + "</td><td>" + score +"</td><td>"
      display += createUrl("option=vote&u="+u+"&q="+encodeUrl(q)+"&vu="+vu+"&va="+encodeUrl(va)+"&vote=up","UP")
      display += " "
      display += createUrl("option=vote&u="+u+"&q="+encodeUrl(q)+"&vu="+vu+"&va="+encodeUrl(va)+"&vote=down","DOWN")
      display += "</td></tr>"
      answerDisplay.append(display)
      answerScore.append(int(score))
    #sort answers and print
    index = numpy.argsort(answerScore)
    print "<table width=400>"
    for i in range(len(answerDisplay)-1, -1, -1):
      print answerDisplay[index[i]]
    print "</table>"
    #print answer question
    print createUrl("option=answer&u="+u+"&q="+encodeUrl(q),"Add an answer")    
  #list
  elif option == 'list':
    print "list"
  #create
  elif option =='create':
    if "qn" not in form:
      print """\
      <form action = %s method=POST>
      What's your question? <br>
      <textarea rows="4" cols="50" name=qc></textarea><br>
      %s
      <input type=submit value=\"Ask This Question\">
      <input type=hidden name=option value=create>
      <input type=hidden name=qn value=%s><br><br>
      </form>
      """ % (path, createUrl("",'Cancel'), random.randrange(99999999,999999999))
    else:
      print "Question submitted"
      command = "./question create \"" + form['qn'].value.replace('+',' ') + "\" \"" + form['qc'].value.replace('+',' ') +"\""
      display(command)
      output = issueCommand(command)
      display(output)
  #vote
  elif option == 'vote':
    u = form['u'].value;
    u = unquote(u)
    q = form['q'].value;
    q = unquote(q)
    vote = form['vote'].value;
    command = "./question vote " + vote + " " + u + "/\"" + q + "\""
    if "vu" in form:
      #vote for answer
      vu = form['vu'].value;
      va = form['va'].value;
      command = command + " " +vu + "/\"" + va + "\"" 
    output = issueCommand(command)
    print output
  elif option == 'answer':
    u = form['u'].value;
    u = unquote(u)
    q = form['q'].value;
    q = unquote(q)
    if "an" not in form:
      print """\
      <form action = %s method=POST>
      <input type=hidden name=option value=answer>
      Your answer: <br>
      <textarea rows="4" cols="50" name=ac></textarea><br>
      %s
      <input type=submit value=\"Add this Answer\">
      <input type=hidden name=u value=%s>
      <input type=hidden name=q value=%s>
      <input type=hidden name=an value=%s><br><br>
      </form>
      """ % (path,createUrl("option=view&u="+u+"&q="+encodeUrl(q),'Cancel'), encodeUrl(u), encodeUrl(q), random.randrange(999999999,9999999999))
    else:
      an = form['an'].value
      an = unquote(an)
      ac = form['ac'].value
      ac = unquote(ac)
      command = "./question answer " + u +"/\"" + q + "\" \"" + an + "\" \"" + ac + "\""
      output = issueCommand(command)
      if output == "":
        print "Your answer has been posted!"
      else:
        print output + "Failed! Please check again!"



print '<FORM><INPUT Type="button" VALUE="Back" onClick="history.go(-1);return true;"></FORM>'
print "</body></html>\n";

#command_array = command_content.split("+")

#command = "./question " + command_content.replace('+', ' ')
#command = "echo /Users/yuyuchih"
#p = subprocess.Popen(['/bin/bash', '-c', command], 
#stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#output = urllib.unquote(p.stdout.read())

