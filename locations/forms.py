from django import forms
from .models import Location

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['location_name', 'task1_id', 'task2_id', 'address', 'locked_by']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Get the current address values
        current_address = getattr(self.instance, 'address', '')

        # Make fields read-only except address (conditionally)
        for field in ['latitude', 'longitude']:
            self.fields[field] = forms.CharField(
                initial=getattr(self.instance, field, ''), 
                disabled=True,
                required=False
            )

        
        # Make address editable only if it is "Address not available"
        if current_address != "Address not available":
            self.fields['address'] = forms.CharField(
                initial=current_address,
                disabled=True,
                required=False
            )
