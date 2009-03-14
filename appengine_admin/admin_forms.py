import logging

from google.appengine.ext.db import djangoforms
from google.appengine.api import datastore_errors
import django.newforms as forms
from django.newforms.util import ValidationError

from . import admin_widgets


class AdminModelForm(djangoforms.ModelForm):
    """This class extends ModelForm to be able to pass additional attributes
        to the form while processing the request.
    """
    enctype = ''
    def __init__(self, urlPrefix = '', *args, **kwargs):
        super(AdminModelForm, self).__init__(*args, **kwargs)
        self.urlPrefix = urlPrefix
        # expose urlPrefix to Select widget
        for fieldName, field in self.fields.items():
            if isinstance(field.widget, admin_widgets.ReferenceSelect):
                field.widget.urlPrefix = self.urlPrefix


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
    }

    def __init__(self, *args, **kwargs):
        super(FileField, self).__init__(*args, **kwargs)

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

        return file_content
forms.fields.FileField = FileField
forms.FileField = FileField

### HACK HACK HACK ###
# djangoforms.ReferenceProperty.get_value_for_form() does not catch the error that occurs
# when referenced item is deleted.
# This "monkey patch" fixes the problem.
def wrapped_get_value_for_form(self, instance):
    """Catch "ReferenceProperty failed to be resolved" error and return None.
    """
    try:
        return original_get_value_for_form(self, instance)
    except datastore_errors.Error, exc:
        # Error is raised if referenced property is deleted
        # Catch the exception and set value to none
        logging.warning('Error catched while getting item values: %s' % exc)
        return  None

original_get_value_for_form = djangoforms.ReferenceProperty.get_value_for_form
djangoforms.ReferenceProperty.get_value_for_form = wrapped_get_value_for_form
