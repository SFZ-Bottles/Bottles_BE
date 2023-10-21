from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import openai
import os

# Make sure to set this environment variable in your environment,
# or replace `os.getenv("OPENAI_API_KEY")` with your actual OpenAI API key as a string.
openai.api_key = os.getenv("OPENAI_API_KEY")


class VoiceflowView(APIView):
    def post(self, request):
        message = request.data.get('message')

        # Sending request to Voiceflow API
        vf_url = 'https://api.voiceflow.com/your-project-id'
        vf_headers = {'Authorization': 'VOICEFLOW_API_KEY'}
        vf_response = requests.post(vf_url, json={'message': message}, headers=vf_headers)
        
        # Sending request to OpenAI API
        openai_response = openai.Completion.create(
            engine="davinci",
            prompt=message,
            max_tokens=150
        )
        
        # Constructing the response
        response_data = {
            'voiceflow_response': vf_response.json(),
            'openai_response': openai_response.choices[0].text if openai_response.choices else ''
        }

        return Response(response_data, status=vf_response.status_code)
