<html>
 <head>
  <title>
  List Page
  </title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
 </head>
 <body>
<ul>
%mklink = lambda url, id: "http://{}/quote/{}".format(url, id)
%link_url = req_url
<ul>
%for person in people:
	<h2> {{ person }} </h2>
	%for quote in list_of_quotes:
		%if quote.person_id.name == person:
    <li> 
<a href={{ mklink(link_url, quote.id) }} > {{ "{} {} {}".format(quote.id, quote.text, quote.person_id.name)}}</a>
    </li>
		%end
	%end
%end
 </ul>

</body>
</html>
