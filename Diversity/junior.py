from typing import Optional
from unittest import mock

import pytest
"""
from app.factories import UserFactory
from app.models import Lexicon, User
from app.views import LexiconResourceList

from tests.conftest import deleted


@pytest.fixture
def user():
   user = UserFactory()
   yield user
   deleted(user)


class TestLexiconResourceList:
   f_post = LexiconResourceList().post.__wrapped__

   @mock.patch('app.views.request')
   def test_post(self, mock_request, user: User):
       data = {'value': "Word_1"}
       mock_request.json = data
       mock_request.user = user
       resp = self.f_post()

       assert resp['value'] == data['value']
       lexicon: Optional[Lexicon] = Lexicon.query \
           .filter(Lexicon.value == data['value'], Lexicon.status == Lexicon.Status.active) \
           .first()
       assert lexicon is not None

       # try again to add the word
       resp = self.f_post()
       assert 'This word already exists' in resp['errors'][0][0]

"""    