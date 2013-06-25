<html>
<head>
    <title>Rickbot</title>
    <link rel="stylesheet" href="/static/style.css" />
</head>

<body>
<div id="wrapper">
    <div id="Rickbot">
        <div id="RickHead">
            <a href="/"><img class="Rick" src="/static/rick-f.jpg" height="480" width="360" /></a>
            <div id="Title">
                <table>
                    <tr>
                        <td>
                            <h1>Rickbot 3.5</h1>
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
                            <h2>{{rickquote}}</h2>
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
                        <h2>What did you hear Rick say?</h2>
                    </td>
                </tr>
            </table>
        </div>
        <div id="SubmitForm">
            <table>
                <tr>
                    <td>
                        <form method="POST" action="/quote" accept-charset="UTF-8">
                        <input type="text" class="text" name="saying">
                        <input type="submit" value="Said Rick">
                        </form>
                    </td>
                </tr>
            </table>
        </div>
    </div>
<div class=clear>&nbsp;</div>
    <div id="Awesomeness">Powered by Awesomeness <sup>®</sup> | Share this quote: <a href="{{shareme}}">{{shareme2}}</a> </div>
</div>
</body>
</html>
