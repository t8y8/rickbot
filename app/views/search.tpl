<html>
 <head>
  <title>
  Search Page
  </title>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
 </head>
 <body>
 <ul>

%if search_results:
    <h2> Search Results: </h2>
    %for quote in search_results:
    <li> {{"{} | {} | {}".format(quote[0], quote[1], quote[2])}}
    %end
%else:
    <h1> There were no matches found for that term. </h1>
%end
 </ul>
 </body>
</html>

