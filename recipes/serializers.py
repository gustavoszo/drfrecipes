from rest_framework import serializers
from django.contrib.auth.models import User
from tag.models import Tag
from .models import Recipe
from authors.validators import AuthorRecipeForm

class TagSerializer(serializers.ModelSerializer):
    # Extendendo de serializer
    # id = serializers.IntegerField()
    # name = serializers.CharField(max_length=255)
    # slug = serializers.SlugField()
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description', 'public', 'preparation', 'category',
            'author', 'tags', 'tag_objects', 'tag_links', 'preparation_time',
            'preparation_time_unit', 'servings', 'servings_unit', 'preparation_steps', 'cover'      
        ]

    public = serializers.BooleanField(source='is_published', read_only=True)
    preparation = serializers.SerializerMethodField(read_only=True)
    category = serializers.StringRelatedField(read_only=True)
    tag_objects = TagSerializer(
        many=True,
        source='tags',
        read_only=True
    )
    tag_links = serializers.HyperlinkedRelatedField(
        many=True,
        source='tags',
        view_name='recipes:recipe_api_v2_tag',
        read_only=True
    )

    def get_preparation(self, recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'

    def validate(self, attrs):
        if self.instance is not None and attrs.get('servings') is None:
            attrs['servings'] = self.instance.servings

        if self.instance is not None and attrs.get('preparation_time') is None:
            attrs['preparation_time'] = self.instance.preparation_time

        super_validate = super().validate(attrs)
        AuthorRecipeForm(attrs, ErrorClass=serializers.ValidationError)
        
        return super_validate

    def save(self, **kwargs):
       return super().save(**kwargs)


#  def validate(self, attrs):
#         super_validate = super().validate(attrs)
#         my_errors = dict()

#         title = attrs.ge
#         description = attrs.get('description')

#         if title == description:
#             my_errors['title'] = ['Não pode ser igual a descrição']
#             my_errors['description'] = ['Não pode ser igual ao titulo']

#         if my_errors:
#             raise serializers.ValidationError(my_errors)
        
#         return super_validate
        
#     
# def validate_title(self, value):
#    title = value

#    if len(title) < 5:
#       raise serializers.ValidationError('O titulo deve ter o minimo de 5 caracteres')
#    return title