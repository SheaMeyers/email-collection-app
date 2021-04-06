from import_export import resources, fields
from .models import EmailEntry


class EmailEntryResource(resources.ModelResource):

    email = fields.Field(attribute='email', column_name='Email')
    date_added = fields.Field(attribute='date_added', column_name='Date Added')

    class Meta:
        model = EmailEntry
        fields = ('email', 'date_added',)
        export_order = ('email', 'date_added',)
