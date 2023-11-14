from django import forms 
from .models import Worker

class WorkerForm(forms.ModelForm):
    
    class Meta:
        model = Worker
        
        fields = (
            "wid",
            "name",
            "description"
        )
    
        labels = {
            "wid": "Worker ID",
            "name": "Worker name",
            "address": "Worker address(dns or ip address)"
        }
        