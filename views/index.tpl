<!DOCTYPE html>
<html>
	<head>
		<title>TODO</title>
	</head>
	<body>
		<form method="post" name="add" id="add" action="/add">
			<dl>
				<dt>
					<label for="todo">Todo:</label>
				</dt>
				<dd><input type="text" name="todo" id="todo" /></dd>
			</dl>
			<div id="submit_buttons">
				<button type="submit">Submit</button>
			</div>
		</form>
		<form method="post" name="delete" id="delete" action="/delete">
			<ul>
			%for t in todos:
			    <li><input type="hidden" value="{{ t.id }}"><button type="submit">X</button>{{ t.li }}!</todo>
			%end
			</ul>
		</form>
	</body>
</html>
