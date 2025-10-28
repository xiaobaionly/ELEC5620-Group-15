from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=User.Role.choices,
        label='Role',
        widget=forms.RadioSelect  # Render as radio buttons
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Field placeholders and focus
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Username (login name)',
            'autofocus': True
        })
        self.fields['email'].widget.attrs.update({'placeholder': 'Email (optional)'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Set password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm password'})

        # Apply unified Tailwind CSS styles
        for name, field in self.fields.items():
            base = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (
                base + ' w-full rounded-lg border px-3 py-2 '
                       'focus:outline-none focus:ring-2 focus:ring-green-500'
            ).strip()

        # Add styles for RadioSelect (role)
        if hasattr(self.fields['role'].widget, 'attrs'):
            self.fields['role'].widget.attrs.update({'class': 'space-x-2'})
