from rest_framework.exceptions import ValidationError


class UrlValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        allowed_url_list = ['https://youtube.com/', 'https://www.youtube.com/', ]
        tmp_val = dict(value).get(self.field)
        x = False
        for i in allowed_url_list:
            if i in tmp_val:
                x = True

        if x is not True:
            raise ValidationError('Ссылки на сторонние ресурсы запрещены')
