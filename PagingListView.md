## Description ##
Paging in Appengine Admin list view works out of the box. Links to first, last, previous and next pages are displayed at the bottom of the page.
You can tune the number of displayed items per page by changing `appengine_admin.ADMIN_ITEMS_PER_PAGE` setting.

Example:
```
# Enlarge number of items per page.
import appengine_admin
appengine_admin.ADMIN_ITEMS_PER_PAGE = 100
```

## Google App Engine limitations ##
Using current implementation of paging it is not possible to access more than 1000 records per model. This [limitation](http://code.google.com/appengine/docs/datastore/queryclass.html#Query_fetch) is set by Google App Engine.