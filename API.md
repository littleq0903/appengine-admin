# Contents #


# Python package name #

To use Appengine Admin [check it out](http://code.google.com/p/appengine-admin/source/checkout) via [Subversion](http://subversion.tigris.org/) using `appengine_admin` as directory name.

Import Appengine Admin into your scripts:
```
import appengine_admin
```

# Compatibility #
Appengine Admin is compatible with Python 2.5 and more recent Python 2.x versions.

# Available objects #
Classes:
  * ModelAdmin
  * Admin
Functions:
  * register
  * getModelAdmin

# Classes #
## ModelAdmin ##
Use this class as base for your model registration to admin site.

Available settings:
  * model - `google.appengine.ext.db.model` derived class that describes your data model
  * listFields - list of field names that should be shown in list view
  * editFields - list of field names that that should be used as editable fields in admin interface
  * readonlyFields - list of field names that should be used as read-only fields in admin interface
  * listGql - GQL statement for record ordering/filtering/whatever\_else in list view
  * AdminForm - custom form (should be derived from django.forms.Form)

Sample usage:
```
from google.appengine.ext import db
import appengine_admin

class Article(db.Model):
    """Your data model
    """
    title = db.StringProperty("Title", required = True)
    content = db.TextProperty("Content", required = True)
    whencreated = db.DateTimeProperty("Created", auto_now_add = True)
    whenupdated = db.DateTimeProperty("Updated", auto_now = True)

class AdminArticle(appengine_admin.ModelAdmin):
    """Appengine Admin settings for the model
    """
    model = Article
    listFields = ('title', 'whencreated', 'whenupdated')
    editFields = ('title', 'content')
    readonlyFields = ('whencreated', 'whenupdated')
    listGql = 'order by whencreated desc'
```

## Admin ##
Use this class as view in your URL scheme definitions.
Admin class is derived from `google.appengine.ext.webapp.RequestHandler` so it contains every property and method that is available for `google.appengine.ext.webapp.RequestHandler`

Additional instance properties:
  * models - Aplphabetically sorted list of registered models
  * urlPrefix - URL prefix that is set for Appengine Admin urls, e.g. "/admin".
Additional methods:
  * index\_get
> Show Appengine Admin start page
  * new\_get
> Attribute: modelName

> Show form for creating new record of particular model
  * new\_post
> Attribute: modelName

> Create new record of particular model
  * edit\_get
> Attributes: modelName, key

> Show for for editing existing record of particular model.
  * edit\_post
> Attributes: modelName, key

> Save details for already existing record of particular model.
  * delete\_get
> Attributes: modelName, key

> Delete record of particular model.

Sample usage:
```
from google.appengine.ext import webapp

application = webapp.WSGIApplication([
    ...
    # Admin pages
    (r'^(/admin)(.*)$', appengine_admin.Admin),
    ...
])
```

# Functions #
  * register
> Attributes: Classes (not class instances or objects!) that are derived from ModelAdmin.

> Registers ModelAdmin instance for corresponding model.
> Only one ModelAdmin instance per model can be active.
> In case if more ModelAdmin instances with same model are registered last registered instance will be the active one.

> Sample usage:
```
import appengine_admin

appengine_admin.register(AdminArticle)
```

# Tips and tricks #
## String represenatation of model instances ##
Define `__unicode__ ` method for your model classes to make model instances displayed in human readable format in Appengine Admin user interface.

Sample usage:
```
class Article(db.Model):
    """Your data model
    """
    title = db.StringProperty("Title", required = True)
    content = db.TextProperty("Content", required = True)

    def __unicode__(self):
        return self.title
```

## verbose\_name ##
Appengine Admin makes use of [verbose\_name](http://code.google.com/appengine/docs/datastore/propertyclass.html#Property) setting of your model properties to create labels for fields in Appengine Admin panel.

Sample usage:
```
class Article(db.Model):
    """Your data model
    """
    title = db.StringProperty("Title", required = True)
    content = db.TextProperty("Content", required = True)

class Comment(db.Model):
    article = db.ReferenceProperty(Article, verbose_name = "Article")
    author = db.StringProperty("Author", required = True)
    content = db.TextProperty("Content", required = True)
```

## BlobProperty meta data ##
If you use BlobProperty for file storage then it is very comfortable to have name and MIME type of the uploaded file cached somewhere. The correct file name and type will be given to browser when downloading file contents via admin interface.

To store meta data of the uploaded file define additional BlobProperty field in the same model with name `<original_blob_field_name>_meta`.

Sample usage:
```
class ModelWithBlobs(db.Model):
    # Store the file contents here.
    # Make this field available in admin interface.
    blobField = db.BlobProperty()
    # File name and MIME type will be stored here in as pickled dictionary
    # There's not much point of showing this field in admin interface.
    blobField_meta = db.BlobProperty()
```
If you don't add this extra field or meta information can not be retrieved for some reason the file MIME type will be set to `application/octet-stream` when you will try to download the file.

## ManyToManyProperty ##
ManyToManyProperty simulates ManyToManyProperty from Django by using Appengine's ListProperty.

Sample usage:
```
from appengine_admin.db_extensions import ManyToManyProperty 

class Tag(db.Model):
    name = db.StringProperty("Name")

class Article(db.Model):
    title = db.StringProperty("Title", required = True)
    content = db.TextProperty("Content", required = True)
    tags = ManyToManyProperty(Tag, verbose_name = "Tag cloud")
```

Admin interface will show SelectMultiple widget for ManyToManyProperty