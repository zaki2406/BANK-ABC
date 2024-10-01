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
'''

def convert_to_float(value):
    if value == '-' or value is None:
        return 0.0  # Return a default value for invalid entries
    try:
        return float(value.replace(',', ''))  # Remove commas and convert to float
    except ValueError:
        return 0.0  # Handle any other conversion errors'''


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
                    
                    
                    #list all assistants
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
                    years=[2022,2023]

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
                        for year in years:

                            thread = client.beta.threads.create(
                                messages=[
                                    {
                                        "role": "user",
                                        "content": f"{key.lower().replace('_', ' ')} breakdown for {year}",
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
                    print(all_data)


# Extract values for 2022 and 2023------------------------------------------------------------------------
                    current_assets_2022, current_assets_2023 = {}, {}
                    non_current_assets_2022, non_current_assets_2023 = {}, {}
                    current_liabilities_2022, current_liabilities_2023 = {}, {}
                    non_current_liabilities_2022, non_current_liabilities_2023 = {}, {}
                    net_worth_2022, net_worth_2023 = {}, {}

                    for entry in all_data:
                        if 'CurrentAssets' in entry:
                            assets = entry['CurrentAssets']
                            if assets['Cash']['year'] == 2022:
                                current_assets_2022 = assets
                            elif assets['Cash']['year'] == 2023:
                                current_assets_2023 = assets
                        elif 'NonCurrentAssets' in entry:
                            assets = entry['NonCurrentAssets']
                            if assets['ConstructionInProgress']['year'] == 2022:
                                non_current_assets_2022 = assets
                            elif assets['ConstructionInProgress']['year'] == 2023:
                                non_current_assets_2023 = assets
                        elif 'CurrentLiabilities' in entry:
                            liabilities = entry['CurrentLiabilities']
                            if liabilities['ShorttermLoansPayable']['year'] == 2022:
                                current_liabilities_2022 = liabilities
                            elif liabilities['ShorttermLoansPayable']['year'] == 2023:
                                current_liabilities_2023 = liabilities
                        elif 'NonCurrentLiabilities' in entry:
                            liabilities = entry['NonCurrentLiabilities']
                            if liabilities['LongTermBankDebt']['year'] == 2022:
                                non_current_liabilities_2022 = liabilities
                            elif liabilities['LongTermBankDebt']['year'] == 2023:
                                non_current_liabilities_2023 = liabilities
                        elif 'NetWorth' in entry:
                            net_worth = entry['NetWorth']
                            if net_worth['CommonStock']['year'] == 2022:
                                net_worth_2022 = net_worth
                            elif net_worth['CommonStock']['year'] == 2023:
                                net_worth_2023 = net_worth

                    def extract_values(data):
                        return {key: details['value'] for key, details in data.items()}

                    # Extract values from all dictionaries
                    current_assets_2022_values = extract_values(current_assets_2022)
                    current_assets_2023_values = extract_values(current_assets_2023)
                    non_current_assets_2022_values = extract_values(non_current_assets_2022)
                    non_current_assets_2023_values = extract_values(non_current_assets_2023)
                    current_liabilities_2022_values = extract_values(current_liabilities_2022)
                    current_liabilities_2023_values = extract_values(current_liabilities_2023)
                    non_current_liabilities_2022_values = extract_values(non_current_liabilities_2022)
                    non_current_liabilities_2023_values = extract_values(non_current_liabilities_2023)
                    net_worth_2022_values = extract_values(net_worth_2022)
                    net_worth_2023_values = extract_values(net_worth_2023)


# Helper function to sum subfields, excluding total fields---------------------------
                    def sum_subfields(data, exclude_field):
                        total_sum = 0.0
                        for key, value in data.items():
                            if key != exclude_field:
                                total_sum += convert_to_float(value['value'])
                        return total_sum

# Calculate sums for 2022 and 2023---------------------------------------------------------------------------------
                    current_assets_sum_2022 = sum_subfields(current_assets_2022, 'TotalCurrentAssets')
                    non_current_assets_sum_2022 = sum_subfields(non_current_assets_2022, 'TotalNonCurrentAssets')
                    current_liabilities_sum_2022 = sum_subfields(current_liabilities_2022, 'TotalCurrentLiabilities')
                    non_current_liabilities_sum_2022 = sum_subfields(non_current_liabilities_2022, 'TotalNonCurrentLiabilities')
                    net_worth_sum_2022 = sum_subfields(net_worth_2022, 'TotalNetWorth')

                    current_assets_sum_2023 = sum_subfields(current_assets_2023, 'TotalCurrentAssets')
                    non_current_assets_sum_2023 = sum_subfields(non_current_assets_2023, 'TotalNonCurrentAssets')
                    current_liabilities_sum_2023 = sum_subfields(current_liabilities_2023, 'TotalCurrentLiabilities')
                    non_current_liabilities_sum_2023 = sum_subfields(non_current_liabilities_2023, 'TotalNonCurrentLiabilities')
                    net_worth_sum_2023 = sum_subfields(net_worth_2023, 'TotalNetWorth')



                    total_current_assets_2022 = total_current_assets_2023 = 0
                    total_non_current_assets_2022 = total_non_current_assets_2023 = 0
                    total_current_liabilities_2022 = total_current_liabilities_2023 = 0
                    total_non_current_liabilities_2022 = total_non_current_liabilities_2023 = 0
                    total_net_worth_2022 = total_net_worth_2023 = 0

# Extract total fields from all_data-------------------------------------------------------------------------
                    for record in all_data:
                        if 'CurrentAssets' in record:
                            assets = record['CurrentAssets']
                            if assets['TotalCurrentAssets']['year'] == 2022:
                                total_current_assets_2022 = convert_to_float(assets['TotalCurrentAssets']['value'])
                            elif assets['TotalCurrentAssets']['year'] == 2023:
                                total_current_assets_2023 = convert_to_float(assets['TotalCurrentAssets']['value'])
                        elif 'NonCurrentAssets' in record:
                            assets = record['NonCurrentAssets']
                            if assets['TotalNonCurrentAssets']['year'] == 2022:
                                total_non_current_assets_2022 = convert_to_float(assets['TotalNonCurrentAssets']['value'])
                            elif assets['TotalNonCurrentAssets']['year'] == 2023:
                                total_non_current_assets_2023 = convert_to_float(assets['TotalNonCurrentAssets']['value'])
                        elif 'CurrentLiabilities' in record:
                            liabilities = record['CurrentLiabilities']
                            if liabilities['TotalCurrentLiabilities']['year'] == 2022:
                                total_current_liabilities_2022 = convert_to_float(liabilities['TotalCurrentLiabilities']['value'])
                            elif liabilities['TotalCurrentLiabilities']['year'] == 2023:
                                total_current_liabilities_2023 = convert_to_float(liabilities['TotalCurrentLiabilities']['value'])
                        elif 'NonCurrentLiabilities' in record:
                            liabilities = record['NonCurrentLiabilities']
                            if liabilities['TotalNonCurrentLiabilities']['year'] == 2022:
                                total_non_current_liabilities_2022 = convert_to_float(liabilities['TotalNonCurrentLiabilities']['value'])
                            elif liabilities['TotalNonCurrentLiabilities']['year'] == 2023:
                                total_non_current_liabilities_2023 = convert_to_float(liabilities['TotalNonCurrentLiabilities']['value'])
                        elif 'NetWorth' in record:
                            net_worth = record['NetWorth']
                            if net_worth['TotalNetWorth']['year'] == 2022:
                                total_net_worth_2022 = convert_to_float(net_worth['TotalNetWorth']['value'])
                            elif net_worth['TotalNetWorth']['year'] == 2023:
                                total_net_worth_2023 = convert_to_float(net_worth['TotalNetWorth']['value'])

                    print(total_current_assets_2022,current_assets_sum_2022,total_current_assets_2023,current_assets_sum_2023)

#PRECISION------------------------------------------
                    

#Precision END ------------------------------------------
                    def extract_values(da):
                        return {key: details['value'] for key, details in da.items()}

                    # Extract values from all dictionaries
                    current_assets_2022_values = extract_values(current_assets_2022)
                    current_assets_2023_values = extract_values(current_assets_2023)
                    non_current_assets_2022_values = extract_values(non_current_assets_2022)
                    non_current_assets_2023_values = extract_values(non_current_assets_2023)
                    current_liabilities_2022_values = extract_values(current_liabilities_2022)
                    current_liabilities_2023_values = extract_values(current_liabilities_2023)
                    non_current_liabilities_2022_values = extract_values(non_current_liabilities_2022)
                    non_current_liabilities_2023_values = extract_values(non_current_liabilities_2023)
                    net_worth_2022_values = extract_values(net_worth_2022)
                    net_worth_2023_values = extract_values(net_worth_2023)

                    print(current_assets_2022_values)

#extract individual values and sending it to prompts::    
                    def assign_variables(data, suffix):
                        for key, value in data.items():
                            globals()[f"{key}_{suffix}"] = value

                    assign_variables(current_assets_2022_values, '2022')
                    assign_variables(current_assets_2023_values, '2023')
                    assign_variables(non_current_assets_2022_values, '2022')
                    assign_variables(non_current_assets_2023_values, '2023')
                    assign_variables(current_liabilities_2022_values, '2022')
                    assign_variables(current_liabilities_2023_values, '2023')
                    assign_variables(non_current_liabilities_2022_values, '2022')
                    assign_variables(non_current_liabilities_2023_values, '2023')
                    assign_variables(net_worth_2022_values, '2022')
                    assign_variables(net_worth_2023_values, '2023')


                    unique_prompts1={}
                    unique_prompts1["current_assets_2022"]=unique_prompts["current_assets_2022"].format(
                        Cash_2022=Cash_2022,
                        TradeReceivables_2022=TradeReceivables_2022,
                        OtherNonTradeReceivables_2022=OtherNonTradeReceivables_2022,
                        FinishedGoods_2022=FinishedGoods_2022,
                        CurrentPortionOfPrepaidAndDeferredAssets_2022=CurrentPortionOfPrepaidAndDeferredAssets_2022,
                        TotalCurrentAssets_2022=TotalCurrentAssets_2022
                    )
                    unique_prompts1["current_assets_2023"]=unique_prompts["current_assets_2023"].format(
                        Cash_2023=Cash_2023,
                        TradeReceivables_2023=TradeReceivables_2023,
                        OtherNonTradeReceivables_2023=OtherNonTradeReceivables_2023,
                        FinishedGoods_2023=FinishedGoods_2023,
                        CurrentPortionOfPrepaidAndDeferredAssets_2023=CurrentPortionOfPrepaidAndDeferredAssets_2023,
                        TotalCurrentAssets_2023=TotalCurrentAssets_2023
                    )


                    unique_prompts1["non_current_assets_2022"]=unique_prompts["non_current_assets_2022"].format(
                        ConstructionInProgress_2022=ConstructionInProgress_2022,
                        MachineryAndEquipment_2022=MachineryAndEquipment_2022,
                        OperatingLeases_2022=OperatingLeases_2022,
                        AccumulatedDepreciationAndImpairment_2022=AccumulatedDepreciationAndImpairment_2022,
                        LongTermPortionOfDerivativeAssets_2022=LongTermPortionOfDerivativeAssets_2022,
                        NonoperatingNoncurrentAssets_2022=NonoperatingNoncurrentAssets_2022,
                        IntangibleAssets_2022=IntangibleAssets_2022,
                        AccumulatedAmortizationAndImpairment_2022=AccumulatedAmortizationAndImpairment_2022,
                        TotalNonCurrentAssets_2022=TotalNonCurrentAssets_2022
                    )

                    unique_prompts1["non_current_assets_2023"]=unique_prompts["non_current_assets_2023"].format(
                        ConstructionInProgress_2023=ConstructionInProgress_2023,
                        MachineryAndEquipment_2023=MachineryAndEquipment_2023,
                        OperatingLeases_2023=OperatingLeases_2023,
                        AccumulatedDepreciationAndImpairment_2023=AccumulatedDepreciationAndImpairment_2023,
                        LongTermPortionOfDerivativeAssets_2023=LongTermPortionOfDerivativeAssets_2023,
                        NonoperatingNoncurrentAssets_2023=NonoperatingNoncurrentAssets_2023,
                        IntangibleAssets_2023=IntangibleAssets_2023,
                        AccumulatedAmortizationAndImpairment_2023=AccumulatedAmortizationAndImpairment_2023,
                        TotalNonCurrentAssets_2023=TotalNonCurrentAssets_2023
                    )


                    unique_prompts1["current_liabilities_2022"]=unique_prompts["current_liabilities_2022"].format(
                        ShorttermLoansPayable_2022=ShorttermLoansPayable_2022,
                        CurrentPortionOfOperatingLeaseObligations_2022=CurrentPortionOfOperatingLeaseObligations_2022,
                        TradeAccountsPayable_2022=TradeAccountsPayable_2022,
                        OtherAccruals_2022=OtherAccruals_2022,
                        OtherTaxesPayable_2022=OtherTaxesPayable_2022,
                        IncomeTaxesPayable_2022=IncomeTaxesPayable_2022,
                        CurrentPortionOfDerivativeLiabilities_2022=CurrentPortionOfDerivativeLiabilities_2022,
                        TotalCurrentLiabilities_2022=TotalCurrentLiabilities_2022
                    )


                    unique_prompts1["current_liabilities_2023"]=unique_prompts["current_liabilities_2023"].format(
                        ShorttermLoansPayable_2023=ShorttermLoansPayable_2023,
                        CurrentPortionOfOperatingLeaseObligations_2023=CurrentPortionOfOperatingLeaseObligations_2023,
                        TradeAccountsPayable_2023=TradeAccountsPayable_2023,
                        OtherAccruals_2023=OtherAccruals_2023,
                        OtherTaxesPayable_2023=OtherTaxesPayable_2023,
                        IncomeTaxesPayable_2023=IncomeTaxesPayable_2023,
                        CurrentPortionOfDerivativeLiabilities_2023=CurrentPortionOfDerivativeLiabilities_2023,
                        TotalCurrentLiabilities_2023=TotalCurrentLiabilities_2023
                    )


                    unique_prompts1["non_current_liabilities_2022"]=unique_prompts["non_current_liabilities_2022"].format(
                        LongTermBankDebt_2022=LongTermBankDebt_2022,
                        LongTermPortionOfOperatingLeaseObligations_2022=LongTermPortionOfOperatingLeaseObligations_2022,
                        LongTermPortionOfDerivativeLiabilities_2022=LongTermPortionOfDerivativeLiabilities_2022,
                        NonOperatingNonCurrentLiabilities_2022=NonOperatingNonCurrentLiabilities_2022,
                        LongTermPortionOfLoansFromRelatedCompanies_2022=LongTermPortionOfLoansFromRelatedCompanies_2022,
                        LongTermPortionOfDeferredFederalIncomeTax_2022=LongTermPortionOfDeferredFederalIncomeTax_2022,
                        TotalNonCurrentLiabilities_2022=TotalNonCurrentLiabilities_2022
                    )


                    unique_prompts1["non_current_liabilities_2023"]=unique_prompts["non_current_liabilities_2023"].format(
                        LongTermBankDebt_2023=LongTermBankDebt_2023,
                        LongTermPortionOfOperatingLeaseObligations_2023=LongTermPortionOfOperatingLeaseObligations_2023,
                        LongTermPortionOfDerivativeLiabilities_2023=LongTermPortionOfDerivativeLiabilities_2023,
                        NonOperatingNonCurrentLiabilities_2023=NonOperatingNonCurrentLiabilities_2023,
                        LongTermPortionOfLoansFromRelatedCompanies_2023=LongTermPortionOfLoansFromRelatedCompanies_2023,
                        LongTermPortionOfDeferredFederalIncomeTax_2023=LongTermPortionOfDeferredFederalIncomeTax_2023,
                        TotalNonCurrentLiabilities_2023=TotalNonCurrentLiabilities_2023
                    )


                    unique_prompts1["net_worth_2022"]=unique_prompts["net_worth_2022"].format(
                        CommonStock_2022=CommonStock_2022,
                        PaidInCapital_2022=PaidInCapital_2022,
                        RetainedEarnings_2022=RetainedEarnings_2022,
                        TotalNetWorth_2022=TotalNetWorth_2022
                    )

                    unique_prompts1["net_worth_2023"]=unique_prompts["net_worth_2023"].format(
                        CommonStock_2023=CommonStock_2023,
                        PaidInCapital_2023=PaidInCapital_2023,
                        RetainedEarnings_2023=RetainedEarnings_2023,
                        TotalNetWorth_2023=TotalNetWorth_2023
                    )






                    mismatches=[]
                    if total_current_assets_2022 != current_assets_sum_2022:
                        mismatches.append("current_assets_2022")
                    if total_current_assets_2023 != current_assets_sum_2023:
                        mismatches.append("current_assets_2023")

                    # Compare non-current assets
                    if total_non_current_assets_2022 != non_current_assets_sum_2022:
                        mismatches.append("non_current_assets_2022")
                    if total_non_current_assets_2023 != non_current_assets_sum_2023:
                        mismatches.append("non_current_assets_2023")

                    # Compare current liabilities
                    if total_current_liabilities_2022 != current_liabilities_sum_2022:
                        mismatches.append("current_liabilities_2022")
                    if total_current_liabilities_2023 != current_liabilities_sum_2023:
                        mismatches.append("current_liabilities_2023")

                    # Compare non-current liabilities
                    if total_non_current_liabilities_2022 != non_current_liabilities_sum_2022:
                        mismatches.append("non_current_liabilities_2022")
                    if total_non_current_liabilities_2023 != non_current_liabilities_sum_2023:
                        mismatches.append("non_current_liabilities_2023")

                    # Compare net worth
                    if total_net_worth_2022 != net_worth_sum_2022:
                        mismatches.append("net_worth_2022")
                    if total_net_worth_2023 != net_worth_sum_2023:
                        mismatches.append("net_worth_2023")


                     #Send unique prompts for each mismatch
                    mall_messages=[] 
                    for mismatch_type in mismatches:
                        
                        update_prompt = unique_prompts1[mismatch_type]

                        # Send the update to OpenAI with your unique prompt
                        client.beta.assistants.update(
                            assistant_id=assistant_id,
                            instructions=update_prompt
                        )

                        thread = client.beta.threads.create(
                                messages=[
                                    {
                                        "role": "user",
                                        "content":update_prompt,
                                        "attachments": [
                                            {"file_id": message_file.id, "tools": [{"type": "file_search"}]}
                                        ],
                                    }
                                ]
                            )
                        run = client.beta.threads.runs.create_and_poll(
                            thread_id=thread.id,assistant_id=assistant_id
                            )
                        mmessages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))
                        
                        
                        mall_messages.extend(mmessages)
                        
                    print(mall_messages)

                    for msg in mall_messages:
                        for content in msg.content:
                            # Extract the text content
                            text_content = content.text.value

                            # Load the JSON data from the text content
                            data = json.loads(text_content)
                            all_data.append(data)
                    print(all_data)

                    print("Mismatches found:", mismatches)

                    for entry in all_data:
                        if 'CurrentAssets' in entry:
                            assets = entry['CurrentAssets']
                            if assets['Cash']['year'] == 2022:
                                current_assets_2022 = assets
                                print(current_assets_2022)
                            elif assets['Cash']['year'] == 2023:
                                current_assets_2023 = assets
                                print(current_assets_2023)
                        elif 'NonCurrentAssets' in entry:
                            assets = entry['NonCurrentAssets']
                            if assets['ConstructionInProgress']['year'] == 2022:
                                non_current_assets_2022 = assets
                                print(non_current_assets_2022)
                            elif assets['ConstructionInProgress']['year'] == 2023:
                                non_current_assets_2023 = assets
                                print(non_current_assets_2023)
                        elif 'CurrentLiabilities' in entry:
                            liabilities = entry['CurrentLiabilities']
                            if liabilities['ShorttermLoansPayable']['year'] == 2022:
                                current_liabilities_2022 = liabilities
                                print(current_liabilities_2022)
                            elif liabilities['ShorttermLoansPayable']['year'] == 2023:
                                current_liabilities_2023 = liabilities
                                print(current_liabilities_2023)
                        elif 'NonCurrentLiabilities' in entry:
                            liabilities = entry['NonCurrentLiabilities']
                            if liabilities['LongTermBankDebt']['year'] == 2022:
                                non_current_liabilities_2022 = liabilities
                                print(non_current_liabilities_2022)
                            elif liabilities['LongTermBankDebt']['year'] == 2023:
                                non_current_liabilities_2023 = liabilities
                                print(non_current_liabilities_2023)
                        elif 'NetWorth' in entry:
                            net_worth = entry['NetWorth']
                            if net_worth['CommonStock']['year'] == 2022:
                                net_worth_2022 = net_worth
                                print(net_worth_2022)
                            elif net_worth['CommonStock']['year'] == 2023:
                                net_worth_2023 = net_worth
                                print(net_worth_2023)
                    


                    current_assets_sum_2022 = sum_subfields(current_assets_2022, 'TotalCurrentAssets')
                    non_current_assets_sum_2022 = sum_subfields(non_current_assets_2022, 'TotalNonCurrentAssets')
                    current_liabilities_sum_2022 = sum_subfields(current_liabilities_2022, 'TotalCurrentLiabilities')
                    non_current_liabilities_sum_2022 = sum_subfields(non_current_liabilities_2022, 'TotalNonCurrentLiabilities')
                    net_worth_sum_2022 = sum_subfields(net_worth_2022, 'TotalNetWorth')

                    current_assets_sum_2023 = sum_subfields(current_assets_2023, 'TotalCurrentAssets')
                    non_current_assets_sum_2023 = sum_subfields(non_current_assets_2023, 'TotalNonCurrentAssets')
                    current_liabilities_sum_2023 = sum_subfields(current_liabilities_2023, 'TotalCurrentLiabilities')
                    non_current_liabilities_sum_2023 = sum_subfields(non_current_liabilities_2023, 'TotalNonCurrentLiabilities')
                    net_worth_sum_2023 = sum_subfields(net_worth_2023, 'TotalNetWorth')

                    Mismatch_CA_2022=total_current_assets_2022-current_assets_sum_2022
                    Mismatch_CA_2023=total_current_assets_2023-current_assets_sum_2023
                    Mismatch_NCA_2022=total_non_current_assets_2022-non_current_assets_sum_2022
                    Mismatch_NCA_2023=total_non_current_assets_2023-non_current_assets_sum_2023
                    Mismatch_CL_2022=total_current_liabilities_2022-current_liabilities_sum_2022
                    Mismatch_CL_2023=total_current_liabilities_2023-current_liabilities_sum_2023
                    Mismatch_NCL_2022=total_non_current_liabilities_2022-non_current_liabilities_sum_2022
                    Mismatch_NCL_2023=total_non_current_liabilities_2023-non_current_liabilities_sum_2023
                    Mismatch_NW_2022=total_net_worth_2022-net_worth_sum_2022
                    Mismatch_NW_2023=total_net_worth_2023-net_worth_sum_2023
                    print(Mismatch_CA_2022,'Mismatch_CA_2022')

                

                    
                  
#Precision END ------------------------------------------





                 
                        
                        

                    # Print results or handle the response as needed
                    
                    
                    current_assets_2022['mismatch']={'value': str(Mismatch_CA_2022),'year':2022}
                    current_assets_2023['mismatch']={'value': str(Mismatch_CA_2023),'year':2022}
                    non_current_assets_2022['mismatch']={'value': str(Mismatch_NCA_2022),'year':2022}
                    non_current_assets_2023['mismatch']={'value': str(Mismatch_NCA_2023),'year':2022}
                    current_liabilities_2022['mismatch']={'value': str(Mismatch_CL_2022),'year':2022}
                    current_liabilities_2023['mismatch']={'value': str(Mismatch_CL_2023),'year':2022}
                    non_current_liabilities_2022['mismatch']={'value': str(Mismatch_NCL_2022),'year':2022}
                    non_current_liabilities_2023['mismatch']={'value': str(Mismatch_NCL_2023),'year':2022}
                    net_worth_2022['mismatch']={'value': str(Mismatch_NW_2022),'year':2022}
                    net_worth_2023['mismatch']={'value': str(Mismatch_NW_2023),'year':2022}

                    print("\n Mismatches found:", mismatches)
                    print("\n Current Assets 2022:", current_assets_2022)
                    print("\n Current Assets 2023:", current_assets_2023)
                    print("\n Non-Current Assets 2022:", non_current_assets_2022)
                    print("\n Non-Current Assets 2023:", non_current_assets_2023)
                    print("\n Current Liabilities 2022:", current_liabilities_2022)
                    print("\n Current Liabilities 2023:", current_liabilities_2023)
                    print("\n Non-Current Liabilities 2022:", non_current_liabilities_2022)
                    print("\n Non-Current Liabilities 2023:", non_current_liabilities_2023)
                    print("\n Net Worth 2022:", net_worth_2022)
                    print("\n Net Worth 2023:", net_worth_2023)

                    
                    def replace_fields(data1):
                        precision_mapping = {
                            ('true', 'true'): 'high',
                            ('true', 'false'): 'mid',
                            ('false', 'true'): 'mid',
                            ('false', 'false'): 'low',
                        }

                        for k, details in data1.items():
                            if isinstance(details, dict):  # Ensure it's a dictionary
                                terminology = details.get('TerminologyInterpretation', None)
                                calculation = details.get('CalculationRequired', None)

                                # Determine precision
                                precision_value = precision_mapping.get((str(terminology).lower(), str(calculation).lower()))

                                # Replace the fields
                                details['precision'] = precision_value

                                # Remove the old fields if they exist
                                details.pop('TerminologyInterpretation', None)
                                details.pop('CalculationRequired', None)
                            else:
                                print(f"Skipping non-dictionary entry for key '{k}' with value: {details}")

                        return data1





                    current_assets_2022 = replace_fields(current_assets_2022)
                    current_assets_2023 = replace_fields(current_assets_2023)
                    non_current_assets_2022 = replace_fields(non_current_assets_2022)
                    non_current_assets_2023 = replace_fields(non_current_assets_2023)
                    current_liabilities_2022 = replace_fields(current_liabilities_2022)
                    current_liabilities_2023 = replace_fields(current_liabilities_2023)
                    non_current_liabilities_2022 = replace_fields(non_current_liabilities_2022)
                    non_current_liabilities_2023 = replace_fields(non_current_liabilities_2023)
                    net_worth_2022 = replace_fields(net_worth_2022)
                    net_worth_2023 = replace_fields(net_worth_2023)
                    print(current_assets_2022)

                    #combining the data into required json structure



                    def combine_assets(year_2022, year_2023):
                        combined = []
                        for key, value in year_2022.items():
                            combined.append({key: value})
                        for key, value in year_2023.items():
                            combined.append({key: value})
                        return combined

                    # Combine all categories
                    combined_data = {
                        'CurrentAssets': combine_assets(current_assets_2022, current_assets_2023),
                        'NonCurrentAssets': combine_assets(non_current_assets_2022, non_current_assets_2023),
                        'CurrentLiabilities': combine_assets(current_liabilities_2022, current_liabilities_2023),
                        'NonCurrentLiabilities': combine_assets(non_current_liabilities_2022, non_current_liabilities_2023),
                        'NetWorth': combine_assets(net_worth_2022, net_worth_2023)
                    }

                    # Convert to JSON
                    json_output = json.dumps(combined_data, indent=2)

                    # Print the JSON
                    print(json_output)


            

       

            

                    

                    return JsonResponse(combined_data, status=status.HTTP_200_OK)


                except Exception as e:
                    logging.error(f"Error during file processing: {str(e)}")

                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




