from django.test import TestCase
from django.contrib.auth.models import User
from .models import Team, Membership

# Create your tests here.
class TeamTestCase(TestCase):
    def setUp(self):
        self.u1 = User.objects.create_user('u1', 'u1@mail.com', '123456')
        self.u2 = User.objects.create_user('u2', 'u1@mail.com', '123456')
        self.u3 = User.objects.create_user('u3', 'u1@mail.com', '123456')
        self.t1 = Team.objects.create_team(creator=self.u1, name='team1')

    def test_members(self):
        self.t1.invite(self.u2, self.u1)
        self.t1.apply(self.u3)
        self.assertEquals(2, self.t1.members.count())
        # import pprint
        print self.t1.members.all()
        print self.t1.creator
        # pprint.pprint( self.t1.members.all() )
        #print self.t1.members.values()

        #print self.t1.members
        #print self.t1.creator
