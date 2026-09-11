from django import forms

from .models import Shop


class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = [
            "name",
            "description",
            "address",
            "phone",
            "open_time",
            "close_time",
            "is_active",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "open_time": forms.TimeInput(attrs={"type": "time"}),
            "close_time": forms.TimeInput(attrs={"type": "time"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == "is_active":
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"

    def clean(self):
        cleaned_data = super().clean()
        open_time = cleaned_data.get("open_time")
        close_time = cleaned_data.get("close_time")
        if open_time and close_time and open_time == close_time:
            raise forms.ValidationError("Open time and close time cannot be the same.")
        return cleaned_data
