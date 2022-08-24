from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def pdf_format_validator(value):
    """ verifica se o arquivo está no formato pdf """
    if not value.name.endswith('pdf'):
        raise ValidationError(_('por favor verifique se o ficheiro é um PDF'))
