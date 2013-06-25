<html>
 <head>
  <title>
  Search Page
  </title>
 </head>
 <body>
 <ul>

%if search_results:
    %for quote in search_results:
    <li> {{"{} | {} | {}".format(quote[0], quote[1], quote[2])}}
    %end
%else:
    <h1> No Matches! </h1>
%end
 </ul>
 </body>
</html>

