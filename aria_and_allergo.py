import os
import base64
from openai import OpenAI
from dotenv import load_dotenv
from openai import OpenAIError

# Load environment variables
load_dotenv()

# Define the base URL and API key
base_url = 'https://api.rhymes.ai/v1'
aria_api = os.getenv('ARIA_API_KEY')

# Initialize the OpenAI client
client = OpenAI(
    base_url=base_url,
    api_key=aria_api
)

def image_to_base64(image_file) -> str:
    """
    Converts an uploaded image file to a base64-encoded string.

    Args:
        image_file (file-like object): The image file object.

    Returns:
        str: The base64-encoded string of the image.
    """
    try:
        return base64.b64encode(image_file.read()).decode("utf-8")
    except Exception as e:
        return f"Failed to parse response {str(e)}"


def get_model_response(prompt, images=None):
    """
    Sends a prompt to the AI model and returns the response.
    
    Args:
        prompt (str): The main prompt or question for the model.
        image_prompt (str): A specific prompt related to the image.
        images (list): List of uploaded image files.
        
    Returns:
        str: The AI model's response.
    """
    try:
        # Initialize base message with the general prompt
        system_prompt = """        
        You are a helpful AI agent specializing in first aid guidance. When given images of accident scenes, generate clear, step-by-step first aid instructions.
        If only a text prompt is provided, offer general guidance relevant to the accident scenario. Always create a separate prompt for video demonstration of the first aid steps, regardless of whether images are provided. Structure your response as a JSON-like string with the following keys: 'instructions:' for the first aid steps and 'video_prompt:' for the video content.        
        """
        messages = [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": system_prompt
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]

        # If images are uploaded, process them and include in the messages
        if images:
            image_contents = []
            for image_file in images:
                base64_image = image_to_base64(image_file)
                if base64_image.startswith("An error occurred"):  # Handle potential error
                    return {"error": base64_image}  # Return the error message
                image_contents.append(
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                )
            
            image_tags = "<image>" * len(images)
            # Add the images and image prompt to messages
            messages.append({
                "role": "user",
                "content": image_contents + [
                    {
                        "type": "text",
                        "text": f'{image_tags}{prompt}'
                    }
                ]
            })

        # Make the API request
        response = client.chat.completions.create(
            model="aria",
            messages=messages,
            stop=["<|im_end|>"],
            stream=False,
            temperature=0.6,
            max_tokens=1024,
            top_p=1
        )

        return response.choices[0].message.content
    except KeyError as e:
        return {"Error": f"Response structure unexpected. Error: {str(e)}"}
    except OpenAIError as e:
        return {"Error": f"OpenAI API error: {str(e)}"}
    except Exception as e:
        # Catch-all for any other errors
        return {"Error":f"An error occurred: {str(e)}"}
