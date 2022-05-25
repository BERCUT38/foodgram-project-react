from django import forms

def size_picture(value):
    if value == '':
        raise forms.ValidationError(
            'Загрузите картинку, или загрузите картинку меньшего размера',
            params={'value': value},
        )
