<!DOCTYPE html>
<html>
    <head>
        <title>TODO</title>
        <link rel="stylesheet" href="/static/foundation/stylesheets/foundation.css">
        <link rel="stylesheet" href="/static/foundation/stylesheets/app.css">
        <!--[if lt IE 9]>
            <link rel="stylesheet" href="/static/foundation/stylesheets/ie.css">
        <![endif]-->
        <link href="/static/css/style.css" type="text/css" rel="stylesheet">
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
        <script src="/static/foundation/javascripts/modernizr.foundation.js"></script>
    </head>
    <body>
        <div class="container">
            <div class="row">
                <div class="six columns centered">
                    <form class="nice" method="post" name="add" id="add" action="/add">
                        <input class="expand input-text" type="text" name="todo" id="todo" placeholder="TODO"/>
                    </form>
                </div>
            </div>
            <div class="row">
                <div class="six columns centered">
                    %for t in todos:
                    <div class="alert-box">
                        {{ t.todo }}
                        <a href="#" class="delete" id="todo-{{ t.id }}">&times;</a>
                    </div>
                    %end
                    </ul>
                </div>
            </div>
        </div>
        <script src="/static/js/jquery-1.7.2.min.js"></script>
        <script src="/static/foundation/javascripts/foundation.js"></script>
        <script src="/static/foundation/javascripts/app.js"></script>
        <script>
        $(document).ready(function(){
            $("#todo").focus();  
            $('a.delete').click(function(){
                var $this = $(this);
                $.post('/delete', { todo_id: $this.attr('id') }, function(data) {
                    $this.parent().fadeOut();
                })
                .error(function() { alert("Shit, something failed!"); });
            });
        });
        </script>
    </body>
</html>
