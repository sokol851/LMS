from rest_framework.exceptions import ValidationError


class UrlValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        allowed_url_list = ['https://youtube.com/', 'https://www.youtube.com/', ]
        tmp_val = dict(value).get(self.field)
        valid = False
        if tmp_val is not None:
            for url in allowed_url_list:
                if url in tmp_val:
                    valid = True
        else:
            valid = True

        if valid is not None and valid is not True:
            raise ValidationError('Ссылки на сторонние ресурсы запрещены')
