from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class LoginViewTestCase(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(username='KimZangui', email='kimzangui@exemple.com', password='testing321')
        # self.user.set_password('testing321')
        self.user.save()

    def post_views_response(self, view=str, post_values=dict, **kwargs):
        """ Simula uma solicitação post para uma determinada view """

        return self.client.post(
            # url
            reverse(view, kwargs=kwargs),
            # valor
            post_values,
            # aceitar o redirecionamento
            follow=True)

    def test_login_view(self):
        """ testa se o login foi feito com sucesso """

        user_data = {
            'email': self.user.email,
            'password': 'testing321'
        }

        response = self.post_views_response('login', user_data)

        self.assertEqual(response.status_code, 200)
