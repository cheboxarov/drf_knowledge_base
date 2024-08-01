from .models import Test
from rest_framework.serializers import ModelSerializer, ValidationError
from typing import List


class TestSerializerDetail(ModelSerializer):

    class Meta:
        model = Test
        fields = ['questions', 'article']


    def validate_questions(self, value):
        for question in value:
            if not isinstance(question.get('type'), str):
                raise ValidationError('Type is required and must be a string.')
            if question.get('type') not in ['single', 'multiple']:
                raise ValidationError('Type is required and must be either "single" or "multiple".')
            if not isinstance(question.get('question'), str):
                raise ValidationError('Question is required and must be a string.')
            if not isinstance(question.get('answers'), list) or not all(isinstance(answer, str) for answer in question.get('answers')):
                raise ValidationError('Answers is required and must be an array of strings.')
            if len(question.get('answers')) < 2:
                raise ValidationError('At least 2 answers required.')
            if not isinstance(question.get('right_answers'), list) or not all(
                    isinstance(answer, str) for answer in question.get('right_answers')):
                raise ValidationError(
                    'Right answers (right_answers) is required and must be an array of strings.')
            if len(question.get('right_answers')) == 0:
                raise ValidationError('At least 1 right_answers required.')
            if question.get('type') == 'single' and len(question.get('right_answers')) != 1:
                raise ValidationError('If th type is single, then only 1 correct answer is required')
            for right_answer in question.get('right_answers'):
                if right_answer not in question.get('answers'):
                    raise ValidationError({right_answer:"The correct answer must be contained in the answers"})
        return value
