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
                            

                            client.beta.assistants.update(
                                assistant_id=assistant_id,
                                instructions=a
                            )

                            
                                    
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
                    

                    all_data=[]
                    for msg in all_messages:
                        for content in msg.content:
                            # Extract the text content
                            text_content = content.text.value

                            # Load the JSON data from the text content
                            data = json.loads(text_content)
                            all_data.append(data)
                    #print(all_data)
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
                    '''   
                    # Now each of the dictionaries will contain the data for the respective years
                    print("Current Assets 2022:", current_assets_2022)
                    print("Current Assets 2023:", current_assets_2023)
                    print("Non-Current Assets 2022:", non_current_assets_2022)
                    print("Non-Current Assets 2023:", non_current_assets_2023)
                    print("Current Liabilities 2022:", current_liabilities_2022)
                    print("Current Liabilities 2023:", current_liabilities_2023)
                    print("Non-Current Liabilities 2022:", non_current_liabilities_2022)
                    print("Non-Current Liabilities 2023:", non_current_liabilities_2023)
                    print("Net Worth 2022:", net_worth_2022)
                    print("Net Worth 2023:", net_worth_2023)
                    '''

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
                    '''
                    print("Current Assets 2022:", current_assets_2022_values)
                    print("Current Assets 2023:", current_assets_2023_values)
                    print("Non-Current Assets 2022:", non_current_assets_2022_values)
                    print("Non-Current Assets 2023:", non_current_assets_2023_values)
                    print("Current Liabilities 2022:", current_liabilities_2022_values)
                    print("Current Liabilities 2023:", current_liabilities_2023_values)
                    print("Non-Current Liabilities 2022:", non_current_liabilities_2022_values)
                    print("Non-Current Liabilities 2023:", non_current_liabilities_2023_values)
                    print("Net Worth 2022:", net_worth_2022_values)
                    print("Net Worth 2023:", net_worth_2023_values)
                    '''

                    def sum_subfields(data, exclude_field):
                        total_sum = 0.0
                        for key, value in data.items():
                            if key != exclude_field:
                                total_sum += convert_to_float(value['value'])
                        return total_sum
                    
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

                    for record in all_data:
                        if 'CurrentAssets' in record:
                            assets = record['CurrentAssets']
                            if 'TotalCurrentAssets' in assets and assets['TotalCurrentAssets'].get('year') == 2022:
                                total_current_assets_2022 = convert_to_float(assets['TotalCurrentAssets']['value'])
                            elif 'TotalCurrentAssets' in assets and assets['TotalCurrentAssets'].get('year') == 2023:
                                total_current_assets_2023 = convert_to_float(assets['TotalCurrentAssets']['value'])
                        
                        if 'NonCurrentAssets' in record:
                            assets = record['NonCurrentAssets']
                            if 'TotalNonCurrentAssets' in assets and assets['TotalNonCurrentAssets'].get('year') == 2022:
                                total_non_current_assets_2022 = convert_to_float(assets['TotalNonCurrentAssets']['value'])
                            elif 'TotalNonCurrentAssets' in assets and assets['TotalNonCurrentAssets'].get('year') == 2023:
                                total_non_current_assets_2023 = convert_to_float(assets['TotalNonCurrentAssets']['value'])
                        
                        if 'CurrentLiabilities' in record:
                            liabilities = record['CurrentLiabilities']
                            if 'TotalCurrentLiabilities' in liabilities and liabilities['TotalCurrentLiabilities'].get('year') == 2022:
                                total_current_liabilities_2022 = convert_to_float(liabilities['TotalCurrentLiabilities']['value'])
                            elif 'TotalCurrentLiabilities' in liabilities and liabilities['TotalCurrentLiabilities'].get('year') == 2023:
                                total_current_liabilities_2023 = convert_to_float(liabilities['TotalCurrentLiabilities']['value'])
                        
                        if 'NonCurrentLiabilities' in record:
                            liabilities = record['NonCurrentLiabilities']
                            if 'TotalNonCurrentLiabilities' in liabilities and liabilities['TotalNonCurrentLiabilities'].get('year') == 2022:
                                total_non_current_liabilities_2022 = convert_to_float(liabilities['TotalNonCurrentLiabilities']['value'])
                            elif 'TotalNonCurrentLiabilities' in liabilities and liabilities['TotalNonCurrentLiabilities'].get('year') == 2023:
                                total_non_current_liabilities_2023 = convert_to_float(liabilities['TotalNonCurrentLiabilities']['value'])
                        
                        if 'NetWorth' in record:
                            net_worth = record['NetWorth']
                            if 'TotalNetWorth' in net_worth and net_worth['TotalNetWorth'].get('year') == 2022:
                                total_net_worth_2022 = convert_to_float(net_worth['TotalNetWorth']['value'])
                            elif 'TotalNetWorth' in net_worth and net_worth['TotalNetWorth'].get('year') == 2023:
                                total_net_worth_2023 = convert_to_float(net_worth['TotalNetWorth']['value'])
                    
                    '''
                    # Now check if the variables exist before printing them
                    try:
                        print("Total Current Assets 2022:", total_current_assets_2022)
                    except NameError:
                        print("Total Current Assets 2022: Data not found")
                    
                    try:
                        print("Total Current Assets 2023:", total_current_assets_2023)
                    except NameError:
                        print("Total Current Assets 2023: Data not found")
                    
                    try:
                        print("Total Non-Current Assets 2022:", total_non_current_assets_2022)
                    except NameError:
                        print("Total Non-Current Assets 2022: Data not found")
                    
                    try:
                        print("Total Non-Current Assets 2023:", total_non_current_assets_2023)
                    except NameError:
                        print("Total Non-Current Assets 2023: Data not found")
                    
                    try:
                        print("Total Current Liabilities 2022:", total_current_liabilities_2022)
                    except NameError:
                        print("Total Current Liabilities 2022: Data not found")
                    
                    try:
                        print("Total Current Liabilities 2023:", total_current_liabilities_2023)
                    except NameError:
                        print("Total Current Liabilities 2023: Data not found")
                    
                    try:
                        print("Total Non-Current Liabilities 2022:", total_non_current_liabilities_2022)
                    except NameError:
                        print("Total Non-Current Liabilities 2022: Data not found")
                    
                    try:
                        print("Total Non-Current Liabilities 2023:", total_non_current_liabilities_2023)
                    except NameError:
                        print("Total Non-Current Liabilities 2023: Data not found")
                    
                    try:
                        print("Total Net Worth 2022:", total_net_worth_2022)
                    except NameError:
                        print("Total Net Worth 2022: Data not found")
                    
                    try:
                        print("Total Net Worth 2023:", total_net_worth_2023)
                    except NameError:
                        print("Total Net Worth 2023: Data not found")
                    
                    # Print statements for summed values for 2022
                    print("Sum of Current Assets 2022:", current_assets_sum_2022)
                    print("Sum of Non-Current Assets 2022:", non_current_assets_sum_2022)
                    print("Sum of Current Liabilities 2022:", current_liabilities_sum_2022)
                    print("Sum of Non-Current Liabilities 2022:", non_current_liabilities_sum_2022)
                    print("Sum of Net Worth 2022:", net_worth_sum_2022)

                    # Print statements for summed values for 2023
                    print("Sum of Current Assets 2023:", current_assets_sum_2023)
                    print("Sum of Non-Current Assets 2023:", non_current_assets_sum_2023)
                    print("Sum of Current Liabilities 2023:", current_liabilities_sum_2023)
                    print("Sum of Non-Current Liabilities 2023:", non_current_liabilities_sum_2023)
                    print("Sum of Net Worth 2023:", net_worth_sum_2023)
                    '''


                    def assign_variables(data, suffix, default_value='0'):
                        for key, value in data.items():
                            globals()[f"{key}_{suffix}"] = convert_to_float(value) if value is not None else default_value

                    # Assign variables for existing values
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

                    # Fallback for missing variables when using or formatting them
                    total_current_assets_2022 = globals().get("TotalCurrentAssets_2022", 0)
                    total_current_assets_2023 = globals().get("TotalCurrentAssets_2023", 0)
                    total_non_current_assets_2022 = globals().get("TotalNonCurrentAssets_2022", 0)
                    total_non_current_assets_2023 = globals().get("TotalNonCurrentAssets_2023", 0)
                    total_current_liabilities_2022 = globals().get("TotalCurrentLiabilities_2022", 0)
                    total_current_liabilities_2023 = globals().get("TotalCurrentLiabilities_2023", 0)
                    total_non_current_liabilities_2022 = globals().get("TotalNonCurrentLiabilities_2022", 0)
                    total_non_current_liabilities_2023 = globals().get("TotalNonCurrentLiabilities_2023", 0)
                    total_net_worth_2022 = globals().get("TotalNetWorth_2022", 0)
                    total_net_worth_2023 = globals().get("TotalNetWorth_2023", 0)


                    unique_prompts1={}
                    

                    unique_prompts1["current_assets_2022"] = unique_prompts["current_assets_2022"].format(
                        Cash_2022=globals().get('Cash_2022', 0),
                        TradeReceivables_2022=globals().get('TradeReceivables_2022', 0),
                        OtherNonTradeReceivables_2022=globals().get('OtherNonTradeReceivables_2022', 0),
                        FinishedGoods_2022=globals().get('FinishedGoods_2022', 0),
                        CurrentPortionOfPrepaidAndDeferredAssets_2022=globals().get('CurrentPortionOfPrepaidAndDeferredAssets_2022', 0),
                        TotalCurrentAssets_2022=globals().get('TotalCurrentAssets_2022', 0)
                    )

                    unique_prompts1["current_assets_2023"] = unique_prompts["current_assets_2023"].format(
                        Cash_2023=globals().get('Cash_2023', 0),
                        TradeReceivables_2023=globals().get('TradeReceivables_2023', 0),
                        OtherNonTradeReceivables_2023=globals().get('OtherNonTradeReceivables_2023', 0),
                        FinishedGoods_2023=globals().get('FinishedGoods_2023', 0),
                        CurrentPortionOfPrepaidAndDeferredAssets_2023=globals().get('CurrentPortionOfPrepaidAndDeferredAssets_2023', 0),
                        TotalCurrentAssets_2023=globals().get('TotalCurrentAssets_2023', 0)
                    )

                    unique_prompts1["non_current_assets_2022"] = unique_prompts["non_current_assets_2022"].format(
                        ConstructionInProgress_2022=globals().get('ConstructionInProgress_2022', 0),
                        MachineryAndEquipment_2022=globals().get('MachineryAndEquipment_2022', 0),
                        OperatingLeases_2022=globals().get('OperatingLeases_2022', 0),
                        AccumulatedDepreciationAndImpairment_2022=globals().get('AccumulatedDepreciationAndImpairment_2022', 0),
                        LongTermPortionOfDerivativeAssets_2022=globals().get('LongTermPortionOfDerivativeAssets_2022', 0),
                        NonoperatingNoncurrentAssets_2022=globals().get('NonoperatingNoncurrentAssets_2022', 0),
                        IntangibleAssets_2022=globals().get('IntangibleAssets_2022', 0),
                        AccumulatedAmortizationAndImpairment_2022=globals().get('AccumulatedAmortizationAndImpairment_2022', 0),
                        TotalNonCurrentAssets_2022=globals().get('TotalNonCurrentAssets_2022', 0)
                    )

                    unique_prompts1["non_current_assets_2023"] = unique_prompts["non_current_assets_2023"].format(
                        ConstructionInProgress_2023=globals().get('ConstructionInProgress_2023', 0),
                        MachineryAndEquipment_2023=globals().get('MachineryAndEquipment_2023', 0),
                        OperatingLeases_2023=globals().get('OperatingLeases_2023', 0),
                        AccumulatedDepreciationAndImpairment_2023=globals().get('AccumulatedDepreciationAndImpairment_2023', 0),
                        LongTermPortionOfDerivativeAssets_2023=globals().get('LongTermPortionOfDerivativeAssets_2023', 0),
                        NonoperatingNoncurrentAssets_2023=globals().get('NonoperatingNoncurrentAssets_2023', 0),
                        IntangibleAssets_2023=globals().get('IntangibleAssets_2023', 0),
                        AccumulatedAmortizationAndImpairment_2023=globals().get('AccumulatedAmortizationAndImpairment_2023', 0),
                        TotalNonCurrentAssets_2023=globals().get('TotalNonCurrentAssets_2023', 0)
                    )

                    unique_prompts1["current_liabilities_2022"] = unique_prompts["current_liabilities_2022"].format(
                        ShorttermLoansPayable_2022=globals().get('ShorttermLoansPayable_2022', 0),
                        CurrentPortionOfOperatingLeaseObligations_2022=globals().get('CurrentPortionOfOperatingLeaseObligations_2022', 0),
                        TradeAccountsPayable_2022=globals().get('TradeAccountsPayable_2022', 0),
                        OtherAccruals_2022=globals().get('OtherAccruals_2022', 0),
                        OtherTaxesPayable_2022=globals().get('OtherTaxesPayable_2022', 0),
                        IncomeTaxesPayable_2022=globals().get('IncomeTaxesPayable_2022', 0),
                        CurrentPortionOfDerivativeLiabilities_2022=globals().get('CurrentPortionOfDerivativeLiabilities_2022', 0),
                        TotalCurrentLiabilities_2022=globals().get('TotalCurrentLiabilities_2022', 0)
                    )

                    unique_prompts1["current_liabilities_2023"] = unique_prompts["current_liabilities_2023"].format(
                        ShorttermLoansPayable_2023=globals().get('ShorttermLoansPayable_2023', 0),
                        CurrentPortionOfOperatingLeaseObligations_2023=globals().get('CurrentPortionOfOperatingLeaseObligations_2023', 0),
                        TradeAccountsPayable_2023=globals().get('TradeAccountsPayable_2023', 0),
                        OtherAccruals_2023=globals().get('OtherAccruals_2023', 0),
                        OtherTaxesPayable_2023=globals().get('OtherTaxesPayable_2023', 0),
                        IncomeTaxesPayable_2023=globals().get('IncomeTaxesPayable_2023', 0),
                        CurrentPortionOfDerivativeLiabilities_2023=globals().get('CurrentPortionOfDerivativeLiabilities_2023', 0),
                        TotalCurrentLiabilities_2023=globals().get('TotalCurrentLiabilities_2023', 0)
                    )

                    unique_prompts1["non_current_liabilities_2022"] = unique_prompts["non_current_liabilities_2022"].format(
                        LongTermBankDebt_2022=globals().get('LongTermBankDebt_2022', 0),
                        LongTermPortionOfOperatingLeaseObligations_2022=globals().get('LongTermPortionOfOperatingLeaseObligations_2022', 0),
                        LongTermPortionOfDerivativeLiabilities_2022=globals().get('LongTermPortionOfDerivativeLiabilities_2022', 0),
                        NonOperatingNonCurrentLiabilities_2022=globals().get('NonOperatingNonCurrentLiabilities_2022', 0),
                        LongTermPortionOfLoansFromRelatedCompanies_2022=globals().get('LongTermPortionOfLoansFromRelatedCompanies_2022', 0),
                        LongTermPortionOfDeferredFederalIncomeTax_2022=globals().get('LongTermPortionOfDeferredFederalIncomeTax_2022', 0),
                        TotalNonCurrentLiabilities_2022=globals().get('TotalNonCurrentLiabilities_2022', 0)
                    )

                    unique_prompts1["non_current_liabilities_2023"] = unique_prompts["non_current_liabilities_2023"].format(
                        LongTermBankDebt_2023=globals().get('LongTermBankDebt_2023', 0),
                        LongTermPortionOfOperatingLeaseObligations_2023=globals().get('LongTermPortionOfOperatingLeaseObligations_2023', 0),
                        LongTermPortionOfDerivativeLiabilities_2023=globals().get('LongTermPortionOfDerivativeLiabilities_2023', 0),
                        NonOperatingNonCurrentLiabilities_2023=globals().get('NonOperatingNonCurrentLiabilities_2023', 0),
                        LongTermPortionOfLoansFromRelatedCompanies_2023=globals().get('LongTermPortionOfLoansFromRelatedCompanies_2023', 0),
                        LongTermPortionOfDeferredFederalIncomeTax_2023=globals().get('LongTermPortionOfDeferredFederalIncomeTax_2023', 0),
                        TotalNonCurrentLiabilities_2023=globals().get('TotalNonCurrentLiabilities_2023', 0)
                    )

                    unique_prompts1["net_worth_2022"] = unique_prompts["net_worth_2022"].format(
                        CommonStock_2022=globals().get('CommonStock_2022', 0),
                        PaidInCapital_2022=globals().get('PaidInCapital_2022', 0),
                        RetainedEarnings_2022=globals().get('RetainedEarnings_2022', 0),
                        TotalNetWorth_2022=globals().get('TotalNetWorth_2022', 0)
                    )

                    unique_prompts1["net_worth_2023"] = unique_prompts["net_worth_2023"].format(
                        CommonStock_2023=globals().get('CommonStock_2023', 0),
                        PaidInCapital_2023=globals().get('PaidInCapital_2023', 0),
                        RetainedEarnings_2023=globals().get('RetainedEarnings_2023', 0),
                        TotalNetWorth_2023=globals().get('TotalNetWorth_2023', 0)
                    )


                    #print(unique_prompts1)

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

                    #print(mismatches)

                    mall_messages=[] 
                    for mismatch_type in mismatches:
                        update_prompt = unique_prompts1[mismatch_type]
                        print(update_prompt)
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
                    #print(mall_messages)
                    
                    mall_data=[]
                    for msg1 in mall_messages:
                        for content in msg1.content:
                            # Extract the text content
                            text_content = content.text.value

                            # Load the JSON data from the text content
                            data = json.loads(text_content)
                            mall_data.append(data)
                    

                    for entry1 in mall_data:
                        if 'CurrentAssets' in entry1:
                            assets = entry1['CurrentAssets']
                            if assets['Cash']['year'] == 2022:
                                current_assets_2022 = assets
                            elif assets['Cash']['year'] == 2023:
                                current_assets_2023 = assets
                        elif 'NonCurrentAssets' in entry1:
                            assets = entry1['NonCurrentAssets']
                            if assets['ConstructionInProgress']['year'] == 2022:
                                non_current_assets_2022 = assets
                            elif assets['ConstructionInProgress']['year'] == 2023:
                                non_current_assets_2023 = assets
                        elif 'CurrentLiabilities' in entry1:
                            liabilities = entry1['CurrentLiabilities']
                            if liabilities['ShorttermLoansPayable']['year'] == 2022:
                                current_liabilities_2022 = liabilities
                            elif liabilities['ShorttermLoansPayable']['year'] == 2023:
                                current_liabilities_2023 = liabilities
                        elif 'NonCurrentLiabilities' in entry1:
                            liabilities = entry1['NonCurrentLiabilities']
                            if liabilities['LongTermBankDebt']['year'] == 2022:
                                non_current_liabilities_2022 = liabilities
                            elif liabilities['LongTermBankDebt']['year'] == 2023:
                                non_current_liabilities_2023 = liabilities
                        elif 'NetWorth' in entry1:
                            net_worth = entry1['NetWorth']
                            if net_worth['CommonStock']['year'] == 2022:
                                net_worth_2022 = net_worth
                            elif net_worth['CommonStock']['year'] == 2023:
                                net_worth_2023 = net_worth
                    '''
                    # Now each of the dictionaries will contain the data for the respective years
                    print("Current Assets 2022:", current_assets_2022)
                    print("Current Assets 2023:", current_assets_2023)
                    print("Non-Current Assets 2022:", non_current_assets_2022)
                    print("Non-Current Assets 2023:", non_current_assets_2023)
                    print("Current Liabilities 2022:", current_liabilities_2022)
                    print("Current Liabilities 2023:", current_liabilities_2023)
                    print("Non-Current Liabilities 2022:", non_current_liabilities_2022)
                    print("Non-Current Liabilities 2023:", non_current_liabilities_2023)
                    print("Net Worth 2022:", net_worth_2022)
                    print("Net Worth 2023:", net_worth_2023)
                    '''

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
                    '''
                    # Print statements for all extracted values
                    print("Total Current Assets 2022:", total_current_assets_2022)
                    print("Total Current Assets 2023:", total_current_assets_2023)
                    print("Total Non-Current Assets 2022:", total_non_current_assets_2022)
                    print("Total Non-Current Assets 2023:", total_non_current_assets_2023)
                    print("Total Current Liabilities 2022:", total_current_liabilities_2022)
                    print("Total Current Liabilities 2023:", total_current_liabilities_2023)
                    print("Total Non-Current Liabilities 2022:", total_non_current_liabilities_2022)
                    print("Total Non-Current Liabilities 2023:", total_non_current_liabilities_2023)
                    print("Total Net Worth 2022:", total_net_worth_2022)
                    print("Total Net Worth 2023:", total_net_worth_2023)

                    # Print statements for summed values for 2022
                    print("Sum of Current Assets 2022:", current_assets_sum_2022)
                    print("Sum of Non-Current Assets 2022:", non_current_assets_sum_2022)
                    print("Sum of Current Liabilities 2022:", current_liabilities_sum_2022)
                    print("Sum of Non-Current Liabilities 2022:", non_current_liabilities_sum_2022)
                    print("Sum of Net Worth 2022:", net_worth_sum_2022)

                    # Print statements for summed values for 2023
                    print("Sum of Current Assets 2023:", current_assets_sum_2023)
                    print("Sum of Non-Current Assets 2023:", non_current_assets_sum_2023)
                    print("Sum of Current Liabilities 2023:", current_liabilities_sum_2023)
                    print("Sum of Non-Current Liabilities 2023:", non_current_liabilities_sum_2023)
                    print("Sum of Net Worth 2023:", net_worth_sum_2023)
                    '''

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

                    '''
                    print("Mismatch in Current Assets 2022:", Mismatch_CA_2022)
                    print("Mismatch in Current Assets 2023:", Mismatch_CA_2023)
                    print("Mismatch in Non-Current Assets 2022:", Mismatch_NCA_2022)
                    print("Mismatch in Non-Current Assets 2023:", Mismatch_NCA_2023)
                    print("Mismatch in Current Liabilities 2022:", Mismatch_CL_2022)
                    print("Mismatch in Current Liabilities 2023:", Mismatch_CL_2023)
                    print("Mismatch in Non-Current Liabilities 2022:", Mismatch_NCL_2022)
                    print("Mismatch in Non-Current Liabilities 2023:", Mismatch_NCL_2023)
                    print("Mismatch in Net Worth 2022:", Mismatch_NW_2022)
                    print("Mismatch in Net Worth 2023:", Mismatch_NW_2023)
                    '''


                    current_assets_2022['mismatch']={'value': str(Mismatch_CA_2022),'year':2022}
                    current_assets_2023['mismatch']={'value': str(Mismatch_CA_2023),'year':2023}
                    non_current_assets_2022['mismatch']={'value': str(Mismatch_NCA_2022),'year':2022}
                    non_current_assets_2023['mismatch']={'value': str(Mismatch_NCA_2023),'year':2023}
                    current_liabilities_2022['mismatch']={'value': str(Mismatch_CL_2022),'year':2022}
                    current_liabilities_2023['mismatch']={'value': str(Mismatch_CL_2023),'year':2023}
                    non_current_liabilities_2022['mismatch']={'value': str(Mismatch_NCL_2022),'year':2022}
                    non_current_liabilities_2023['mismatch']={'value': str(Mismatch_NCL_2023),'year':2023}
                    net_worth_2022['mismatch']={'value': str(Mismatch_NW_2022),'year':2022}
                    net_worth_2023['mismatch']={'value': str(Mismatch_NW_2023),'year':2023}


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

                    # Ensure to apply replace_fields to all datasets
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



                    '''

                    print("Current Assets 2022:", current_assets_2022)
                    print("Current Assets 2023:", current_assets_2023)
                    print("Non-Current Assets 2022:", non_current_assets_2022)
                    print("Non-Current Assets 2023:", non_current_assets_2023)
                    print("Current Liabilities 2022:", current_liabilities_2022)
                    print("Current Liabilities 2023:", current_liabilities_2023)
                    print("Non-Current Liabilities 2022:", non_current_liabilities_2022)
                    print("Non-Current Liabilities 2023:", non_current_liabilities_2023)
                    print("Net Worth 2022:", net_worth_2022)
                    print("Net Worth 2023:", net_worth_2023)
                    '''

                    combined_data = combined_data = {
    "CurrentAssets": [
        {
            "Cash": {
                "year": current_assets_2022.get('Cash', {}).get('year', '2022'),
                "value": current_assets_2022.get('Cash', {}).get('value', 0),
                "precision": current_assets_2022.get('Cash', {}).get('precision', 'N/A')
            }
        },
        {
            "TradeReceivables": {
                "year": current_assets_2022.get('TradeReceivables', {}).get('year', '2022'),
                "value": current_assets_2022.get('TradeReceivables', {}).get('value', 0),
                "precision": current_assets_2022.get('TradeReceivables', {}).get('precision', 'N/A')
            }
        },
        {
            "OtherNonTradeReceivables": {
                "year": current_assets_2022.get('OtherNonTradeReceivables', {}).get('year', '2022'),
                "value": current_assets_2022.get('OtherNonTradeReceivables', {}).get('value', 0),
                "precision": current_assets_2022.get('OtherNonTradeReceivables', {}).get('precision', 'N/A')
            }
        },
        {
            "FinishedGoods": {
                "year": current_assets_2022.get('FinishedGoods', {}).get('year', '2022'),
                "value": current_assets_2022.get('FinishedGoods', {}).get('value', 0),
                "precision": current_assets_2022.get('FinishedGoods', {}).get('precision', 'N/A')
            }
        },
        {
            "CurrentPortionOfPrepaidAndDeferredAssets": {
                "year": current_assets_2022.get('CurrentPortionOfPrepaidAndDeferredAssets', {}).get('year', '2022'),
                "value": current_assets_2022.get('CurrentPortionOfPrepaidAndDeferredAssets', {}).get('value', 0),
                "precision": current_assets_2022.get('CurrentPortionOfPrepaidAndDeferredAssets', {}).get('precision', 'N/A')
            }
        },
        {
            "TotalCurrentAssets": {
                "year": current_assets_2022.get('TotalCurrentAssets', {}).get('year', '2022'),
                "value": current_assets_2022.get('TotalCurrentAssets', {}).get('value', 0),
                "precision": current_assets_2022.get('TotalCurrentAssets', {}).get('precision', 'N/A')
            }
        },
        {
            "mismatch": {
                "value": current_assets_2022.get('mismatch', {}).get('value', 0),
                "year": current_assets_2022.get('mismatch', {}).get('year', '2022'),
                "precision": 'null'
            }
        },
        {
            "Cash": {
                "year": current_assets_2023.get('Cash', {}).get('year', 2023),
                "value": current_assets_2023.get('Cash', {}).get('value', 0),
                "precision": current_assets_2023.get('Cash', {}).get('precision', 'N/A')
            }
        },
        {
            "TradeReceivables": {
                "year": current_assets_2023.get('TradeReceivables', {}).get('year', 2023),
                "value": current_assets_2023.get('TradeReceivables', {}).get('value', 0),
                "precision": current_assets_2023.get('TradeReceivables', {}).get('precision', 'N/A')
            }
        },
        {
            "OtherNonTradeReceivables": {
                "year": current_assets_2023.get('OtherNonTradeReceivables', {}).get('year', 2023),
                "value": current_assets_2023.get('OtherNonTradeReceivables', {}).get('value', 0),
                "precision": current_assets_2023.get('OtherNonTradeReceivables', {}).get('precision', 'N/A')
            }
        },
        {
            "FinishedGoods": {
                "year": current_assets_2023.get('FinishedGoods', {}).get('year', 2023),
                "value": current_assets_2023.get('FinishedGoods', {}).get('value', 0),
                "precision": current_assets_2023.get('FinishedGoods', {}).get('precision', 'N/A')
            }
        },
        {
            "CurrentPortionOfPrepaidAndDeferredAssets": {
                "year": current_assets_2023.get('CurrentPortionOfPrepaidAndDeferredAssets', {}).get('year', 2023),
                "value": current_assets_2023.get('CurrentPortionOfPrepaidAndDeferredAssets', {}).get('value', 0),
                "precision": current_assets_2023.get('CurrentPortionOfPrepaidAndDeferredAssets', {}).get('precision', 'N/A')
            }
        },
        {
            "TotalCurrentAssets": {
                "year": current_assets_2023.get('TotalCurrentAssets', {}).get('year', 2023),
                "value": current_assets_2023.get('TotalCurrentAssets', {}).get('value', 0),
                "precision": current_assets_2023.get('TotalCurrentAssets', {}).get('precision', 'N/A')
            }
        },
        {
            "mismatch": {
                "value": current_assets_2023.get('mismatch', {}).get('value', 'N/A'),
                "year": current_assets_2023.get('mismatch', {}).get('year', 2023),
                "precision": 'null'
            }
        }
    ],
    "NonCurrentAssets": [
        {
            "ConstructionInProgress": {
                "year": non_current_assets_2022.get('ConstructionInProgress', {}).get('year', '2022'),
                "value": non_current_assets_2022.get('ConstructionInProgress', {}).get('value', 0),
                "precision": non_current_assets_2022.get('ConstructionInProgress', {}).get('precision', 'N/A')
            }
        },
        {
            "MachineryAndEquipment": {
                "year": non_current_assets_2022.get('MachineryAndEquipment', {}).get('year', '2022'),
                "value": non_current_assets_2022.get('MachineryAndEquipment', {}).get('value', 0),
                "precision": non_current_assets_2022.get('MachineryAndEquipment', {}).get('precision', 'N/A')
            }
        },
        {
            "OperatingLeases": {
                "year": non_current_assets_2022.get('OperatingLeases', {}).get('year', '2022'),
                "value": non_current_assets_2022.get('OperatingLeases', {}).get('value', 0),
                "precision": non_current_assets_2022.get('OperatingLeases', {}).get('precision', 'N/A')
            }
        },
        {
            "AccumulatedDepreciationAndImpairment": {
                "year": non_current_assets_2022.get('AccumulatedDepreciationAndImpairment', {}).get('year', '2022'),
                "value": non_current_assets_2022.get('AccumulatedDepreciationAndImpairment', {}).get('value', 0),
                "precision": non_current_assets_2022.get('AccumulatedDepreciationAndImpairment', {}).get('precision', 'N/A')
            }
        },
        {
            "LongTermPortionOfDerivativeAssets": {
                "year": non_current_assets_2022.get('LongTermPortionOfDerivativeAssets', {}).get('year', '2022'),
                "value": non_current_assets_2022.get('LongTermPortionOfDerivativeAssets', {}).get('value', 0),
                "precision": non_current_assets_2022.get('LongTermPortionOfDerivativeAssets', {}).get('precision', 'N/A')
            }
        },
        {
            "NonoperatingNoncurrentAssets": {
                "year": non_current_assets_2022.get('NonoperatingNoncurrentAssets', {}).get('year', '2022'),
                "value": non_current_assets_2022.get('NonoperatingNoncurrentAssets', {}).get('value', 0),
                "precision": non_current_assets_2022.get('NonoperatingNoncurrentAssets', {}).get('precision', 'N/A')
            }
        },
        {
            "IntangibleAssets": {
                "year": non_current_assets_2022.get('IntangibleAssets', {}).get('year', '2022'),
                "value": non_current_assets_2022.get('IntangibleAssets', {}).get('value', 0),
                "precision": non_current_assets_2022.get('IntangibleAssets', {}).get('precision', 'N/A')
            }
        },
        {
            "AccumulatedAmortizationAndImpairment": {
                "year": non_current_assets_2022.get('AccumulatedAmortizationAndImpairment', {}).get('year', '2022'),
                "value": non_current_assets_2022.get('AccumulatedAmortizationAndImpairment', {}).get('value', 0),
                "precision": non_current_assets_2022.get('AccumulatedAmortizationAndImpairment', {}).get('precision', 'N/A')
            }
        },
        {
            "TotalNonCurrentAssets": {
                "year": non_current_assets_2022.get('TotalNonCurrentAssets', {}).get('year', '2022'),
                "value": non_current_assets_2022.get('TotalNonCurrentAssets', {}).get('value', 0),
                "precision": non_current_assets_2022.get('TotalNonCurrentAssets', {}).get('precision', 'N/A')
            }
        },
        {
            "mismatch": {
                "year": non_current_assets_2022.get('mismatch', {}).get('year', '2022'),
                "value": non_current_assets_2022.get('mismatch', {}).get('value', 0),
                "precision": 'null'
            }
        },
        {
            "ConstructionInProgress": {
                "year": non_current_assets_2023.get('ConstructionInProgress', {}).get('year', 2023),
                "value": non_current_assets_2023.get('ConstructionInProgress', {}).get('value', 0),
                "precision": non_current_assets_2023.get('ConstructionInProgress', {}).get('precision', 'N/A')
            }
        },
        {
            "MachineryAndEquipment": {
                "year": non_current_assets_2023.get('MachineryAndEquipment', {}).get('year', 2023),
                "value": non_current_assets_2023.get('MachineryAndEquipment', {}).get('value', 0),
                "precision": non_current_assets_2023.get('MachineryAndEquipment', {}).get('precision', 'N/A')
            }
        },
        {
            "OperatingLeases": {
                "year": non_current_assets_2023.get('OperatingLeases', {}).get('year', 2023),
                "value": non_current_assets_2023.get('OperatingLeases', {}).get('value', 0),
                "precision": non_current_assets_2023.get('OperatingLeases', {}).get('precision', 'N/A')
            }
        },
        {
            "AccumulatedDepreciationAndImpairment": {
                "year": non_current_assets_2023.get('AccumulatedDepreciationAndImpairment', {}).get('year', 2023),
                "value": non_current_assets_2023.get('AccumulatedDepreciationAndImpairment', {}).get('value', 0),
                "precision": non_current_assets_2023.get('AccumulatedDepreciationAndImpairment', {}).get('precision', 'N/A')
            }
        },
        {
            "LongTermPortionOfDerivativeAssets": {
                "year": non_current_assets_2023.get('LongTermPortionOfDerivativeAssets', {}).get('year', 2023),
                "value": non_current_assets_2023.get('LongTermPortionOfDerivativeAssets', {}).get('value', 0),
                "precision": non_current_assets_2023.get('LongTermPortionOfDerivativeAssets', {}).get('precision', 'N/A')
            }
        },
        {
            "NonoperatingNoncurrentAssets": {
                "year": non_current_assets_2023.get('NonoperatingNoncurrentAssets', {}).get('year', 2023),
                "value": non_current_assets_2023.get('NonoperatingNoncurrentAssets', {}).get('value', 0),
                "precision": non_current_assets_2023.get('NonoperatingNoncurrentAssets', {}).get('precision', 'N/A')
            }
        },
        {
            "IntangibleAssets": {
                "year": non_current_assets_2023.get('IntangibleAssets', {}).get('year', 2023),
                "value": non_current_assets_2023.get('IntangibleAssets', {}).get('value', 0),
                "precision": non_current_assets_2023.get('IntangibleAssets', {}).get('precision', 'N/A')
            }
        },
        {
            "AccumulatedAmortizationAndImpairment": {
                "year": non_current_assets_2023.get('AccumulatedAmortizationAndImpairment', {}).get('year', 2023),
                "value": non_current_assets_2023.get('AccumulatedAmortizationAndImpairment', {}).get('value', 0),
                "precision": non_current_assets_2023.get('AccumulatedAmortizationAndImpairment', {}).get('precision', 'N/A')
            }
        },
        {
            "TotalNonCurrentAssets": {
                "year": non_current_assets_2023.get('TotalNonCurrentAssets', {}).get('year', 2023),
                "value": non_current_assets_2023.get('TotalNonCurrentAssets', {}).get('value', 0),
                "precision": non_current_assets_2023.get('TotalNonCurrentAssets', {}).get('precision', 'N/A')
            }
        },
        {
            "mismatch": {
                "year": non_current_assets_2023.get('mismatch', {}).get('year', 2023),
                "value": non_current_assets_2023.get('mismatch', {}).get('value', 0),
                "precision": 'null'
            }
        }
    ]
,
  "CurrentLiabilities": [
    {
      "ShorttermLoansPayable": {
        "year": current_liabilities_2022.get('ShorttermLoansPayable', {}).get('year', 2022),
        "value": current_liabilities_2022.get('ShorttermLoansPayable', {}).get('value', 0),
        "precision": current_liabilities_2022.get('ShorttermLoansPayable', {}).get('precision', 'null')
      }
    },
    {
      "CurrentPortionOfOperatingLeaseObligations": {
        "year": current_liabilities_2022.get('CurrentPortionOfOperatingLeaseObligations', {}).get('year', 2022),
        "value": current_liabilities_2022.get('CurrentPortionOfOperatingLeaseObligations', {}).get('value', 0),
        "precision": current_liabilities_2022.get('CurrentPortionOfOperatingLeaseObligations', {}).get('precision', 'null')
      }
    },
    {
      "TradeAccountsPayable": {
        "year": current_liabilities_2022.get('TradeAccountsPayable', {}).get('year', 2022),
        "value": current_liabilities_2022.get('TradeAccountsPayable', {}).get('value', 0),
        "precision": current_liabilities_2022.get('TradeAccountsPayable', {}).get('precision', 'null')
      }
    },
    {
      "OtherAccruals": {
        "year": current_liabilities_2022.get('OtherAccruals', {}).get('year', 2022),
        "value": current_liabilities_2022.get('OtherAccruals', {}).get('value', 0),
        "precision": current_liabilities_2022.get('OtherAccruals', {}).get('precision', 'null')
      }
    },
    {
      "OtherTaxesPayable": {
        "year": current_liabilities_2022.get('OtherTaxesPayable', {}).get('year', 2022),
        "value": current_liabilities_2022.get('OtherTaxesPayable', {}).get('value', 0),
        "precision": current_liabilities_2022.get('OtherTaxesPayable', {}).get('precision', 'null')
      }
    },
    {
      "IncomeTaxesPayable": {
        "year": current_liabilities_2022.get('IncomeTaxesPayable', {}).get('year', 2022),
        "value": current_liabilities_2022.get('IncomeTaxesPayable', {}).get('value', 0),
        "precision": current_liabilities_2022.get('IncomeTaxesPayable', {}).get('precision', 'null')
      }
    },
    {
      "CurrentPortionOfDerivativeLiabilities": {
        "year": current_liabilities_2022.get('CurrentPortionOfDerivativeLiabilities', {}).get('year', 2022),
        "value": current_liabilities_2022.get('CurrentPortionOfDerivativeLiabilities', {}).get('value', 0),
        "precision": current_liabilities_2022.get('CurrentPortionOfDerivativeLiabilities', {}).get('precision', 'null')
      }
    },
    {
      "TotalCurrentLiabilities": {
        "year": current_liabilities_2022.get('TotalCurrentLiabilities', {}).get('year', 2022),
        "value": current_liabilities_2022.get('TotalCurrentLiabilities', {}).get('value', 0),
        "precision": current_liabilities_2022.get('TotalCurrentLiabilities', {}).get('precision', 'null')
      }
    },
    {
      "mismatch": {
        "value": current_liabilities_2022.get('mismatch', {}).get('value', 0),
        "year": current_liabilities_2022.get('mismatch', {}).get('year', '2022'),
        "precision": 'null'
      }
    },
    {
      "ShorttermLoansPayable": {
        "year": current_liabilities_2023.get('ShorttermLoansPayable', {}).get('year', 0),
        "value": current_liabilities_2023.get('ShorttermLoansPayable', {}).get('value', 0),
        "precision": current_liabilities_2023.get('ShorttermLoansPayable', {}).get('precision', 'null')
      }
    },
    {
      "CurrentPortionOfOperatingLeaseObligations": {
        "year": current_liabilities_2023.get('CurrentPortionOfOperatingLeaseObligations', {}).get('year', 0),
        "value": current_liabilities_2023.get('CurrentPortionOfOperatingLeaseObligations', {}).get('value', 0),
        "precision": current_liabilities_2023.get('CurrentPortionOfOperatingLeaseObligations', {}).get('precision', 'null')
      }
    },
    {
      "TradeAccountsPayable": {
        "year": current_liabilities_2023.get('TradeAccountsPayable', {}).get('year', 0),
        "value": current_liabilities_2023.get('TradeAccountsPayable', {}).get('value', 0),
        "precision": current_liabilities_2023.get('TradeAccountsPayable', {}).get('precision', 'null')
      }
    },
    {
      "OtherAccruals": {
        "year": current_liabilities_2023.get('OtherAccruals', {}).get('year', 0),
        "value": current_liabilities_2023.get('OtherAccruals', {}).get('value', 0),
        "precision": current_liabilities_2023.get('OtherAccruals', {}).get('precision', 'null')
      }
    },
    {
      "OtherTaxesPayable": {
        "year": current_liabilities_2023.get('OtherTaxesPayable', {}).get('year', 0),
        "value": current_liabilities_2023.get('OtherTaxesPayable', {}).get('value', 0),
        "precision": current_liabilities_2023.get('OtherTaxesPayable', {}).get('precision', 'null')
      }
    },
    {
      "IncomeTaxesPayable": {
        "year": current_liabilities_2023.get('IncomeTaxesPayable', {}).get('year', 0),
        "value": current_liabilities_2023.get('IncomeTaxesPayable', {}).get('value', 0),
        "precision": current_liabilities_2023.get('IncomeTaxesPayable', {}).get('precision', 'null')
      }
    },
    {
      "CurrentPortionOfDerivativeLiabilities": {
        "year": current_liabilities_2023.get('CurrentPortionOfDerivativeLiabilities', {}).get('year', 0),
        "value": current_liabilities_2023.get('CurrentPortionOfDerivativeLiabilities', {}).get('value', 0),
        "precision": current_liabilities_2023.get('CurrentPortionOfDerivativeLiabilities', {}).get('precision', 'null')
      }
    },
    {
      "TotalCurrentLiabilities": {
        "year": current_liabilities_2023.get('TotalCurrentLiabilities', {}).get('year', 0),
        "value": current_liabilities_2023.get('TotalCurrentLiabilities', {}).get('value', 0),
        "precision": current_liabilities_2023.get('TotalCurrentLiabilities', {}).get('precision', 'null')
      }
    },
    {
      "mismatch": {
        "value": current_liabilities_2023.get('mismatch', {}).get('value', 0),
        "year": current_liabilities_2023.get('mismatch', {}).get('year', 2023),
        "precision": 'null'
      }
    }
  ]
,
   "NonCurrentLiabilities": [
    {
      "LongTermBankDebt": {
        "year": non_current_liabilities_2022.get("LongTermBankDebt", {}).get("year", 2022),
        "value": non_current_liabilities_2022.get("LongTermBankDebt", {}).get("value", 0),
        "precision": non_current_liabilities_2022.get("LongTermBankDebt", {}).get("precision", "null")
      }
    },
    {
      "LongTermPortionOfOperatingLeaseObligations": {
        "year": non_current_liabilities_2022.get("LongTermPortionOfOperatingLeaseObligations", {}).get("year", 2022),
        "value": non_current_liabilities_2022.get("LongTermPortionOfOperatingLeaseObligations", {}).get("value", 0),
        "precision": non_current_liabilities_2022.get("LongTermPortionOfOperatingLeaseObligations", {}).get("precision", "null")
      }
    },
    {
      "LongTermPortionOfDerivativeLiabilities": {
        "year": non_current_liabilities_2022.get("LongTermPortionOfDerivativeLiabilities", {}).get("year", 2022),
        "value": non_current_liabilities_2022.get("LongTermPortionOfDerivativeLiabilities", {}).get("value", 0),
        "precision": non_current_liabilities_2022.get("LongTermPortionOfDerivativeLiabilities", {}).get("precision", "null")
      }
    },
    {
      "NonOperatingNonCurrentLiabilities": {
        "year": non_current_liabilities_2022.get("NonOperatingNonCurrentLiabilities", {}).get("year", 2022),
        "value": non_current_liabilities_2022.get("NonOperatingNonCurrentLiabilities", {}).get("value", 0),
        "precision": non_current_liabilities_2022.get("NonOperatingNonCurrentLiabilities", {}).get("precision", "null")
      }
    },
    {
      "LongTermPortionOfLoansFromRelatedCompanies": {
        "year": non_current_liabilities_2022.get("LongTermPortionOfLoansFromRelatedCompanies", {}).get("year", 2022),
        "value": non_current_liabilities_2022.get("LongTermPortionOfLoansFromRelatedCompanies", {}).get("value", 0),
        "precision": non_current_liabilities_2022.get("LongTermPortionOfLoansFromRelatedCompanies", {}).get("precision", "null")
      }
    },
    {
      "LongTermPortionOfDeferredFederalIncomeTax": {
        "year": non_current_liabilities_2022.get("LongTermPortionOfDeferredFederalIncomeTax", {}).get("year", 2022),
        "value": non_current_liabilities_2022.get("LongTermPortionOfDeferredFederalIncomeTax", {}).get("value", 0),
        "precision": non_current_liabilities_2022.get("LongTermPortionOfDeferredFederalIncomeTax", {}).get("precision", "null")
      }
    },
    {
      "TotalNonCurrentLiabilities": {
        "year": non_current_liabilities_2022.get("TotalNonCurrentLiabilities", {}).get("year", 2022),
        "value": non_current_liabilities_2022.get("TotalNonCurrentLiabilities", {}).get("value", 0),
        "precision": non_current_liabilities_2022.get("TotalNonCurrentLiabilities", {}).get("precision", "null")
      }
    },
    {
      "mismatch": {
        "value": non_current_liabilities_2022.get("mismatch", {}).get("value", 0),
        "year": non_current_liabilities_2022.get("mismatch", {}).get("year", 2022),
        "precision": 'null'
      }
    },
    {
      "LongTermBankDebt": {
        "year": non_current_liabilities_2023.get("LongTermBankDebt", {}).get("year", 2023),
        "value": non_current_liabilities_2023.get("LongTermBankDebt", {}).get("value", 0),
        "precision": non_current_liabilities_2023.get("LongTermBankDebt", {}).get("precision", "null")
      }
    },
    {
      "LongTermPortionOfOperatingLeaseObligations": {
        "year": non_current_liabilities_2023.get("LongTermPortionOfOperatingLeaseObligations", {}).get("year", 2023),
        "value": non_current_liabilities_2023.get("LongTermPortionOfOperatingLeaseObligations", {}).get("value", 0),
        "precision": non_current_liabilities_2023.get("LongTermPortionOfOperatingLeaseObligations", {}).get("precision", "null")
      }
    },
    {
      "LongTermPortionOfDerivativeLiabilities": {
        "year": non_current_liabilities_2023.get("LongTermPortionOfDerivativeLiabilities", {}).get("year", 2023),
        "value": non_current_liabilities_2023.get("LongTermPortionOfDerivativeLiabilities", {}).get("value", 0),
        "precision": non_current_liabilities_2023.get("LongTermPortionOfDerivativeLiabilities", {}).get("precision", "null")
      }
    },
    {
      "NonOperatingNonCurrentLiabilities": {
        "year": non_current_liabilities_2023.get("NonOperatingNonCurrentLiabilities", {}).get("year", 2023),
        "value": non_current_liabilities_2023.get("NonOperatingNonCurrentLiabilities", {}).get("value", 0),
        "precision": non_current_liabilities_2023.get("NonOperatingNonCurrentLiabilities", {}).get("precision", "null")
      }
    },
    {
      "LongTermPortionOfLoansFromRelatedCompanies": {
        "year": non_current_liabilities_2023.get("LongTermPortionOfLoansFromRelatedCompanies", {}).get("year", 2023),
        "value": non_current_liabilities_2023.get("LongTermPortionOfLoansFromRelatedCompanies", {}).get("value", 0),
        "precision": non_current_liabilities_2023.get("LongTermPortionOfLoansFromRelatedCompanies", {}).get("precision", "null")
      }
    },
    {
      "LongTermPortionOfDeferredFederalIncomeTax": {
        "year": non_current_liabilities_2023.get("LongTermPortionOfDeferredFederalIncomeTax", {}).get("year", 2023),
        "value": non_current_liabilities_2023.get("LongTermPortionOfDeferredFederalIncomeTax", {}).get("value", 0),
        "precision": non_current_liabilities_2023.get("LongTermPortionOfDeferredFederalIncomeTax", {}).get("precision", "null")
      }
    },
    {
      "TotalNonCurrentLiabilities": {
        "year": non_current_liabilities_2023.get("TotalNonCurrentLiabilities", {}).get("year", 2023),
        "value": non_current_liabilities_2023.get("TotalNonCurrentLiabilities", {}).get("value", 0),
        "precision": non_current_liabilities_2023.get("TotalNonCurrentLiabilities", {}).get("precision", "null")
      }
    },
    {
      "mismatch": {
        "value": non_current_liabilities_2023.get("mismatch", {}).get("value", 0),
        "year": non_current_liabilities_2023.get("mismatch", {}).get("year", 2023),
        "precision": 'null'
      }
    }
  ],
  "NetWorth": [
    {
      "CommonStock": {
        "year": net_worth_2022.get("CommonStock", {}).get("year", 2022),
        "value": net_worth_2022.get("CommonStock", {}).get("value", 0),
        "precision": net_worth_2022.get("CommonStock", {}).get("precision", 'null')
      }
    },
    {
      "PaidInCapital": {
        "year": net_worth_2022.get("PaidInCapital", {}).get("year", 2022),
        "value": net_worth_2022.get("PaidInCapital", {}).get("value", 0),
        "precision": net_worth_2022.get("PaidInCapital", {}).get("precision", 'null')
      }
    },
    {
      "RetainedEarnings": {
        "year": net_worth_2022.get("RetainedEarnings", {}).get("year", 2022),
        "value": net_worth_2022.get("RetainedEarnings", {}).get("value", 0),
        "precision": net_worth_2022.get("RetainedEarnings", {}).get("precision", 'null')
      }
    },
    {
      "TotalNetWorth": {
        "year": net_worth_2022.get("TotalNetWorth", {}).get("year", 2022),
        "value": net_worth_2022.get("TotalNetWorth", {}).get("value", 0),
        "precision": net_worth_2022.get("TotalNetWorth", {}).get("precision", 'null')
      }
    },
    {
      "mismatch": {
        "value": net_worth_2022.get("mismatch", {}).get("value", 0),
        "year": net_worth_2022.get("mismatch", {}).get("year", 2022),
        "precision": 'null'
      }
    },
    {
      "CommonStock": {
        "year": net_worth_2023.get("CommonStock", {}).get("year", 2023),
        "value": net_worth_2023.get("CommonStock", {}).get("value", 0),
        "precision": net_worth_2023.get("CommonStock", {}).get("precision", 'null')
      }
    },
    {
      "PaidInCapital": {
        "year": net_worth_2023.get("PaidInCapital", {}).get("year", 2023),
        "value": net_worth_2023.get("PaidInCapital", {}).get("value", 0),
        "precision": net_worth_2023.get("PaidInCapital", {}).get("precision", 'null')
      }
    },
    {
      "RetainedEarnings": {
        "year": net_worth_2023.get("RetainedEarnings", {}).get("year", 2023),
        "value": net_worth_2023.get("RetainedEarnings", {}).get("value", 0),
        "precision": net_worth_2023.get("RetainedEarnings", {}).get("precision", 'null')
      }
    },
    {
      "TotalNetWorth": {
        "year": net_worth_2023.get("TotalNetWorth", {}).get("year", 2023),
        "value": net_worth_2023.get("TotalNetWorth", {}).get("value", 0),
        "precision": net_worth_2023.get("TotalNetWorth", {}).get("precision", 'null')
      }
    },
    {
      "mismatch": {
        "value": net_worth_2023.get("mismatch", {}).get("value", 0),
        "year": net_worth_2023.get("mismatch", {}).get("year", 2023),
        "precision": 'null'
      }
    }
  ]
}


                

                    return JsonResponse(combined_data, status=status.HTTP_200_OK,safe=False)

                    #return HttpResponse(combined_data, content_type='application/json')


                except Exception as e:
                    logging.error(f"Error during file processing: {str(e)}")

                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



