from django.test import TestCase
from django.contrib.auth.models import User

from users.forms import UserRegisterForm


# class UserRegisterFormTestCase(TestCase):
#     """ teste para o form UserRegisterForm """

#     def test_user_resgister_form__is_valid(self):
#         """ testa se os dados enviados para o formulário  UserRegisterForm são válidos """

#         user_register_form = UserRegisterForm(data={'email': 'kimzangui@gmail.com', 'password1': 't&sting12&@44', 'password2': 't&sting12&@44'})

#         self.assertTrue(user_register_form.is_valid(), user_register_form.errors.as_data())
