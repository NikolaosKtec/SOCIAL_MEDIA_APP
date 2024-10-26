# from django.conf import settings
# settings.configure()
import json
from rest_framework.test import APITestCase,RequestsClient
from ..social_network.models import UserModel
import logging
# rest_framework.request.Request
# from rest_framework.test import APIRequestFactory



class Test(APITestCase):
    client = RequestsClient()
    headers = {'Authorization': 'Token 6a192de3bb41380ba44d477ecce73d377ebfba1a'}
    url_base = 'http://localhost:8000/'
   
    def setUp(self):

        UserModel.objects.create(userName='userName',email='email@0',password='password',followers='')
        UserModel.objects.create(userName='userName2',email='email@2',password='password',followers='')
        UserModel.objects.create(userName='userName3',email='email@3',password='password',followers='')
        UserModel.objects.create(userName='userName4',email='email@4',password='password',followers='')
        UserModel.objects.create(userName='userName5',email='email@5',password='password',followers='')
      
    def testGetUsers(self):
        request  = self.client.get(f'{self.url_base}users/')
        # print(request.headers)
        self.assertTrue( request.status_code == 200 and request.headers['Content-Type'] == 'application/json',msg= """ conteudo da resposta 
                        não é application/json ou status code não é 200 """)
        
    def testPostUser(self):
        user_raw =  [ {'userName': "Mclaughlin Middleton zillactic",
        'email': "mclaughlinmiddleton@gmail.com",
        'followers': "",
		'password':"12345678"},
        ]
        
        # user_raw={}

        
        request = self.client.post(f'{self.url_base}users/',data=json.dumps(user_raw),
            content_type='application/json')
        self.assertTrue( request.status_code == 201,msg=f"usuario não foi criado! error: {request.content}")
  

    def test_UserNameAlreadyExists(self):

        user_raw =  [ {'userName': "userName",
        'email': "mclaughlinmiddleton@gmail.com",
        'followers': "",
		'password':"12345678"},
        ]
        
        # user_raw={}

        
        request = self.client.post(f'{self.url_base}users/',data=json.dumps(user_raw),
            content_type='application/json')
        
        self.assertTrue( request.status_code == 400, msg=f'{request.content}')

    def test_EmailAlreadyExists(self):

        user_raw =  [ {'userName': "userName",
        'email': "email@5",
        'followers': "",
		'password':"12345678"},
        ]
        
        # user_raw={}

        
        request = self.client.post(f'{self.url_base}users/',data=json.dumps(user_raw),
            content_type='application/json')
        
        self.assertTrue( request.status_code == 400, msg=f'{request.content}')

    def test_PostUserWeakPassword(self):

        user_raw =  [ {'userName': "userName",
        'email': "email@5",
        'followers': "",
		'password':"123"},
        ]
        
        # user_raw={}

        
        request = self.client.post(f'{self.url_base}users/',data=json.dumps(user_raw),
            content_type='application/json')
        
        self.assertTrue( request.status_code == 400, msg=f'{request.content}')
        
    def test_PostNoneFields(self):

        user_raw =  [ {'userName': "",
       
        'followers': "",
		'password':""},
        ]
        
        # user_raw={}
       
        
        request = self.client.post(f'{self.url_base}users/',data=json.dumps(user_raw),
            content_type='application/json')
        
        
        self.assertTrue( request.status_code == 400, msg=f'{request.content}')

    # def test_put_curso(self):
    #     atualizado = {
    #         "titulo": "Curso atualizado1",
    #         "url": "http://atualizado1.com"
    #     }
    #     resposta = requests.put(url=f'{self.url_base_cursos}3/', headers=self.headers, data=atualizado)
    #     assert resposta.status_code == 200
    
    # def test_put_titulo_curso(self):
    #     atualizado = {
    #         "titulo": "Curso atualizado2",
    #         "url": "http://atualizado2.com"
    #     }
    #     resposta = requests.put(url=f'{self.url_base_cursos}3/', headers=self.headers, data=atualizado)
    #     assert resposta.json()['titulo'] == atualizado["titulo"]