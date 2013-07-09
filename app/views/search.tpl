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
    <li> {{" | ".join(map(str, quote))}} </li>
    %end
%else:
    <h1> No Matches! </h1>
%end
 </ul>
 </body>
</html>

