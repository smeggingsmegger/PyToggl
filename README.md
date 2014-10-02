PyToggl
=======

The definitive Toggl library for Python.
-------

Currently this library supports all API calls via the self.query and the self.query_report methods. They return the JSON that is documented in the Toggl API documentation.

In addition to the query methods, this library contains quite a few helpful methods and classes for working with Toggl data.

### How To Use / Examples

Initialize the Library
```python
from PyToggl import PyToggl
pytoggl = PyToggl('YOUR-API-KEY-HERE')

# Wasn't that easy?
```

Now do something with it.
```python
# Grab our workspace(s)
workspaces = pytoggl.get_workspaces()

# Now grab all our users for the first workspace
users = pytoggl.get_workspace_users(workspaces[0].id)

# PyToggl creates objects out of all your query results that use the
# helper methods (ie. get_workspaces and get_workspace_users)

print(users[0].name)
```

```
John Smith
```

```python
# The repr is very useful for debugging.
print(users[0])
```

```
class instance>.wid = 12345
class instance>.uid = 543210
class instance>.admin = False
class instance>.avatar_file_name = https://secure.gravatar.com/avatar/87vh8r7h8er7ch8wd7ch9wd7cj9wr7h?d=404&s=200
class instance>.id = 987656789
class instance>.inactive = False
class instance>.at = 2014-09-26T17:54:54+00:00
class instance>.active = True
class instance>.group_ids = [345678]
class instance>.email = johnsmith@notarealdomain.com
class instance>.name = John Smith
```

```python
# All objects have a dict property.
print(users[0].dict)
```

```
{'active': True,
'admin': False,
'at': u'2014-09-26T17:54:54+00:00',
'avatar_file_name': u'https://secure.gravatar.com/avatar/87vh8r7h8er7ch8wd7ch9wd7cj9wr7h?d=404&s=200',
'email': u'johnsmith@notarealdomain.com',
'group_ids': [345678],
'id': 987656789,
'inactive': False,
'name': u'John Smith',
'uid': 543210,
'wid': 12345}
```

```python
# All objects also have a json property

print(users[0].json)
```
```
'{"wid": 12345, "uid": 543210, "avatar_file_name": "https://secure.gravatar.com/avatar/87vh8r7h8er7ch8wd7ch9wd7cj9wr7h?d=404&s=200", "inactive": false, "at": "2014-09-26T17:54:54+00:00", "active": true, "id": 987656789, "group_ids": [345678], "name": "John Smith", "admin": false, "email": "johnsmith@notarealdomain.com"}'
```
