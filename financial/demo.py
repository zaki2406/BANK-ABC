import json

# Sample data for current assets in 2022 and 2023
all_data=[{'CurrentAssets': {'Cash': {'year': 2022, 'value': '21.2', 'TerminologyInterpretation': False, 'CalculationRequired': False}, 'TradeReceivables': {'year': 2022, 'value': '0.7', 'TerminologyInterpretation': True, 'CalculationRequired': False}, 'OtherNonTradeReceivables': {'year': 2022, 'value': '8.6', 'TerminologyInterpretation': True, 'CalculationRequired': False}, 'FinishedGoods': {'year': 2022, 'value': '0', 'TerminologyInterpretation': False, 'CalculationRequired': False}, 'CurrentPortionOfPrepaidAndDeferredAssets': {'year': 2022, 'value': '0', 'TerminologyInterpretation': False, 'CalculationRequired': False}, 'TotalCurrentAssets': {'year': 2022, 'value': '30.5', 'TerminologyInterpretation': False, 'CalculationRequired': False}}}, {'CurrentAssets': {'Cash': {'year': 2023, 'value': '194.2', 'TerminologyInterpretation': False, 'CalculationRequired': False}, 'TradeReceivables': {'year': 2023, 'value': '10.4', 'TerminologyInterpretation': False, 'CalculationRequired': False}, 'OtherNonTradeReceivables': {'year': 2023, 'value': '31.5', 'TerminologyInterpretation': False, 'CalculationRequired': False}, 'FinishedGoods': {'year': 2023, 'value': '33.5', 'TerminologyInterpretation': True, 'CalculationRequired': False}, 'CurrentPortionOfPrepaidAndDeferredAssets': {'year': 2023, 'value': '9.6', 'TerminologyInterpretation': True, 'CalculationRequired': False}, 'TotalCurrentAssets': {'year': 2023, 'value': '280.0', 'TerminologyInterpretation': False, 'CalculationRequired': False}}}, {'NonCurrentAssets': {'ConstructionInProgress': {'year': 2022, 'value': '308.5', 'TerminologyInterpretation': 'true', 'CalculationRequired': 'false'}, 'MachineryAndEquipment': {'year': 2022, 'value': '384.9', 'TerminologyInterpretation': 'true', 'CalculationRequired': 'false'}, 'OperatingLeases': {'year': 2022, 'value': '209.9', 'TerminologyInterpretation': 'true', 'CalculationRequired': 'false'}, 'AccumulatedDepreciationAndImpairment': {'year': 2022, 'value': '-151.9', 'TerminologyInterpretation': 'true', 'CalculationRequired': 'false'}, 'LongTermPortionOfDerivativeAssets': {'year': 2022, 'value': '9.2', 'TerminologyInterpretation': 'true', 'CalculationRequired': 'false'}, 'NonoperatingNoncurrentAssets': {'year': 2022, 'value': '0.6', 'TerminologyInterpretation': 'true', 'CalculationRequired': 'false'}, 'IntangibleAssets': {'year': 2022, 'value': '218.7', 'TerminologyInterpretation': 'true', 'CalculationRequired': 'false'}, 'AccumulatedAmortizationAndImpairment': {'year': 2022, 'value': '-6.2', 'TerminologyInterpretation': 'true', 'CalculationRequired': 'false'}, 'TotalNonCurrentAssets': {'year': 2022, 'value': '975.3', 'TerminologyInterpretation': 'true', 'CalculationRequired': 'false'}}}, {'NonCurrentAssets': {'ConstructionInProgress': {'year': 2023, 'value': '200.9', 'TerminologyInterpretation': 'true', 'CalculationRequired': 'false'}, 'MachineryAndEquipment': {'year': 2023, 'value': '849.9', 'TerminologyInterpretation': 'true', 'CalculationRequired': 'false'}, 'OperatingLeases': {'year': 2023, 'value': '108.9', 'TerminologyInterpretation': 'true', 'CalculationRequired': 'false'}, 'AccumulatedDepreciationAndImpairment': {'year': 2023, 'value': '-224.1', 'TerminologyInterpretation': 'true', 'CalculationRequired': 'false'}, 'LongTermPortionOfDerivativeAssets': {'year': 2023, 'value': '0.1', 'TerminologyInterpretation': 'true', 'CalculationRequired': 'false'}, 'NonoperatingNoncurrentAssets': {'year': 2023, 'value': '34.2', 'TerminologyInterpretation': 'true', 'CalculationRequired': 'false'}, 'IntangibleAssets': {'year': 2023, 'value': '255.3', 'TerminologyInterpretation': 'true', 'CalculationRequired': 'false'}, 'AccumulatedAmortizationAndImpairment': {'year': 2023, 'value': '-', 'TerminologyInterpretation': 'false', 'CalculationRequired': 'false'}, 'TotalNonCurrentAssets': {'year': 2023, 'value': '1,460.4', 'TerminologyInterpretation': 'true', 'CalculationRequired': 'false'}}}, {'CurrentLiabilities': {'ShorttermLoansPayable': {'year': 2022, 'value': '79.9', 'TerminologyInterpretation': 'true', 'CalculationRequired': 'false'}, 'CurrentPortionOfOperatingLeaseObligations': {'year': 2022, 'value': '68.8', 'TerminologyInterpretation': 'true', 'CalculationRequired': 'false'}, 'TradeAccountsPayable': {'year': 2022, 'value': '18.4', 'TerminologyInterpretation': 'true', 'CalculationRequired': 'false'}, 'OtherAccruals': {'year': 2022, 'value': '87.0', 'TerminologyInterpretation': 'true', 'CalculationRequired': 'false'}, 'OtherTaxesPayable': {'year': 2022, 'value': '0.9', 'TerminologyInterpretation': 'true', 'CalculationRequired': 'false'}, 'IncomeTaxesPayable': {'year': 2022, 'value': '0.9', 'TerminologyInterpretation': 'true', 'CalculationRequired': 'false'}, 'CurrentPortionOfDerivativeLiabilities': {'year': 2022, 'value': '4.2', 'TerminologyInterpretation': 'true', 'CalculationRequired': 'false'}, 'TotalCurrentLiabilities': {'year': 2022, 'value': '180.2', 'TerminologyInterpretation': 'true', 'CalculationRequired': 'false'}}}, {'CurrentLiabilities': {'ShorttermLoansPayable': {'year': 2023, 'value': '79.9', 'TerminologyInterpretation': 'false', 'CalculationRequired': 'false'}, 'CurrentPortionOfOperatingLeaseObligations': {'year': 2023, 'value': '37.9', 'TerminologyInterpretation': 'true', 'CalculationRequired': 'false'}, 'TradeAccountsPayable': {'year': 2023, 'value': '42.0', 'TerminologyInterpretation': 'true', 'CalculationRequired': 'false'}, 'OtherAccruals': {'year': 2023, 'value': '174.2', 'TerminologyInterpretation': 'true', 'CalculationRequired': 'false'}, 'OtherTaxesPayable': {'year': 2023, 'value': '3.5', 'TerminologyInterpretation': 'true', 'CalculationRequired': 'false'}, 'IncomeTaxesPayable': {'year': 2023, 'value': '0.6', 'TerminologyInterpretation': 'true', 'CalculationRequired': 'false'}, 'CurrentPortionOfDerivativeLiabilities': {'year': 2023, 'value': '0.0', 'TerminologyInterpretation': 'true', 'CalculationRequired': 'false'}, 'TotalCurrentLiabilities': {'year': 2023, 'value': '338.1', 'TerminologyInterpretation': 'false', 'CalculationRequired': 'false'}}}, {'NonCurrentLiabilities': {'LongTermBankDebt': {'year': 2022, 'value': 164.9, 'TerminologyInterpretation': True, 'CalculationRequired': False}, 'LongTermPortionOfOperatingLeaseObligations': {'year': 2022, 'value': 187.2, 'TerminologyInterpretation': True, 'CalculationRequired': False}, 'LongTermPortionOfDerivativeLiabilities': {'year': 2022, 'value': 1.4, 'TerminologyInterpretation': True, 'CalculationRequired': False}, 'NonOperatingNonCurrentLiabilities': {'year': 2022, 'value': 33.6, 'TerminologyInterpretation': True, 'CalculationRequired': False}, 'LongTermPortionOfLoansFromRelatedCompanies': {'year': 2022, 'value': 0, 'TerminologyInterpretation': False, 'CalculationRequired': False}, 'LongTermPortionOfDeferredFederalIncomeTax': {'year': 2022, 'value': 9.3, 'TerminologyInterpretation': True, 'CalculationRequired': False}, 'TotalNonCurrentLiabilities': {'year': 2022, 'value': 420.2, 'TerminologyInterpretation': True, 'CalculationRequired': False}}}, {'NonCurrentLiabilities': {'LongTermBankDebt': {'year': 2023, 'value': '292.6', 'TerminologyInterpretation': 'true', 'CalculationRequired': 'false'}, 'LongTermPortionOfOperatingLeaseObligations': {'year': 2023, 'value': '108.6', 'TerminologyInterpretation': 'true', 'CalculationRequired': 'false'}, 'LongTermPortionOfDerivativeLiabilities': {'year': 2023, 'value': '0.4', 'TerminologyInterpretation': 'true', 'CalculationRequired': 'false'}, 'NonOperatingNonCurrentLiabilities': {'year': 2023, 'value': '224.0', 'TerminologyInterpretation': 'true', 'CalculationRequired': 'false'}, 'LongTermPortionOfLoansFromRelatedCompanies': {'year': 2023, 'value': '67.4', 'TerminologyInterpretation': 'true', 'CalculationRequired': 'false'}, 'LongTermPortionOfDeferredFederalIncomeTax': {'year': 2023, 'value': '11.7', 'TerminologyInterpretation': 'true', 'CalculationRequired': 'false'}, 'TotalNonCurrentLiabilities': {'year': 2023, 'value': '704.7', 'TerminologyInterpretation': 'true', 'CalculationRequired': 'false'}}}, {'NetWorth': {'CommonStock': {'year': 2022, 'value': '2.6', 'TerminologyInterpretation': 'false', 'CalculationRequired': 'false'}, 'PaidInCapital': {'year': 2022, 'value': '550.1', 'TerminologyInterpretation': 'true', 'CalculationRequired': 'false'}, 'RetainedEarnings': {'year': 2022, 'value': '62.6', 'TerminologyInterpretation': 'false', 'CalculationRequired': 'false'}, 'TotalNetWorth': {'year': 2022, 'value': '615.3', 'TerminologyInterpretation': 'false', 'CalculationRequired': 'false'}}}, {'NetWorth': {'CommonStock': {'year': 2023, 'value': '2.6', 'TerminologyInterpretation': 'true', 'CalculationRequired': 'false'}, 'PaidInCapital': {'year': 2023, 'value': '550.1', 'TerminologyInterpretation': 'true', 'CalculationRequired': 'false'}, 'RetainedEarnings': {'year': 2023, 'value': '144.9', 'TerminologyInterpretation': 'true', 'CalculationRequired': 'false'}, 'TotalNetWorth': {'year': 2023, 'value': '697.6', 'TerminologyInterpretation': 'true', 'CalculationRequired': 'false'}}}]
#for b in all_data:
    #print(b)
 #   for c in b:
# Variables to store the values for 2022 and 2023
current_assets_2022, current_assets_2023 = {}, {}
non_current_assets_2022, non_current_assets_2023 = {}, {}
current_liabilities_2022, current_liabilities_2023 = {}, {}
non_current_liabilities_2022, non_current_liabilities_2023 = {}, {}
net_worth_2022, net_worth_2023 = {}, {}

for entry in all_data:
    # Check if the entry is for current assets
    if 'CurrentAssets' in entry:
        assets = entry['CurrentAssets']
        if assets['Cash']['year'] == 2022:
            current_assets_2022 = assets
        elif assets['Cash']['year'] == 2023:
            current_assets_2023 = assets
    
    # Check if the entry is for non-current assets
    elif 'NonCurrentAssets' in entry:
        assets = entry['NonCurrentAssets']
        if assets['ConstructionInProgress']['year'] == 2022:
            non_current_assets_2022 = assets
        elif assets['ConstructionInProgress']['year'] == 2023:
            non_current_assets_2023 = assets
    
    # Check if the entry is for current liabilities
    elif 'CurrentLiabilities' in entry:
        liabilities = entry['CurrentLiabilities']
        if liabilities['ShorttermLoansPayable']['year'] == 2022:
            current_liabilities_2022 = liabilities
        elif liabilities['ShorttermLoansPayable']['year'] == 2023:
            current_liabilities_2023 = liabilities
    
    # Check if the entry is for non-current liabilities
    elif 'NonCurrentLiabilities' in entry:
        liabilities = entry['NonCurrentLiabilities']
        if liabilities['LongTermBankDebt']['year'] == 2022:
            non_current_liabilities_2022 = liabilities
        elif liabilities['LongTermBankDebt']['year'] == 2023:
            non_current_liabilities_2023 = liabilities
    
    # Check if the entry is for net worth
    elif 'NetWorth' in entry:
        net_worth = entry['NetWorth']
        if net_worth['CommonStock']['year'] == 2022:
            net_worth_2022 = net_worth
        elif net_worth['CommonStock']['year'] == 2023:
            net_worth_2023 = net_worth

'''
# Combine the dictionaries
combined_ca = {'CurrentAssets': []}

# Add assets from 2022
for key, value in current_assets_2022.items():
    combined_ca['CurrentAssets'].append({key: value})

# Add assets from 2023
for key, value in current_assets_2023.items():
    combined_ca['CurrentAssets'].append({key: value})

print(combined_ca)
# Convert to JSON
json_output = json.dumps(combined_ca, indent=2)

# Print the JSON
print(json_output)
'''


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



