<html>
 <head>
  <title>
  List Page
  </title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
 </head>
 <body>
 <ul>
%for quote in list_of_quotes:
    <li> {{"{} | {} | {}".format(quote[0], quote[1], quote[2])}}
%end
 </ul>
 </body>
</html>

