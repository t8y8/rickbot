<html>
 <head>
  <title>
  List Page
  </title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
 </head>
 <body>
%mklink = lambda url, id: "http://{}/quote/{}".format(url, id)
%link_url =  req_url
<ul>
%for quote in list_of_quotes:
    <li> 
        <a href={{ "{}".format(mklink(link_url, quote[0])) }} > {{ quote[0] }}</a> {{"| {} | {}".format(quote[1], quote[2]) }}
%end
 </ul>

</body>
</html>
