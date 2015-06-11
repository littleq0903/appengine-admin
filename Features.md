# Implemented features #
  * List records for each registered model
  * Create new records
  * Update/edit records
  * Delete records
  * [Paging](PagingListView.md) of items in Appengine Admin list view
  * Derived modules
  * Supported and tested model property types:
    * [StringProperty](http://code.google.com/appengine/docs/datastore/typesandpropertyclasses.html#StringProperty)
    * [IntegerProperty](http://code.google.com/appengine/docs/datastore/typesandpropertyclasses.html#IntegerProperty)
    * [FloatProperty](http://code.google.com/appengine/docs/datastore/typesandpropertyclasses.html#FloatProperty)
    * [ReferenceProperty](http://code.google.com/appengine/docs/datastore/typesandpropertyclasses.html#ReferenceProperty)
    * [TextProperty](http://code.google.com/appengine/docs/datastore/typesandpropertyclasses.html#TextProperty)
    * [BooleanProperty](http://code.google.com/appengine/docs/datastore/typesandpropertyclasses.html#BooleanProperty)
    * [BlobProperty](http://code.google.com/appengine/docs/datastore/typesandpropertyclasses.html#BlobProperty)
    * [CategoryProperty](http://code.google.com/appengine/docs/datastore/typesandpropertyclasses.html#CategoryProperty)
    * [LinkProperty](http://code.google.com/appengine/docs/datastore/typesandpropertyclasses.html#LinkProperty)
    * [EmailProperty](http://code.google.com/appengine/docs/datastore/typesandpropertyclasses.html#EmailProperty)
    * [IMProperty](http://code.google.com/appengine/docs/datastore/typesandpropertyclasses.html#IMProperty)
    * [PhoneNumberProperty](http://code.google.com/appengine/docs/datastore/typesandpropertyclasses.html#PhoneNumberProperty)
    * [PostalAddressProperty](http://code.google.com/appengine/docs/datastore/typesandpropertyclasses.html#PostalAddressProperty)
    * [RatingProperty](http://code.google.com/appengine/docs/datastore/typesandpropertyclasses.html#RatingProperty)
    * [DateTimeProperty](http://code.google.com/appengine/docs/datastore/typesandpropertyclasses.html#DateTimeProperty)
    * [DateProperty](http://code.google.com/appengine/docs/datastore/typesandpropertyclasses.html#DateProperty)
    * [TimeProperty](http://code.google.com/appengine/docs/datastore/typesandpropertyclasses.html#TimeProperty)
    * [StringListProperty](http://code.google.com/appengine/docs/python/datastore/typesandpropertyclasses.html#StringListProperty)
  * Not tested but should be usable without additional patches:
    * [UserProperty](http://code.google.com/appengine/docs/datastore/typesandpropertyclasses.html#UserProperty)
  * These property types have custom widgets:
    * [TextProperty](http://code.google.com/appengine/docs/datastore/typesandpropertyclasses.html#TextProperty) - Textarea (just bigger size than the default one)
    * [ReferenceProperty](http://code.google.com/appengine/docs/datastore/typesandpropertyclasses.html#ReferenceProperty) - dropdown list of existing records
    * [BooleanProperty](http://code.google.com/appengine/docs/datastore/typesandpropertyclasses.html#BooleanProperty) - Checkbox in edit view
    * [BlobProperty](http://code.google.com/appengine/docs/datastore/typesandpropertyclasses.html#BlobProperty) - File upload field; link to already uploaded file.
    * [DateTimeProperty](http://code.google.com/appengine/docs/datastore/typesandpropertyclasses.html#DateTimeProperty) - Split date-time widget (taken from Django admin interface).
    * [DateProperty](http://code.google.com/appengine/docs/datastore/typesandpropertyclasses.html#DateProperty) - Date pickup widget (taken from Django admin interface).
    * [TimeProperty](http://code.google.com/appengine/docs/datastore/typesandpropertyclasses.html#TimeProperty) - Time widget (taken from Django admin interface).
  * These property types need some additional work in Appengine Admin to be really usable:
    * [SelfReferenceProperty](http://code.google.com/appengine/docs/datastore/typesandpropertyclasses.html#SelfReferenceProperty)
    * [GeoPtProperty](http://code.google.com/appengine/docs/datastore/typesandpropertyclasses.html#GeoPtProperty)
  * Custom properties (from appengine\_admin.db\_extensions)
    * ManyToManyProperty
    * StringListChoicesProperty