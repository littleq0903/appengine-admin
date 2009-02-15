import logging
from google.appengine.ext.db import djangoforms
import django.newforms as forms
from . import admin_widgets


class AdminModelForm(djangoforms.ModelForm):
    """This class extends ModelForm to be able to pass additional attributes
        to the form while processing the request.
    """
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
