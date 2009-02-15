import django.newforms as forms

class ReferenceSelect(forms.widgets.Select):
    """Customized Select widget that adds link "Add new" near dropdown box.
        This widget should be used for ReferenceProperty support only.
    """
    def __init__(self, urlPrefix = '', referenceKind = '', *attrs, **kwattrs):
        super(ReferenceSelect, self).__init__(*attrs, **kwattrs)
        self.urlPrefix = urlPrefix
        self.referenceKind = referenceKind

    def render(self, *attrs, **kwattrs):
        output = super(ReferenceSelect, self).render(*attrs, **kwattrs)
        return output + u'\n<a href="%s/%s/new/" target="_blank">Add new</a>' % (self.urlPrefix, self.referenceKind)


### These are taken from Django 1.0 contrib.admin.widgets
class AdminDateWidget(forms.TextInput):
    def __init__(self, attrs={}):
        super(AdminDateWidget, self).__init__(attrs={'class': 'vDateField', 'size': '10'})

class AdminTimeWidget(forms.TextInput):
    def __init__(self, attrs={}):
        super(AdminTimeWidget, self).__init__(attrs={'class': 'vTimeField', 'size': '8'})

class AdminSplitDateTime(forms.SplitDateTimeWidget):
    """
    A SplitDateTime Widget that has some admin-specific styling.
    """
    def __init__(self, attrs=None):
        widgets = [AdminDateWidget, AdminTimeWidget]
        # Note that we're calling MultiWidget, not SplitDateTimeWidget, because
        # we want to define widgets.
        forms.MultiWidget.__init__(self, widgets, attrs)

    def format_output(self, rendered_widgets):
        return u'<p class="datetime">%s %s<br />%s %s</p>' % \
            ('Date:', rendered_widgets[0], 'Time:', rendered_widgets[1])
