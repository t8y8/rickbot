<html>
 <head>
  <title>
  List Page
  </title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
 </head>
 <body>
 <h2> All Quotes </h2>
 <ul>
%for quote in list_of_quotes:
    <li> {{"{} | {} | {}".format(quote[0], quote[1], quote[2])}} </li>
%end
 </ul>
 </body>
</html>

