#!/bin/ksh
. ls
#. cgi-lib.ksh # Read special functions to help parse ReadParse
PrintHeader
print -r -- "${Cgi.comment}" | /bin/mailx -s "COMMENT" kornj
print "<H2>You submitted the comment</H2>" print "<pre>"
print -r -- "${Cgi.comment}"
print "</pre>"