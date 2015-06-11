# Quick start #
The usage is as simple as this:
  1. Check out Appengine Admin via SVN:
```
svn checkout http://appengine-admin.googlecode.com/svn/trunk/ appengine_admin
```
  1. Put it into your GAE application root directory
  1. Modify your application to include admin page URL's:
```
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import appengine_admin

application = webapp.WSGIApplication([
    ...
    # Admin pages
    (r'^(/admin)(.*)$', appengine_admin.Admin),
    ...
])

...

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()

```
  1. Register your data models with admin site:
```
from google.appengine.ext import db
import appengine_admin

## Sample models ##
class Article(db.Model):
    title = db.StringProperty("Title", required = True)
    content = db.TextProperty("Content", required = True)
    whencreated = db.DateTimeProperty("Created", auto_now_add = True)
    whenupdated = db.DateTimeProperty("Updated", auto_now = True)

    def __str__(self):
        return str(self.title)

class Comment(db.Model):
    article = db.ReferenceProperty(Article, verbose_name = "Article")
    author = db.StringProperty("Author", required = True)
    content = db.TextProperty("Content", required = True)
    whencreated = db.DateTimeProperty("Created", auto_now_add = True)
    whenupdated = db.DateTimeProperty("Updated", auto_now = True)

## Admin views ##
class AdminArticle(appengine_admin.ModelAdmin):
    model = Article
    listFields = ('title', 'whencreated', 'whenupdated')
    editFields = ('title', 'content')
    readonlyFields = ('whencreated', 'whenupdated')

class AdminComment(appengine_admin.ModelAdmin):
    model = Comment
    listFields = ('article', 'author', 'whencreated', 'whenupdated')
    editFields = ('article', 'author', 'content')
    readonlyFields = ('whencreated', 'whenupdated')

# Register to admin site
appengine_admin.register(AdminArticle, AdminComment)

```
  1. Make available Appengine Admin static files by  adding these lines to your app.yaml
```
- url: /appengine_admin_media
  static_dir: appengine_admin/media
  secure: never
```
  1. That's it! Now refresh http://localhost:8080/admin/ and give Appengine Admin a try!