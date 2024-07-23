from rest_framework import test
from rest_framework.reverse import reverse
from .test_recipe_base import RecipeMixin
from unittest.mock import patch

class RecipeAPIV2TestMixin(RecipeMixin):
    def get_recipe_list_reverse_url(self, reverse_result=None):
        api_url = reverse_result or reverse('recipes:recipes-api-list')
        return api_url
    
    def get_recipe_api_list(self, reverse_result=None):
        api_url = self.get_recipe_list_reverse_url(reverse_result)
        response = self.client.get(api_url)
        return response
    
    def get_auth_data(self, username='user', password='pass'):
        user = {
            'username': username,
            'password': password
        }
        created_user = self.make_author(
            username=user['username'],
            password=user['password']
        )
        api_url = reverse('recipes:token_obtain_pair')
        response = self.client.post(api_url, data={**user})

        return {
            'jwt_access_token': response.data.get('access'),
            'jwt_refresh_token': response.data.get('refresh'),
            'user': created_user,
        }
    
    def get_recipe_raw_data(self):
        return {
            "title": "Este é o title da recipe com autor",
            "description": "Esse é o tile",
            "servings": 1,
            "preparation_time": 1,
            "preparation_time_unit": "Minutos",
            "servings_unit": "Porções",
            "preparation_steps": "Modo de preparo"
        }

class RecipeAPIv2Test(test.APITestCase, RecipeAPIV2TestMixin):

    def test_recipe_api_list_return_status_code_200(self):
        api_url = self.get_recipe_list_reverse_url()
        response = self.get_recipe_api_list(api_url)
        self.assertEqual(
            response.status_code,
            200
        )

    @patch('recipes.views.api.RecipeAPIv2Pagination.page_size', new=7)
    def test_recipe_api_list_loads_correct_number_of_recipes(self):
        wanted_number_of_recipes = 7
        self.make_recipe_in_batch(qtd=wanted_number_of_recipes)

        api_url = self.get_recipe_list_reverse_url()
        response = self.get_recipe_api_list(api_url)
        qtd_of_loaded_recipes = len(response.data.get('results'))

        self.assertEqual(
            wanted_number_of_recipes,
            qtd_of_loaded_recipes
        )

    def test_recipe_api_list_do_not_show_not_published_recipes(self):
        recipes = self.make_recipe_in_batch(qtd=2)
        recipe_not_published = recipes[0]
        recipe_not_published.is_published = False
        recipe_not_published.save()
        recipe_published = recipes[1]
        api_url = self.get_recipe_list_reverse_url()
        response = self.get_recipe_api_list()
        self.assertEqual(
            len(response.data.get('results')),
            1
        )

    @patch('recipes.views.api.RecipeAPIv2Pagination.page_size', new=10)
    def test_recipe_api_list_loads_recipes_by_servings_qtd(self):
        recipes = self.make_recipe_in_batch()
        
        for recipe in recipes:
            recipe.servings = 1

        recipes[0].servings = 2
        recipes[0].save()
        
        api_url = reverse('recipes:recipes-api-list') + '?servings=1'
        response = self.client.get(api_url)

        self.assertEqual(
            len(response.data.get('results')),
            9
        )

    def test_recipe_api_list_must_be_send_jwt_token_to_create_recipe(self):
        api_url = reverse('recipes:recipes-api-list')
        response = self.client.post(api_url)

        self.assertEqual(
            response.status_code,
            401
        )

    def test_recipe_api_list_logged_user_can_create_a_recipe(self):
        recipe_raw_data = self.get_recipe_raw_data()
        api_url = self.get_recipe_list_reverse_url()

        response = self.client.post(
            api_url, data={**recipe_raw_data}, 
            HTTP_AUTHORIZATION='Bearer ' + self.get_auth_data()['jwt_access_token']
        )
        self.assertEqual(
            response.status_code,
            201
        )

    def test_recipe_api_list_logged_user_can_update_a_recipe(self):
        recipe = self.make_recipe()
        auth = self.get_auth_data(username='patch_test', password='abcd1234')
        recipe.author = auth['user']
        recipe.save()
        
        wanted_title = 'This is the new title'

        response = self.client.patch(
            reverse('recipes:recipes-api-detail', args = (recipe.id, )), 
            data={'title': wanted_title}, 
            HTTP_AUTHORIZATION='Bearer ' + self.get_auth_data()['jwt_access_token']
        )

        self.assertEqual(
            response.data.get('title'),
            wanted_title
        ) 
    