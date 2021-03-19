from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Post

# Tests go below.

class PostTests(TestCase):

    def setUp(self):
        '''This is a way to set up our test database that replicates our real database and it is destroyed
           after we run python manage.py test in CLI.'''
        self.user = get_user_model().objects.create_user(
            username ='pen-tester',
            email = 'pen-tester@gmail.com',
            password = 'secret'
        )
        self.post = Post.objects.create(
            title = 'CHAMPIONSHIP FIGHT',
            slug = 'CHAMPIONSHIP-FIGHT',
            content = 'Tyson Fury has agreed to take on Anthony Joshua',
            author = self.user,
        )
    
    def test_my_string_rep(self):
        '''here we are testing the string representation function for our Post in models.py '''
        writing = Post(title = '2')
        self.assertEqual(str(writing), writing.title)

    def test_my_post_model(self):
        '''Here we test our fields in the test database which replicates our real database'''
        self.assertEqual(f'{self.post.slug}','CHAMPIONSHIP-FIGHT')
        self.assertEqual(f'{self.post.title}','CHAMPIONSHIP FIGHT')
        self.assertEqual(f'{self.post.content}','Tyson Fury has agreed to take on Anthony Joshua')
        self.assertEqual(f'{self.post.author}','pen-tester')
        self.assertEqual(f'{self.post.id}','1')

    def test_my_post_list_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code,200) 
        self.assertTrue(response,'Tyson Fury has agreed to take on Anthony Joshua')
        self.assertContains(response,'1')
        self.assertTemplateUsed(response,'index.html')
        
   def test_post_detail_view(self):
        response = self.client.get('/CHAMPIONSHIP-FIGHT/')
        no_response = self.client.get('/slug/')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.status_code==200, 1)
        self.assertEqual(no_response.status_code,404)
        self.assertEqual(no_response.status_code==404, 1)
        self.assertContains(response, 'CHAMPIONSHIP FIGHT')
        self.assertTemplateUsed(response,'post_detail.html')
     
