from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from groq import Groq

# Set your Groq API key
GROQ_API_KEY = "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"

# Predefined Q&A dataset
qa_dict = {
    "What is a stock?": "A stock represents ownership in a company and constitutes a claim on part of the company’s assets and earnings.",
    "What is Bitcoin?": "Bitcoin is a decentralized digital currency that operates on a peer-to-peer network without a central authority, using blockchain technology.",
    "What is Ethereum?": "Ethereum is an open-source blockchain platform that enables smart contracts and decentralized applications (dApps) using its native currency, Ether.",
}

# Initialize the Groq client
client = Groq(api_key=GROQ_API_KEY)

def get_chatbot_response(question):
    """
    Function that first checks if the question is in predefined Q&A.
    If not found, it queries LLaMA 3.1 via the Groq API.
    """
    if question in qa_dict:
        return qa_dict[question]

    # Use LLaMA 3.1 if the question is not found in the dataset
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You are a helpful financial chatbot providing educational insights."},
                {"role": "user", "content": question}
            ],
            temperature=0
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"


@csrf_exempt
def chatbot_view(request):
    """
    Django API endpoint to handle chatbot queries.
    """
    if request.method == "POST":
        try:
            # Debugging: Print raw request body
            print("Raw Request Body:", request.body)

            # Decode request body and parse JSON
            data = json.loads(request.body.decode("utf-8"))  

            # Debugging: Print received data
            print("Parsed JSON Data:", data)

            # Extract and validate 'question'
            question = data.get("question", "").strip()

            if not question:
                return JsonResponse({"error": "No question provided"}, status=400)

            # Get chatbot response
            response = get_chatbot_response(question)
            return JsonResponse({"response": response})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Server error: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)