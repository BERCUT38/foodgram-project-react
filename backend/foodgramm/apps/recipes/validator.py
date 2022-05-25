def size_picture(value):
    # Проверка "а заполнено ли поле?"
    if value == '':
        raise forms.ValidationError(
            'Загрузите картинку, или загрузите картинку меньшего размера',
            params={'value': value},
        )  