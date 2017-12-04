from flask_admin.contrib import sqla
from flask_admin.contrib.sqla.fields import QuerySelectMultipleField, QuerySelectField
from flask_admin.form.fields import Select2TagsField
from flask_admin.form import Select2Widget
from wtforms.validators import Required

from . import models

#class MyQuerySelectMultipleField(QuerySelectMultipleField):
#    def process_formdata(self, valuelist):
#        if valuelist:
#            if self.allow_blank and valuelist[0] == u'__None':
#                self.data = None
#            else:
#                self._data = None
#                self._formdata = valuelist[0]
#
#    def _value(self):
#        raise("fuck value")
#        if isinstance(self._formdata, (list, tuple)):
#            return u','.join(as_unicode(v) for v in self._formdata)
#        elif self._formdata:
#            return as_unicode(self._formdata)
#        else:
#            return u''


class DnsForwarderView(sqla.ModelView):
    column_searchable_list = [models.DnsForwarder.dm, models.DnsForwarder.dns]
    column_filters =  column_searchable_list

    form_excluded_columns = ('typ')

    form_choices = {
            'typ': [
               ('only', 'only'),
               ('first', 'first'),
            ]
    }

    def ldns_choices():
        #return [ ldns.addr for ldns in models.Ldns.query.all() ]
        return models.Ldns.query.all()


    form_extra_fields= dict(
        #dns=QuerySelectMultipleField(
        #dns=MyQuerySelectMultipleField(
        #    label='DNS server',
        #    query_factory=ldns_choices,
        #    validators=[Required()],
        #)

        dns=Select2TagsField(label='DNS Server',validators=[Required()]),
    )
