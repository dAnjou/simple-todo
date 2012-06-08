<ul>
    %for l in lists:
        <li>
            <a href="/{{ l['_id'] }}/">{{ l['_id'] }}</a>
        </li>
    %end
</ul>