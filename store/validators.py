import os


def validate_file_extension(value):
    """валидатор по формату файла для иконок модели Наши Преимущества"""
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.png', '.svg']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')
