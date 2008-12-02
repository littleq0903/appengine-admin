import models
import appengine_admin

## Admin views ##
class AdminTestModel(appengine_admin.ModelAdmin):
    model = models.TestModel
    'stringField', 'textField', 'choicesField', 'integerField', 'booleanField', 'referenceField', 'whencreated', 'whenupdated'
    listFields = (
        'stringField',
        'textField',
        'choicesField',
        'integerField',
        'booleanField',
        'referenceField',
        'dateField',
        'timeField',
        'userField',
        'categoryField',
        'linkField',
        'emailField',
        'imField',
        'phoneNumberField',
        'postalAddressField',
        'ratingField',
        'whencreated',
        'whenupdated')
    editFields = (
        'stringField',
        'textField',
        'choicesField',
        'integerField',
        'booleanField',
        'referenceField',
        'dateField',
        'timeField',
        'userField',
        'categoryField',
        'linkField',
        'emailField',
        'imField',
        'phoneNumberField',
        'postalAddressField',
        'ratingField')
    readonlyFields = ('whencreated', 'whenupdated')
    listGql = 'order by stringField, integerField'

class AdminReferencedModel(appengine_admin.ModelAdmin):
    model = models.ReferencedModel
    listFields = ('name', 'whencreated', 'whenupdated')
    editFields = ('name',)
    readonlyFields = ('whencreated', 'whenupdated')
    listGql = 'order by name'
    
appengine_admin.register(AdminTestModel, AdminReferencedModel)

