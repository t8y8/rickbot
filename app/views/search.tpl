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
    <li> {{ "{} {} {}".format(quote.id, quote.text, quote.person_id.name)}}</li>
    %end
%elif searchbox:
	<h2> Please enter a search term: </h2>
	<form method="GET" action="/search" accept-charset="UTF-8">
	<input type="text" class="text" name="keyword">
	<input type="submit" value="Go">
%else:
    <h1> No Matches! </h1>
%end
 </ul>
 </body>
</html>

