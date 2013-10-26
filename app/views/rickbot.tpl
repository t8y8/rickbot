<html>
<head>
    <title>Rickbot</title>
    <link rel="stylesheet" href="/static/style.css" />
</head>

<body>
<div id="wrapper">
    <div id="Rickbot">
        <div id="RickHead">
            <a href="/"><img class="Rick" src="/static/{{ name.lower() }}.jpg" height="480" width="360" /></a>
            <div id="Title">
                <table>
                    <tr>
                        <td>
                            <h1>Rickbot 3.6</h1>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div id="SpeechBubble">
            <img src="/static/speech-bubble.jpg" height="477" width="633" />
        </div>
            <div id="Quote">
                <table>
                    <tr>
                        <td>
                            <h2>{{ rickquote.text }}</h2>
                        </td>
                    </tr>
                </table>
            </h2>
        </div>
    </div>
<div class=clear>&nbsp;</div>
    <div id="QuoteSubmit">
        <div id="SubmitText">
            <table>
                <tr>
                    <td>
                        <form method="POST" action="/quote" accept-charset="UTF-8">
                            <h2>What did you hear
                            <select name="person">
                            % for person in persons:
                                <option value="{{ person }}"> {{ person }} </option>\\
                            % end
                            </select> say?</h2>
                        <input type="text" class="text" name="saying">
                        <input type="submit" value="Submit">
                        </form>
                    </td>
                </tr>
            </table>
        </div>
    </div>
<div class=clear>&nbsp;</div>
% root_url = "{}://{}".format(*shareme[:2])
% share_url = "{}/quote/{}".format(root_url, rickquote.id)
% list_url = root_url + "/list" 
    <div id="Awesomeness">Powered by Awesomeness <sup>®</sup> | Share this quote: <a href="{{ share_url  }}">{{ share_url }}</a> | <a href="{{ list_url }}"> List All </a> </div>
</div>
</body>
</html>
