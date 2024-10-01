from django.shortcuts import render

# Create your views here.
import os
import json
import csv
import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.conf import settings
from dotenv import load_dotenv
from openai import OpenAI
from .forms import ReportUploadForm

# Load environment variables
load_dotenv(override=True)
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

class FinancialDataView(View):
    def get(self, request, *args, **kwargs):
        form = ReportUploadForm()
        return render(request, 'financial/upload.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = ReportUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            
            # Save uploaded file to a temporary location
            temp_file_path = os.path.join(settings.MEDIA_ROOT, 'temp_report.pdf')
            with open(temp_file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # Define the instructions file names
            instructions_files = {
                "CurrentAssets": os.path.join(settings.BASE_DIR, 'financial', 'instructions', 'ins_ca.txt'),
                "NoncurrentAssets": os.path.join(settings.BASE_DIR, 'financial', 'instructions', 'ins_nca.txt'),
                "CurrentLiabilities": os.path.join(settings.BASE_DIR, 'financial', 'instructions', 'ins_cl.txt'),
                "NoncurrentLiabilities": os.path.join(settings.BASE_DIR, 'financial', 'instructions', 'ins_ncl.txt'),
                "NetWorth": os.path.join(settings.BASE_DIR, 'financial', 'instructions', 'ins_nw.txt')
            }

            #instructions_files = {
             #   "CurrentAssets": "instructions/ins_ca.txt",
              #  "NoncurrentAssets": "instructions/ins_nca.txt",
               # "CurrentLiabilities": "instructions/ins_cl.txt",
                #"NoncurrentLiabilities": "instructions/ins_ncl.txt",
                #"NetWorth": "instructions/ins_nw.txt"
            #}

            # Create the assistant with the first set of instructions
            with open(instructions_files["CurrentAssets"], 'r') as file:
                instructions = file.read()
            
            all_assistants = client.beta.assistants.list()
            existing_assistant = None
            for assistant in all_assistants:
                if assistant.name == "financedude":
                    existing_assistant = assistant
                    break
            if existing_assistant:
                assistant_id = existing_assistant.id
                print(f"Using existing assistant with ID: {assistant_id}")
            else:
                assistant = client.beta.assistants.create(
                name="financedude",
                instructions=instructions,
                model="gpt-4o",
                tools=[{"type": "file_search"}],
                temperature=0.1,
                top_p=0.1
                )
                assistant_id = assistant.id
                print(f"Created new assistant with ID: {assistant_id}")


  

            '''assistant = client.beta.assistants.create(
                name="financedude",
                instructions=instructions,
                model="gpt-4o",
                tools=[{"type": "file_search"}],
                temperature=0.1,
                top_p=0.1
            )'''

            # Create a vector store called "Financial Statements"
            vector_store = client.beta.vector_stores.create(name="Financial Statements")

            # Ready the files for upload to OpenAI
            file_streams = [open(temp_file_path, "rb")]

            # Upload files and associate with the vector store
            file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
                vector_store_id=vector_store.id, files=file_streams
            )

            # Update the assistant to use the vector store
            assistant = client.beta.assistants.update(
                assistant_id=assistant.id,
                tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
            )

            final_output = {}

            # Process each set of instructions
            for key, instructions_file in instructions_files.items():
                # Update the assistant with the new set of instructions
                with open(instructions_file, 'r') as file:
                    instructions = file.read()

                assistant = client.beta.assistants.update(
                    assistant_id=assistant.id,
                    instructions=instructions
                )

                # Create a thread and attach the file to the message
                message_file = client.files.create(
                    file=open(temp_file_path, "rb"), purpose="assistants"
                )

                thread = client.beta.threads.create(
                    messages=[
                        {
                            "role": "user",
                            "content": f"{key.lower().replace('_', ' ')} breakdown for 2023",
                            "attachments": [
                                {"file_id": message_file.id, "tools": [{"type": "file_search"}]}
                            ],
                        }
                    ]
                )

                # Run the assistant and get the result
                run = client.beta.threads.runs.create_and_poll(
                    thread_id=thread.id, assistant_id=assistant.id
                )

                messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

                message_content = messages[0].content[0].text
                annotations = message_content.annotations
                citations = []

                for index, annotation in enumerate(annotations):
                    message_content.value = message_content.value.replace(annotation.text, f"[{index}]")
                    if file_citation := getattr(annotation, "file_citation", None):
                        cited_file = client.files.retrieve(file_citation.file_id)
                        citations.append(f"[{index}] {cited_file.filename}")

                # Save the result into the final output structure
                final_output[key] = {
                    "result": message_content.value,
                    "citations": citations
                }

            # Save the final output to a JSON file
            json_path = 'final_balance_sheet.json'
            with open(json_path, 'w') as f:
                json.dump(final_output, f, indent=4)

            # Convert JSON to CSV
            csv_data = []
            for category, content in final_output.items():
                result = json.loads(content['result'])
                for metric, value in result.items():
                    csv_data.append([category, metric, value])

            csv_path = 'values.csv'
            with open(csv_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['category', 'metric', 'value'])
                writer.writerows(csv_data)

            # Analyze CSV data
            df = pd.read_csv(csv_path)
            results = []

            grouped = df.groupby('category')

            for category, group in grouped:
                total_row = group[group['metric'].str.contains('Total', case=False)]
                sum_of_items = group[~group['metric'].str.contains('Total', case=False)]['value'].sum()
                total_value = total_row['value'].values[0] if not total_row.empty else None

                sumcheck = sum_of_items == total_value

                if total_value != 0:
                    percentage_mismatch = abs(sum_of_items - total_value) / total_value * 100
                else:
                    percentage_mismatch = 0.0

                results.append({
                    'category': category,
                    'sumcheck': sumcheck,
                    'percentage_mismatch': percentage_mismatch
                })

            result_df = pd.DataFrame(results)

            # Generate response
            response = HttpResponse(result_df.to_csv(index=False), content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="results.csv"'

            return response
        else:
            return render(request, 'financial/upload.html', {'form': form})
