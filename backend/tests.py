'''tests of all endpoints'''

#to use jsons
import json

#django imports
from django.urls import reverse
from rest_framework import status

#models to use in tests
from accounts.models import CustomUser
from goals.models import Goal
from scores.models import TotalScore, IndividualScore

#serializers to use with the models
from accounts.api.serializers import (UserSerializer, 
                                    CustomLoginSerializer, 
                                    CustomRegisterSerializer)
from goals.api.serializers import GoalSerializer
from scores.api.serializers import IndividualScoreSerializer, TotalScoreSerializer

#base class of the test cases
from rest_framework.test import APITestCase

#date objects for the total scores
from datetime import datetime, timedelta

#the core utils, holds functions that produce repetitive pieces of test code used for database setup
from core.utils import (create_user, 
                        create_three_goals, 
                        create_three_scores, 
                        create_three_ind_scores, 
                        single_goal,
                        clean_month,
                        create_three_ind_scores_same
                        )

#test registration through api
class RegistrationTestCase(APITestCase):
    def test_registration(self):
        #the data of the user being registered
        data = {"email": "test1@server.com",
                'password1': "a-very-strong-password",
                'password2': 'a-very-strong-password'}
        #the response
        response = self.client.post("/api/rest-auth/registration/", data)
        #assert equal
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#test login through api
class LogInTestCase(APITestCase):
    #the method to login the created user
    def test_log_in(self):                               
        self.CustomUser = create_user('test1@server.com', 'Test', 'User')
        #the user's data
        data = {'email': 'test1@server.com',
                'password':'a-very-strong-password'}
        #the response
        response = self.client.post('/api/rest-auth/login/', data)
        #check a 200 response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

#test view of current user
class CurrentUserViewTestCase(APITestCase):
    #setup, build user, call authentication
    def setUp(self):
        #an empty dic to store the returned data
        self.ret = {}
        #make a user
        self.CustomUser = create_user('test1@server.com', 'Test', 'User')
        #authenticate user
        self.api_authentication()
    
    #the autentication method
    def api_authentication(self):
        self.client.login(email = 'test1@server.com', password = 'a-very-strong-password')
        #call a method used to generate one response to fill the global data dict for attribute tests
        self.fill_dict()

    #a method to populate the credentials of the user
    def fill_dict(self):
        response = self.client.get('/api/accounts/')
        self.ret = response.data

    #test the proper status code, see if data was retrieved
    def test_data_returned(self):
        #response for the request for this user's data
        response = self.client.get('/api/accounts/')
        #status code should be 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    #test the first name
    def test_valid_first_name(self):
        self.assertEqual(self.CustomUser.first_name, self.ret['first_name'])

    #test the last name
    def test_valid_last_name(self):
        self.assertEqual(self.CustomUser.last_name, self.ret['last_name'])

    #test the email
    def test_valid_email(self):
        self.assertEqual(self.CustomUser.email, self.ret['email'])

#test creation of goals
class GoalCreateTestCase(APITestCase):
    #the setup method, needed to create and login
    def setUp(self):
        #make a user
        self.CustomUser = create_user('test1@server.com', 'Test', 'User')
        #the data for the goal
        self.data = [{'goal': 'test',
                    'measure': 10, 
                    'unit': 'minutes', 
                    'weight':20, 
                    'mon': True,
                    'tues':False,
                    'wen': False,
                    'thurs': False,
                    'fri': False,
                    'sat': False,
                    'sun': False
                    },
                    {'goal': 'test1',
                    'measure': 20, 
                    'unit': 'hours', 
                    'weight':20, 
                    'mon': True,
                    'tues':False,
                    'wen': False,
                    'thurs': False,
                    'fri': False,
                    'sat': False,
                    'sun': False
                    }]
        #authenticate user
        self.api_authentication()
    
    #the autentication method
    def api_authentication(self):
        self.client.login(email = 'test1@server.com', password = 'a-very-strong-password')
    
    #tests that goal has been created, using a valid category
    def test_goal_creation(self):
        #use a valid category with the data
        self.data[0]['category'] = 'fitness'
        self.data[1]['category'] = 'career'
        response = self.client.post(path = '/api/goal/create/', data = json.dumps(self.data), content_type = 'application/json')
        #test the response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    
    #tests creating a goal with an invalid category, should return 400 error
    def test_bad_goal_creation(self):
        #use invalid category
        self.data[0]['category'] = 'invalid'
        self.data[1]['category'] = 'career'
        #the response
        response = self.client.post(path = '/api/goal/create/', data = self.data, content_type = 'application/json')
        #test the response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


#test viewing a list of goals
class GoalListViewTestCase(APITestCase):
    #the setup method, needed to create and login
    def setUp(self):
        #make a user
        self.CustomUser = create_user('test1@server.com', 'Test', 'User')
        #declaration of data vars
        self.data1 = {}
        self.data2 = {}
        self.data3 = {}
        #authenticate user
        self.api_authentication()
    
    #the autentication method
    def api_authentication(self):
        self.client.login(email = 'test1@server.com', password = 'a-very-strong-password')
        #call a method that creates 3 goals for the user
        self.create_goals()
    
    #a method that creates three goals to test with the list view
    def create_goals(self):
        #create the 3 goals
        create_three_goals(self.CustomUser)
        #call a method to generate the reponse that will be used to check the 3 goals
        self.gen_response()
    
    #stores responses for the goals
    def gen_response(self):
        response = self.client.get('/api/goal/list/')
        #stores dictionaries for the first two goals
        self.data1 = json.loads(json.dumps(response.data['results'][0]))
        self.data2 = json.loads(json.dumps(response.data['results'][1]))
        #third goal on a new page, new request
        next_page = response.data['next']
        response2 = self.client.get(next_page)
        self.data3 = json.loads(json.dumps(response2.data['results'][0]))
        
    #check that a 200 response is returned when the page is requested
    def test_goal_list_request(self):
        #the reponse
        response = self.client.get('/api/goal/list/')
        #test the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    #checks that goal returned is what it should be 
    def test_goal_list_response1(self):
        self.assertEqual(self.data1['goal'], 'test1')
    
    #checks that goal 2 returned is what it should be
    def test_goal_list_response2(self):
        self.assertEqual(self.data2['goal'], 'test2')
    
    #checks that goal 3 returned is what it should be
    def test_goal_list_response3(self):
        self.assertEqual(self.data3['goal'], 'test3')

#test updating a particular goal
class UpdateGoalTestCase(APITestCase):
    #the setup method, needed to create and login
    def setUp(self):
        #make a user
        self.CustomUser = create_user('test1@server.com', 'Test', 'User')
        #declaration of goal vars
        self.Goal = None
        #authenticate user
        self.api_authentication()
    
    #the autentication method
    def api_authentication(self):
        self.client.login(email = 'test1@server.com', password = 'a-very-strong-password')
        #call a method that creates 3 goals for the user
        self.create_goal()
    
    #a method that creates goals for the database
    def create_goal(self):
        create_three_goals(self.CustomUser)
        
    #check that goal is successfully updated at the endpoint, see if the update takes effect
    def test_update_goal(self):
        #the data to update
        new_data = {'goal' :'updated',
                    'category' :'fitness',
                    'measure' :10, 
                    'unit' :'minutes', 
                    'weight' :20, 
                    'mon' :True,
                    'tues' :False,
                    'wen' :False,
                    'thurs' :False,
                    'fri' :False,
                    'sat' :False,
                    'sun' :False,
                    'user' :self.CustomUser}
        #post to the update endpoint
        response = self.client.put('/api/goal/1/update/', new_data)
        #now get the goal back
        response2 = self.client.get('/api/goal/list/')
        response_data = response2.data
        response_data = json.loads(json.dumps(response.data))
        self.assertEqual(response_data['goal'], 'updated')

#test list view of the total scores
class TotalScoreListViewTest(APITestCase):
    #the setup method, needed to create and login
    def setUp(self):
        #make a user
        self.CustomUser = create_user('test1@server.com', 'Test', 'User')
        #authenticate user
        self.api_authentication()
        #create 3 goals
        goal_list = create_three_goals(self.CustomUser)
        #create 3 total scores
        score_list = create_three_scores()
        #create three individual scores
        create_three_ind_scores(goal_list, score_list)
        #to hold the data from the list of total scores
        self.data1 = None
        self.data2 = None
        self.data3 = None
        #method to get responses
        self.gen_response()

    #the autentication method
    def api_authentication(self):
        self.client.login(email = 'test1@server.com', password = 'a-very-strong-password')
    
    #stores responses for the list
    def gen_response(self):
        response = self.client.get('/api/totalScore/list/')
        #stores dictionaries for the first two goals
        self.data1 = json.loads(json.dumps(response.data['results'][0]))
        self.data2 = json.loads(json.dumps(response.data['results'][1]))
        #third goal on a new page, new request
        next_page = response.data['next']
        response2 = self.client.get(next_page)
        self.data3 = json.loads(json.dumps(response2.data['results'][0]))
        

    #check that a 200 response is returned when the page is requested
    def test_score_list_request(self):
        #the reponse
        response = self.client.get('/api/totalScore/list/')
        #test the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    #checks that score 1 is returned as it should be
    def test_goal_list_response1(self):
        self.assertEqual(self.data1['total_score'], 100)
    
    #checks that score 2 is returned as it should be
    def test_goal_list_response2(self):
        self.assertEqual(self.data2['total_score'], 200)
    
    #checks that score 3 is returned as it should be
    def test_goal_list_response3(self):
        self.assertEqual(self.data3['total_score'], 300)
    
    #check if list view contains score created by a different user
    def test_list_score_dif_user(self):
        #make a new user
        new_user = create_user('new_email@server.com', 'test2_first', 'test2_last')
        #create a new goal for this user
        new_goal = single_goal(new_user)
        #create a new total score for today
        new_total_score = TotalScore.objects.create(total_score = 0, date = datetime.now())
        IndividualScore.objects.create(goal = new_goal, individual_score = 10, total_score = new_total_score)
        #the list view should still 3 items, no score for other user
        response = self.client.get('/api/totalScore/list/')
        next_page = response.data['next']
        response2 = self.client.get(next_page)
        self.assertEqual(len(response2.data['results']), 1)

    #test if can pass in month as a parameter as filter
    def test_month_filter(self):
        dt1 = datetime.now().replace(day=1)
        dt2 = dt1 - timedelta(days=1)
        dt3 = dt2.replace(day=1)
        new_total_score = TotalScore.objects.create(total_score = 0, date = dt3)
        new_goal = single_goal(self.CustomUser)
        IndividualScore.objects.create(goal = new_goal, individual_score = 10, total_score = new_total_score)
        #create a total score from a previous month
        dt1 = datetime.now().replace(day=1)
        dt2 = dt1 - timedelta(days=1)
        dt3 = dt2.replace(day=1)
        #get month and year of this previous month
        year = str(dt3.year)
        month = clean_month(dt3.month)
        #get the response
        url = '/api/totalScore/list/?month=' + month + "+" + year
        response = self.client.get(url)
        response_data = json.loads(json.dumps(response.data))
        self.assertEqual(response_data['count'], 1)

#test update of a score
class IndividualScoreUpdateTestCase(APITestCase):
    #the setup method, needed to create and login
    def setUp(self):
        #make a user
        self.CustomUser = create_user('test1@server.com', 'Test', 'User')
        #authenticate user
        self.api_authentication()
        #create 3 goals
        self.goal_list = create_three_goals(self.CustomUser)
        #create 3 total scores
        self.score_list = create_three_scores()
        #create three individual scores
        create_three_ind_scores(self.goal_list, self.score_list)
        #authenticate userdatetime.now() + timedelta(days=1)
        self.api_authentication()
    
    #the autentication method
    def api_authentication(self):
        self.client.login(email = 'test1@server.com', password = 'a-very-strong-password')
    
    #check that total score is successfully updated
    def test_update_score(self):
        #the data to update
        new_data = [{'id':1, 'individual_score': 10000}, {'id': 2, 'individual_score': 50}]
        #post to the update endpoint
        response = self.client.patch(path = '/api/score/update/', data = json.dumps(new_data), content_type = 'application/json')
        #get the goals back, check that score has been updated
        response2 = self.client.get('/api/score/list/')
        response_data = response2.data
        response_data = json.loads(json.dumps(response_data))
        results = response_data['results']
        result_list = []
        for res in results:
            result_list.append(res['individual_score'])
        self.assertEqual([10000, 50], result_list)
    
    #try to update a score created by a different user
    def test_update_score_dif_user(self):
        #make a new user
        new_user = create_user('new_email@server.com', 'test2_first', 'test2_last')
        #create a new goal for this user
        new_goal = single_goal(new_user)
        #create a new total score for today
        new_total_score = TotalScore.objects.create(total_score = 0, date = datetime.now())
        #create an individual score for this user
        IndividualScore.objects.create(goal = new_goal, individual_score = 10, total_score = new_total_score)
        #the update view should not include this score
        new_data = [{'individual_score': 10000, 'id': 4}]
        response = self.client.patch(path = '/api/score/update/', data = json.dumps(new_data), content_type = 'application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#test web endpoint used for goals mapped to scores for a passed in total score id
class GoalToScoreTestCase(APITestCase):
    #the setup method, needed to create and login
    def setUp(self):
        #make a user
        self.CustomUser = create_user('test1@server.com', 'Test', 'User')
        #authenticate user
        self.api_authentication()
        #create 3 goals for this user
        self.goal_list = create_three_goals(self.CustomUser)
        #create a total score
        self.total_score = TotalScore.objects.create(total_score = 0, date = datetime.now())
        #create three individual scores
        create_three_ind_scores_same(self.goal_list, self.total_score)
        #create 3 goals and 3 scores for a different user
        self.set_up_another_user()
        self.api_authentication()
    
    #the autentication method
    def api_authentication(self):
        self.client.login(email = 'test1@server.com', password = 'a-very-strong-password')

    #set up another user
    def set_up_another_user(self):
        new_user = create_user('new_email@server.com', 'test2_first', 'test2_last')
        goal_list = create_three_goals(new_user)
        total_score = TotalScore.objects.create(total_score = 0, date = datetime.now())
        score_list = create_three_ind_scores_same(goal_list, total_score)

    #test that the data is what is should be, only this user's goals
    def test_get_goal_scores(self):
        response = self.client.get('/api/endpoints/goal-to-scores/?id=1')
        response_data = json.loads(json.dumps(response.data))
        expected_data = {'test1': [10, 'minutes'], 'test2': [20, 'hours'], 'test3': [30, 'reps']}
        self.assertEqual(response_data, expected_data)

#test endpoint that retrieves categoris mapped to a list of goal info and ind scores
class GoalTodayTestCase(APITestCase):
    #the setup method, needed to create and login
    def setUp(self):
        #make a user
        self.CustomUser = create_user('test1@server.com', 'Test', 'User')
        #authenticate user
        self.api_authentication()
        #create 3 goals for this user
        self.goal_list = create_three_goals(self.CustomUser)
        #create a total score
        self.total_score = TotalScore.objects.create(total_score = 0, date = datetime.now())
        #create three individual scores
        create_three_ind_scores_same(self.goal_list, self.total_score)
        #create 3 goals and 3 scores for a different user
        self.set_up_another_user()
        self.api_authentication()
    
    #the autentication method
    def api_authentication(self):
        self.client.login(email = 'test1@server.com', password = 'a-very-strong-password')

    #set up another user
    def set_up_another_user(self):
        new_user = create_user('new_email@server.com', 'test2_first', 'test2_last')
        goal_list = create_three_goals(new_user)
        total_score = TotalScore.objects.create(total_score = 0, date = datetime.now())
        score_list = create_three_ind_scores_same(goal_list, total_score)
    
    #test that the results are what they should be, only for the authenticated user
    def test_score_today(self):
        response = self.client.get('/api/endpoints/ScoreToday/')
        response_data = json.loads(json.dumps(response.data))
        expected_data = {'fitness': [['test1', 10, 'minutes', 10, 1]], 'career':[['test2', 20, 'hours', 10, 2]], 'social': [['test3', 30, 'reps', 10, 3]]}
        self.assertEqual(response_data, expected_data)