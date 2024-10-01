# your_app/views.py
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





# Load environment variables
load_dotenv(override=True)
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

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
                    "CurrentAssets": os.path.join(settings.BASE_DIR, 'financial', 'instructions', 'ins_ca.txt'),
                    "NoncurrentAssets": os.path.join(settings.BASE_DIR, 'financial', 'instructions', 'ins_nca.txt'),
                    "CurrentLiabilities": os.path.join(settings.BASE_DIR, 'financial', 'instructions', 'ins_cl.txt'),
                    "NoncurrentLiabilities": os.path.join(settings.BASE_DIR, 'financial', 'instructions', 'ins_ncl.txt'),
                    "NetWorth": os.path.join(settings.BASE_DIR, 'financial', 'instructions', 'ins_nw.txt')
                }

                # Create or get the assistant and process as before
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

                all_messages = []

                # Process each set of instructions
                for key, instructions_file in instructions_files.items():
                    with open(instructions_file, 'r') as file:
                        instructions = file.read()

                    client.beta.assistants.update(
                        assistant_id=assistant_id,
                        instructions=instructions
                    )

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

                    run = client.beta.threads.runs.create_and_poll(
                        thread_id=thread.id, assistant_id=assistant_id
                    )

                    messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))
                    all_messages.extend(messages)
                print(all_messages)
                '''for msg in all_messages:
                    for content in msg.content:
                            
                        for c in content:
                                
                            for d in c[1]:
                                print(d[1])
                                f=d[1]'''
                all_data=[]
                for msg in all_messages:
                    for content in msg.content:
                        # Extract the text content
                        text_content = content.text.value

                        # Load the JSON data from the text content
                        data = json.loads(text_content)
                        all_data.append(data)

                        # Print the parsed JSON data
                        #print(json.dumps(data, indent=4)) 
                        #works perfectly till here
               #print(all_data)


                #block to extract totals


                
                def convert_to_float(value):
                    return float(value.replace(',', ''))

                for b in all_data:
                    #print(b)
                    for key in b:
                        if key == 'CurrentAssets':
                            total_current_assets = convert_to_float(b[key]['TotalCurrentAssets']['value'])
                            Cash=convert_to_float(b[key]['Cash']['value'])
                            TradeReceivables=convert_to_float(b[key]['TradeReceivables']['value'])
                            OtherNonTradeReceivables=convert_to_float(b[key]['OtherNonTradeReceivables']['value'])
                            FinishedGoods=convert_to_float(b[key]['FinishedGoods']['value'])
                            CurrentPortionOfPrepaidAndDeferredAssets=convert_to_float(b[key]['CurrentPortionOfPrepaidAndDeferredAssets']['value'])
                            
                            # Sum all the values in CurrentAssets
                            sum_current_assets = Cash +TradeReceivables+OtherNonTradeReceivables+FinishedGoods+CurrentPortionOfPrepaidAndDeferredAssets
                            
                            print(f"Total Current Assets: {sum_current_assets}")
                            print(total_current_assets)

                            if total_current_assets==sum_current_assets:
                                  pass
                            else:
                                  break
                                  
                                  
                        elif key == 'NonCurrentAssets':
                            total_noncurrent_assets = convert_to_float(b[key]['TotalNonCurrentAssets']['value'])

                            construction_in_progress = convert_to_float(b[key]['ConstructionInProgress']['value'])
                            machinery_and_equipment = convert_to_float(b[key]['MachineryAndEquipment']['value'])
                            operating_leases = convert_to_float(b[key]['OperatingLeases']['value'])
                            accumulated_depreciation_and_impairment = convert_to_float(b[key]['AccumulatedDepreciationAndImpairment']['value'])
                            long_term_portion_of_derivative_assets = convert_to_float(b[key]['LongTermPortionOfDerivativeAssets']['value'])
                            nonoperating_noncurrent_assets = convert_to_float(b[key]['NonoperatingNoncurrentAssets']['value'])
                            intangible_assets = convert_to_float(b[key]['IntangibleAssets']['value'])
                            accumulated_amortization_and_impairment = convert_to_float(b[key]['AccumulatedAmortizationAndImpairment']['value'])

                            # Sum all the values in NonCurrentAssets
                            sum_non_current_assets = (construction_in_progress +machinery_and_equipment +operating_leases +accumulated_depreciation_and_impairment +long_term_portion_of_derivative_assets +nonoperating_noncurrent_assets +intangible_assets +accumulated_amortization_and_impairment
)
                            print(f"Total Non-Current Assets: {sum_non_current_assets}")
                            print(total_noncurrent_assets)

                        elif key == 'CurrentLiabilities':
                            total_current_liabilities = convert_to_float(b[key]['TotalCurrentLiabilities']['value'])
                            shortterm_loans_payable = convert_to_float(b[key]['ShorttermLoansPayable']['value'])
                            current_portion_of_operating_lease_obligations = convert_to_float(b[key]['CurrentPortionOfOperatingLeaseObligations']['value'])
                            trade_accounts_payable = convert_to_float(b[key]['TradeAccountsPayable']['value'])
                            other_accruals = convert_to_float(b[key]['OtherAccruals']['value'])
                            other_taxes_payable = convert_to_float(b[key]['OtherTaxesPayable']['value'])
                            income_taxes_payable = convert_to_float(b[key]['IncomeTaxesPayable']['value'])
                            current_portion_of_derivative_liabilities = convert_to_float(b[key]['CurrentPortionOfDerivativeLiabilities']['value'])

                            # Sum all the values in CurrentLiabilities
                            sum_current_liabilities = shortterm_loans_payable + current_portion_of_operating_lease_obligations +trade_accounts_payable +other_accruals +other_taxes_payable +income_taxes_payable +current_portion_of_derivative_liabilities 
                            print(f"Total Current Liabilities: {sum_current_liabilities}")
                            print(total_current_liabilities)

                        elif key == 'NonCurrentLiabilities':
                            total_non_current_liabilities=convert_to_float(b[key]['TotalNonCurrentLiabilities']['value'])
                            LongTermBankDebt=convert_to_float(b[key]['LongTermBankDebt']['value']) 
                            LongTermPortionOfOperatingLeaseObligations=convert_to_float(b[key]['LongTermPortionOfOperatingLeaseObligations']['value']) 
                            LongTermPortionOfDerivativeLiabilities=convert_to_float(b[key]['LongTermPortionOfDerivativeLiabilities']['value']) 
                            NonOperatingNonCurrentLiabilities=convert_to_float(b[key]['NonOperatingNonCurrentLiabilities']['value']) 
                            LongTermPortionOfLoansFromRelatedCompanies=convert_to_float(b[key]['LongTermPortionOfLoansFromRelatedCompanies']['value']) 
                            LongTermPortionOfDeferredFederalIncomeTax=convert_to_float(b[key]['LongTermPortionOfDeferredFederalIncomeTax']['value'])
                           
                            # Sum all the values in NonCurrentLiabilities
                            sum_non_current_liabilities = LongTermBankDebt+LongTermPortionOfOperatingLeaseObligations+LongTermPortionOfDerivativeLiabilities+NonOperatingNonCurrentLiabilities+LongTermPortionOfLoansFromRelatedCompanies+LongTermPortionOfDeferredFederalIncomeTax
                            print(f"Total Non-Current Liabilities: {sum_non_current_liabilities}")
                            print(total_non_current_liabilities)

                        elif key == 'NetWorth':
                            total_net_worth = convert_to_float(b[key]['TotalNetWorth']['value'])
                           
                            common_stock = convert_to_float(b[key]['CommonStock']['value'])
                            paid_in_capital = convert_to_float(b[key]['PaidInCapital']['value'])
                            retained_earnings = convert_to_float(b[key]['RetainedEarnings']['value'])

                            # Sum all the values in NetWorth
                            sum_net_worth = (
                                common_stock +
                                paid_in_capital +
                                retained_earnings
                            )
                            print(f"Total Net Worth: {sum_net_worth}")
                            print(total_net_worth)


                                #new code here
                       

                    


                return Response(all_messages, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
