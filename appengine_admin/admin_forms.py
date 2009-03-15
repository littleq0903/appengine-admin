import logging
import pickle
import copy

from google.appengine.ext.db import djangoforms
from google.appengine.api import datastore_errors
import django.newforms as forms
from django.newforms.util import ValidationError

from . import admin_widgets
from . import utils
from . import admin_settings

MAX_REQUEST_SIZE = admin_settings.MAX_REQUEST_SIZE
BLOB_FIELD_META_SUFFIX = admin_settings.BLOB_FIELD_META_SUFFIX

class AdminModelForm(djangoforms.ModelForm):
    """This class extends ModelForm to be able to pass additional attributes
        to the form while processing the request.
    """
    enctype = ''
    def __init__(self, urlPrefix = '', *args, **kwargs):
        super(AdminModelForm, self).__init__(*args, **kwargs)
        self.urlPrefix = urlPrefix
        instance = kwargs.get('instance', None)

        for fieldName, field in self.fields.items():
            # expose urlPrefix to Select widget
            if isinstance(field.widget, admin_widgets.ReferenceSelect):
                field.widget.urlPrefix = self.urlPrefix
            # deliver meta info to FileInput widget for file download link display
            # do it only if file is uploaded :)
            if instance and isinstance(field.widget, admin_widgets.FileInput) and getattr(instance, fieldName):
                meta = utils.getBlobProperties(instance, fieldName)
                if meta:
                    fileName = meta['File_Name']
                else:
                    fileName = ''
                # these settings should be indivudual for every instance
                field = copy.copy(field)
                widget = copy.copy(field.widget)
                field.widget = widget
                self.fields[fieldName] = field
                # set uploaded file meta data
                widget.showDownloadLink = True
                widget.urlPrefix = self.urlPrefix
                widget.modelName = instance.kind()
                widget.fieldName = fieldName
                widget.itemKey = instance.key()
                widget.fileName = fileName

    def save(self, *args, **kwargs):
        """The overrided method adds uploaded file meta info for BlobProperty fields.
        """
        item = super(AdminModelForm, self).save(*args, **kwargs)
        for fieldName, field in self.fields.items():
            if isinstance(field, FileField) and field.file_name is not None:
                metaFieldName = fieldName + BLOB_FIELD_META_SUFFIX
                if getattr(self.Meta.model, metaFieldName, None):
                    metaData = {
                        'Content_Type': field.file_type,
                        'File_Name': field.file_name,
                        'File_Size': field.file_size,
                    }
                    logging.info("Caching meta data for BlobProperty: %r" % metaData)
                    setattr(item, metaFieldName, pickle.dumps(metaData))
                else:
                    logging.info(
                        'Cache field "%(metaFieldName)s" for blob property "%(propertyName)s" not found. Add field "%(metaFieldName)s" to model "%(modelName)s" if you want to store meta info about the uploaded file',
                        {'metaFieldName': metaFieldName, 'propertyName' : fieldName, 'modelName': self.Meta.model.kind()}
                    )
        # Save the item in Datastore if not told otherwise.
        if kwargs.get('commit', True):
            item.put()
        return item



def createAdminForm(formModel, editFields, editProps):
    """AdminForm factory
        Input: formModel - model that will be used for ModelForm creation
            editFields - tuple of field names that should be exposed in the form
    """
    class AdminForm(AdminModelForm):
        class Meta:
            model = formModel
            fields = editFields

    # Adjust widgets by widget type
    logging.info("Ajusting widgets for AdminForm")
    for fieldName, field in AdminForm.base_fields.items():
        logging.info("  Adjusting field: %s; widget: %s" % (fieldName, field.widget.__class__))
        if isinstance(field.widget, forms.widgets.Textarea):
            logging.info("  Adjusting field: %s; widget: %s" % (fieldName, field.widget.__class__))
            field.widget.attrs.update({'rows': '15', 'cols': '40', 'class': 'adminTextarea'})
        if isinstance(field.widget, forms.widgets.TextInput):
            logging.info("  Adjusting field: %s; widget: %s" % (fieldName, field.widget.__class__))
            field.widget.attrs.update({'class': 'adminTextInput'})
        if isinstance(field.widget, forms.widgets.Select):
            logging.info("  Adjusting field: %s; widget: %s" % (fieldName, field.widget.__class__))
            # Use custom widget with link "Add new" near dropdown box
            field.widget = admin_widgets.ReferenceSelect(
                attrs = field.widget.attrs,
                urlPrefix = None,
                referenceKind = getattr(formModel, fieldName).reference_class.kind()
            )
            # Choices must be set after creating the widget because in our case choices
            # is not a list but a wrapeper around query that always fetches fresh data from datastore
            field.widget.choices = field.choices
        if getattr(field.widget, 'needs_multipart_form', False):
            AdminForm.enctype = 'multipart/form-data'

    # Adjust widgets by property type
    for prop in editProps:
        if prop.typeName == 'DateProperty':
            AdminForm.base_fields[prop.name].widget = admin_widgets.AdminDateWidget()
        if prop.typeName == 'TimeProperty':
            AdminForm.base_fields[prop.name].widget = admin_widgets.AdminTimeWidget()
        if prop.typeName == 'DateTimeProperty':
            old = AdminForm.base_fields[prop.name]
            AdminForm.base_fields[prop.name] = forms.fields.SplitDateTimeField(
                required = old.required,
                widget = admin_widgets.AdminSplitDateTime,
                label = old.label,
                initial = old.initial,
                help_text = old.help_text
            )
    return AdminForm


class FileField(forms.fields.Field):
    widget = admin_widgets.FileInput
    error_messages = {
        'invalid': u"No file was submitted. Check the encoding type on the form.",
        'missing': u"No file was submitted.",
        'empty': u"The submitted file is empty.",
        'max_size': u"File size too big (%s bytes). Max size: %s bytes",
    }

    def __init__(self, *args, **kwargs):
        super(FileField, self).__init__(*args, **kwargs)
        self.file_name = None
        self.file_size = None
        self.file_type = None

    def clean(self, data, initial=None):
        super(FileField, self).clean(initial or data)

        if not self.required and data in forms.fields.EMPTY_VALUES:
            return None
        elif not data.value and initial:
            return initial

        # UploadedFile objects should have name and size attributes.
        try:
            self.file_name = data.filename
            self.file_size = len(data.value)
            self.file_type = data.type
            file_content = data.value
        except AttributeError:
            raise ValidationError(self.error_messages['invalid'])

        if not self.file_name:
            raise ValidationError(self.error_messages['invalid'])
        if not self.file_size:
            raise ValidationError(self.error_messages['empty'])
        if self.file_size > MAX_REQUEST_SIZE:
            raise ValidationError(self.error_messages['max_size'] % (self.file_size, MAX_REQUEST_SIZE))

        return file_content
forms.fields.FileField = FileField
forms.FileField = FileField

### HACK HACK HACK ###
# djangoforms.ReferenceProperty.get_value_for_form() does not catch the error that occurs
# when referenced item is deleted.
# This "monkey patch" fixes the problem.
def _wrapped_get_value_for_form(self, instance):
    """Catch "ReferenceProperty failed to be resolved" error and return None.
    """
    try:
        return _original_get_value_for_form(self, instance)
    except datastore_errors.Error, exc:
        # Error is raised if referenced property is deleted
        # Catch the exception and set value to none
        logging.warning('Error catched while getting item values: %s' % exc)
        return  None

_original_get_value_for_form = djangoforms.ReferenceProperty.get_value_for_form
djangoforms.ReferenceProperty.get_value_for_form = _wrapped_get_value_for_form
