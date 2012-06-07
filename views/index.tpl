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
                        <div class="input row">
                            <div class="eleven columns">
                                <input class="expand input-text" type="text" name="title" id="todo" placeholder="TODO"/>
                            </div>
                            <div class="no-margin columns">
                                <a href="#" id="settings" class="white small radius button"><img src="/static/glyphicons/png/glyphicons_280_settings.png"></a>
                            </div>
                        </div>
                        <div class="priority row">
                            <div class="four columns">
                                <label class="blue"><input type="radio" name="priority" value="lazy"><span class="blue radius label">lazy</span></label>
                            </div>
                            <div class="four columns">
                                <label class="red"><input type="radio" name="priority" value="soon"><span class="red radius label">soon</span></label>
                            </div>
                            <div class="four columns">
                                <label class="black"><input type="radio" name="priority" value="now"><span class="black radius label">now</span></label>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
            <div class="row">
                <div class="six columns centered">
                    <ul>
                        %for t in todos:
                            <li>
                                <div class="alert-box">
                                    %if t.priority == 'lazy':
                                        <span class="blue radius label">lazy</span>
                                    %end
                                    %if t.priority == 'soon':
                                        <span class="red radius label">soon</span>
                                    %end
                                    %if t.priority == 'now':
                                        <span class="black radius label">now</span>
                                    %end
                                    {{ t.title }}
                                    <a href="#" class="delete" id="todo-{{ t.id }}">&times;</a>
                                </div>
                            </li>
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
            $('a#settings').click(function(){
                $('div.priority.row').toggle();
            })
        });
        </script>
    </body>
</html>
