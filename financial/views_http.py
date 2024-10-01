from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import FinancialReport
from .serializers import FinancialDataSerializer
import os
from django.conf import settings
from dotenv import load_dotenv
from openai import OpenAI
import json
from .prompts import unique_prompts  # Import your prompts
import logging
from django.http import HttpResponse
from .oprompts import original_promts


# Load environment variables
load_dotenv(override=True)
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)


def convert_to_float(value):
    if value == '-' or value is None:
        return 0.0  # Return a default value for invalid entries
    if isinstance(value, float):
        return value  # Return the value as-is if it's already a float
    try:
        return float(str(value).replace(',', ''))  # Convert to string, remove commas, and convert to float
    except ValueError:
        return 0.0 


class FinancialDataView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"message": "Upload a financial report file."}, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
            serializer = FinancialDataSerializer(data=request.data)
            if serializer.is_valid():
                try:
                    uploaded_file = serializer.validated_data['file']

                    # Save the file to the model
                    financial_report = FinancialReport(file=uploaded_file)
                    financial_report.save()  # Save to the database

                    
                    
                    # Save uploaded file to a temporary location
                    temp_file_path = os.path.join(settings.MEDIA_ROOT, 'temp_report.pdf')
                    with open(temp_file_path, 'wb+') as destination:
                        for chunk in uploaded_file.chunks():
                            destination.write(chunk)

                    # Define instructions file names
                    instructions_files = {
                        "CurrentAssets": os.path.join(settings.BASE_DIR, 'financial', 'instructions', 'ins_ca.txt')
                        
                    }
                    
                    all_assistants = client.beta.assistants.list()
                    existing_assistant = next((assistant for assistant in all_assistants if assistant.name == "financedude"), None)

                    if existing_assistant:
                        assistant_id = existing_assistant.id
                    else:
                        with open(instructions_files["CurrentAssets"], 'r') as file:
                            instructions = file.read()
                            assistant = client.beta.assistants.create(
                            name="financedude",
                            instructions=instructions,
                            model="gpt-4o",
                            tools=[{"type": "file_search"}],
                            temperature=0.1,
                            top_p=0.1
                            )
                        assistant_id = assistant.id

                    # Create a vector store
                    vector_store = client.beta.vector_stores.create(name="Financial Statements")
                    file_streams = [open(temp_file_path, "rb")]

                    # Upload files to the vector store
                    client.beta.vector_stores.file_batches.upload_and_poll(vector_store_id=vector_store.id, files=file_streams)

                    # Update the assistant to use the vector store
                    client.beta.assistants.update(
                        assistant_id=assistant_id,
                        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
                    )
                    message_file = client.files.create(
                            file=open(temp_file_path, "rb"), purpose="assistants"
                    )

                    all_messages = []
                    years=[2022,2023]

                    # Process each set of instructions
                    for year in years:
                        year1=year
                        for pmpt in original_promts:
                            a=pmpt.format(year1=year1)
                            print(pmpt,'\n')

                            client.beta.assistants.update(
                                assistant_id=assistant_id,
                                instructions=a
                            )

                            print('\n\n\n\n')
                                    
                            thread = client.beta.threads.create(
                                messages=[
                                    {
                                        "role": "user",
                                        "content": a, 

                                        #"content": f"{key.lower().replace('_', ' ')} breakdown for {year}",
                                        "attachments": [
                                            {"file_id": message_file.id, "tools": [{"type": "file_search"}]}
                                        ],
                                    }
                                ]
                            )

                            run = client.beta.threads.runs.create_and_poll(
                                thread_id=thread.id, assistant_id=assistant_id
                            )

                            messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))
                            all_messages.extend(messages)
                    
                            print('\n',all_messages)
                    all_data=[]
                    for msg in all_messages:
                        for content in msg.content:
                            # Extract the text content
                            text_content = content.text.value

                            # Load the JSON data from the text content
                            data = json.loads(text_content)
                            all_data.append(data)

    

                    
                    
                    
                    return JsonResponse(all_data, status=status.HTTP_200_OK,safe=False)

                    #return HttpResponse(combined_data, content_type='application/json')


                except Exception as e:
                    logging.error(f"Error during file processing: {str(e)}")
                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



