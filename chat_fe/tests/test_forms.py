from django.test import TestCase
from chat_fe.forms import RegistrationForm


class TestForms(TestCase):
    def test_registration_form_valid_data(self):
        form = RegistrationForm(
            data={
                "username": "lukasz12321",
                "first_name": "lukasz",
                "last_name": "wlosek",
                "email": "email@email.com",
                "password1": "polkiolki901",
                "password2": "polkiolki901",
            }
        )
        self.assertTrue(form.is_valid())

    def test_registration_form_no_data(self):
        form = RegistrationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)
