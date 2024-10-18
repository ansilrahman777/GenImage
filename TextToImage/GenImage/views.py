from urllib.parse import urlparse
from django.http import HttpResponse, JsonResponse
import openai
from django.shortcuts import render, redirect
from django.conf import settings
import requests
from django.views.decorators.csrf import csrf_protect

# importing my openAI api key from settings
openai.api_key = settings.OPENAI_API_KEY



#---------------------------view function for home page ---------------------------------

def index(request):
    return render(request, 'index.html')  #input form



#---------------------------view function for generating the image------------------------

@csrf_protect  # Enable CSRF protection
def generate_image(request):
    if request.method == "POST":
        prompt = request.POST.get('my_description')  # for getting the description from the form (frontend)
        try:
            # for generateing images using the openAI api 
            response = openai.Image.create(
                prompt=prompt,
                n=4,  # Image count
                size="1024x1024"
            )
            images = [data['url'] for data in response['data']]  # Collecting image URLs
            return render(request, 'display_images.html', {'images': images, 'prompt': prompt})  # Render template with images
        except openai.error.OpenAIError as e:
            return render(request, 'index.html', {'error': f"OpenAI API error: {str(e)}"})  # Handle OpenAI API errors
        except requests.exceptions.RequestException as e:
            return render(request, 'index.html', {'error': f"Network error: {str(e)}"})  # Handle network issues
        except Exception as e:
            return render(request, 'index.html', {'error': f"Unexpected error: {str(e)}"})  # Handle unexpected errors
    else:
        return render(request, 'index.html', {'error': "Invalid request method."})  # Handle invalid methods



#----------------------------view function for downloading the image-----------------------------

def download_image(request, image_url):
    # fetch the image from the url
    response = requests.get(image_url)

    # get the original filename from the utl and change its extension to .png 
    filename = urlparse(image_url).path.split('/')[-1].split('?')[0]
    new_filename = f"downloaded_image_{filename.split('.')[0]}.png"

    # send the image as the a file response
    response = HttpResponse(response.content, content_type='image/png')
    response['Content-Disposition'] = f'attachment; filename="{new_filename}"'

    return response
