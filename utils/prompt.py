import json

balance_sheet_response_format = {
    "is_balance_sheet_present": "Yes/No",
    "balance_sheet": {
        "assets": {
            "cash": [
                ["field_label", "field_value", "pdf_document_page_number"]
            ],
            "tenant_accounts_receivable": [["field_label", "field_value", "pdf_document_page_number"],["field_label", "field_value", "pdf_document_page_number"],],
            "accounts_receivable_other": [["field_label", "field_value", "pdf_document_page_number"],],
            "tenant_security_deposits": [["field_label", "field_value", "pdf_document_page_number"],],
            "prepaid_property_insurances": [["field_label", "field_value", "pdf_document_page_number"],],
            "other_prepaid_expenses": [["field_label", "field_value", "pdf_document_page_number"],],
            "miscellaneous_current_assets": [["field_label", "field_value", "pdf_document_page_number"],],
            "total_current_assets": "0",
            "real_estate_taxes_and_insurance_escrow": [["field_label", "field_value", "pdf_document_page_number"],],
            "reserve_for_replacement": [["field_label", "field_value", "pdf_document_page_number"],],
            "operating_deficit_reserve": [["field_label", "field_value", "pdf_document_page_number"],],
            "bond_escrow": [["field_label", "field_value", "pdf_document_page_number"],],
            "construction_escrow": [["field_label", "field_value", "pdf_document_page_number"],],
            "miscellaneous_escrows": [["field_label", "field_value", "pdf_document_page_number"],],
            "total_reserves_and_deposits": "0",
            "land": [["field_label", "field_value", "pdf_document_page_number"],],
            "fixed_assets": [["field_label", "field_value", "pdf_document_page_number"],],
            "accumulated_depreciation": [["field_label", "field_value", "pdf_document_page_number"],],
            "total_fixed_assets": "0",
            "other_assets": [["field_label", "field_value", "pdf_document_page_number"],],
            "total_other_assets": "0",
            "total_assets": "0"
        },
        "liabilities": {
            "accounts_payable": [["field_label", "field_value", "pdf_document_page_number"],],
            "accrued_property_taxes": [["field_label", "field_value", "pdf_document_page_number"],],
            "other_accrued_expenses": [["field_label", "field_value", "pdf_document_page_number"],],
            "tenant_security_deposits": [["field_label", "field_value", "pdf_document_page_number"],],
            "accrued_management_fees": [["field_label", "field_value", "pdf_document_page_number"],],
            "prepaid_rent": [["field_label", "field_value", "pdf_document_page_number"],],
            "accrued_interest_payable": [["field_label", "field_value", "pdf_document_page_number"],],
            "mortgage_notes_payable_current_portion": [["field_label", "field_value", "pdf_document_page_number"],],
            "construction_payable": [["field_label", "field_value", "pdf_document_page_number"],],
            "miscellaneous_current_liabilities": [["field_label", "field_value", "pdf_document_page_number"],],
            "total_current_liabilities": "0",
            "mortgage_notes_payable_long_term": [["field_label", "field_value", "pdf_document_page_number"],],
            "loan_issuance_costs_net_of_accum_amort": [["field_label", "field_value", "pdf_document_page_number"],],
            "construction_loan": [["field_label", "field_value", "pdf_document_page_number"],],
            "developer_fee_payable": [["field_label", "field_value", "pdf_document_page_number"],],
            "development_advances": [["field_label", "field_value", "pdf_document_page_number"],],
            "project_expense_loans": [["field_label", "field_value", "pdf_document_page_number"],],
            "working_capital_loans": [["field_label", "field_value", "pdf_document_page_number"],],
            "accrued_distributions_fees_to_ilpi": [["field_label", "field_value", "pdf_document_page_number"],],
            "soft_debt_payable": [["field_label", "field_value", "pdf_document_page_number"],],
            "accrued_soft_debt_interest": [["field_label", "field_value", "pdf_document_page_number"],],
            "ilp_loans": [["field_label", "field_value", "pdf_document_page_number"],],
            "other_long_term_liabilities": [["field_label", "field_value", "pdf_document_page_number"],],
            "total_long_term_liabilities": "0",
            "limited_partners_equity_deficiency": [["field_label", "field_value", "pdf_document_page_number"],],
            "other_partners_equity_deficiency": [["field_label", "field_value", "pdf_document_page_number"],],
            "miscellaneous_equity_deficiency": [["field_label", "field_value", "pdf_document_page_number"],],
            "total_owners_equity": "0",
            "total_liabilities_and_equity": "0",
        }
    }

}

income_statement_response_format = {
    "is_income_statement_present": "Yes/No",
    "income_statement": {
        "revenue_income": {
            'apartment_revenue': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'gain_loss_to_lease': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'commercial_revenue': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'gross_potential_rent': "0",
            'vacancy_apartments': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'vacancy_commercial': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'total_vacancy': "0",
            'bad_debt': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'concessions': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'net_rental_revenue': "0",
            'laundry': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'parking': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'interest_income': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'miscellaneous_revenue': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'total_other_revenue': "0",
            'net_revenue': "0",
        },
        "expenses": {
            'administrative_payroll': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'management_fee': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'administrative_expenses': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'total_administrative_expenses': "0",
            'water_sewer': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'other_utilities_expense': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'total_utilities_expense': "0",
            'maintenance_payroll': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'trash_removal': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'maintenance_expenses': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'total_maintenance_expenses': "0",
            'real_estate_taxes': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'property_liability_insurance': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'total_taxes_and_insurance': "0",
            'total_operating_expenses': "0",
            'net_operating_income': "0",
            'interest_expense_hard_debt': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'interest_expense_construction': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'interest_expense_soft_debt': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'interest_on_notes': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'amortization_of_loan_issuance_costs': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'total_interest_on_mortgage_notes': "0",
            'loan_fees': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'mortgage_insurance_premium': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'miscellaneous_financial_expenses': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'total_financial_expenses': "0",
            'other_non_cash_expenses_income': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'depreciation_other_amortization': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'partnership_fees': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'non_recurring_non_cash_expense': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'non_recurring_non_cash_income': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'capital_repairs_not_capitalized': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'non_recurring_cash_expense': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'non_recurring_cash_income': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'impairment': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'net_profit_loss': "0",
            'principal_payments_hard_debt': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'principal_payments_soft_debt': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'total_mortgage_principal_payments': "0",
            'depreciation_amort_other_non_cash': "0",
            'actual_replacement_reserve_deposits': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'replacement_reserve_withdrawals': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'interest_expense_soft_debt_accrued': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'accrued_partnership_fees': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'capital_improvements_not_expensed': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'preferred_equity_distribution': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'other_adjustments': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'total_operating_cash_flow': "0",
            'capital_contributions': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'deficit_funding': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'ilp_fund_advances': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'other_cash_flow_adjustments': [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category"],],
            'total_net_cash_flow': "0"
        },
        "unmapped_fields": [["field_label", "field_value", "pdf_document_page_number", "pdf_subheader_category", "reason_for_not_being_mapped"],]
    }

}



def get_balance_sheet_user_prompt(extracted_text):
   balance_sheet_user_prompt = f'''
            Please process the extracted text for "Balance Sheet" for a property provided between triple backticks, ensuring below guidelines are followed strictly:
               - ** Please Extract field values for Chart of Accounts (CoA) as per the guidelines mentioned for Balance Sheet.
               - ** Your task is to map all fields from extracted text to any Chart of Accounts that is most similar or most related match
                    - If you are unable to map any field to a CoA then search for CoA with most similar or most related match, All fields should be mapped
               - ** Each CoA can have multiple fields mapped to it
               - ** Output for each CoA is a list of fields in format ["field_label", "field_value", "pdf_document_page_number"]
                    - "field_label" is the label of the field
                    - "field_value" is the value of the field which is a decimal value without any comma
                        - remove comma ',' from "field_value" if present
                            - E.g. 72,598.08 will be 72598.08
                            - E.g. -15,786.78 will be -15786.78
                    - "pdf_document_page_number" is an integer value
                    - If any field is not mapped to any COA then output is an empty array
               - ** pdf_document_page_number is a number present in the format "<!-- PdfDocumentPageNumber 7 -->" at the begining of each page
               - ** If a value is surrounded by round paranthesis, then the value will be negative
                    - E.g. (14,876) will be -14,876
               - ** Balance Sheet: 
                    - Document title for Balance Sheet is labelled as Balance Sheet
                    - Balance Sheet contains Assets and Liabilities
                    - Classify the fields under Assets and liabilities as per the CoA mentioned for Balance Sheet
                    - Any value from extracted text should be mapped to the field that matches the CoA
                    - the output value for each CoA would be a list of values as per the JSON format
               - ** If Balance Sheet is not present in the extracted text then balance_sheet key value will be 'null'


         ## Balance Sheet Document guidelines:

            - ## Assets Chart of Accounts (CoA)      
                - Cash
                    - Any Escrow values will not come under Cash
                    - Only below categories is considered as Cash
                        - Cash In Bank
                        - CD's
                        - Checking Account	
                        - Investment Cash	
                        - Investment Fund	
                        - Money Market - Cash	
                        - Month End Arrears	
                        - Operating Account/Cash	
                        - Partnership Checking - Owner Held	
                        - Petty Cash
                        - Rental Depository Account	
                        - U.S. Bank Funds	
                - Tenant Accounts Receivable
                    - A/R - Local Housing Authority
                    - A/R - PHA
                    - A/R- Residents
                    - Allowance for Doubtful Accounts
                        - This should be (-) and reduce Tenant Accounts Receivable
                    - Bad Debt Allowance
                        - This should be (-) and reduce Tenant Accounts Receivable
                    - HAP Receivable
                    - HUD Receivable
                    - Rent Receivable 
                    - Section 8 A/R
                    - Subsidies Receivable
                    - Subsidized Rent
                    - Tenant Accounts Receivable
                    - Uncollected Rent
                - Accounts Receivable Other
                    - A/R - Due from Affiliate
                    - Accounts Receivable Other
                    - Clearing Account
                    - Due from Other Company
                    - Intercompany Receivable
                    - Owner Receivables
                    - Partnership Contribution Receivables
                    - Repayment Agreement
                    - TIF Receivable
                - Tenant Security Deposits
                    - Cash - Security
                    - Interest on Security deposit
                    - Key Deposit
                    - Other Tenant Deposits
                    - Pet Security Deposits
                    - Tenant Security Deposits
                - Prepaid Property Insurances
                    - Prepaid Insurance
                    - Prepaid Insurance - Earthquake
                    - Prepaid Property Insurance
                - Other Prepaid Expenses
                    - Prepaid Expenses Other
                    - Prepaid Insurance Other
                    - Prepaid Mortgage Insurance
                    - Prepaid Real Estate Taxes
                    - Prepaid Rent
                - Miscellaneous Current Assets
                    - Account Revenue Other Than Rent
                    - Insurance Claims
                    - Investment Short Term
                    - Misc Current Assets
                    - Notes Receivable
                    - Payroll Deposits
                    - Short Term Borrowing
                    - Utility Deposit 
            
                - Real Estate Taxes and Insurance Escrow
                    - Impounds
                    - Insurance Escrow
                    - MIP Escrow
                    - Mortgage Reserve
                    - Mortgagee Escrow Deposits
                    - Reserve for Insurance
                    - Reserve Hazard Insurance
                    - RTO Escrow
                    - Tax Rscrow
                    - Trustee - Mortgage
                    - Trustee - Tax & Insurance
                - Reserve for Replacement
                    - EUR Reserves
                    - Painting Reserve
                    - Repair and Improvement Escrow
                    - Reserve CD
                    - Reserve Deposits
                    - Reserve For Replacements
                    - Tenant Improvement escrows
                    - Trustee - Replacement                
                - Operating Deficit Reserve
                    - Operating Reserve                
                    - Operating Deficit Reserve
                - Bond Escrow
                    - Bond Escrows
                    - Debt Service Reserve
                    - Principal Reserve
                    - Revenue Fund
                    - Interest Fund
                    - Sinking Fund
                    - Trust - Bond Fund
                    - Trust - Interest/Admin Expense
                    - Trust - Principal
                    - Trustee Escrow                
                - Construction Escrow
                    - Development Escrow
                    - Construction Escrow                
                - Miscellaneous Escrows
                    - Audit Expense Escrow
                    - Capital Contribution Escrows
                    - Main Fund 
                    - Miscellaneous Escrows
                    - MMA Special Reserve
                    - Other Escrows
                    - Partnership Escrow
                    - Performance Deposits
                    - Project Buyout Reserves
                    - Rent Subsidy Reserves
                    - Resident Service Reserve
                    - Residual Receipts reserve
                    - Social Service Reserve
                    - Special Escrow
                    - Transition Reserve                
            
                - Land
                - Fixed Assets
                    - Building
                    - Building Improvements
                    - Building Equipment
                    - Capital Expenditures
                    - Capital Improvements
                    - Computer Equipment/Software
                    - Construction in Progress/Work in Progress
                    - Furniture
                    - Land Improvements
                    - Maintenance Equipment
                    - Motor Vehicles
                    - Other Fixed Assets
                    - Personal Property
                    - Rehab Cost                
                - Accumulated Depreciation
            
                - Other Assets
                    - Accumulated Amortization
                    - Capital Subscriptions
                    - Compliance Monitoring Fees
                    - Deferred Charges
                    - Deferred Financing Costs, Net
                    - Deferred Organization Costs, Net
                    - Deposits Receivable
                    - Exchange
                    - Intangible Assets
                    - Loan Costs
                    - Miscellaneous Other Assets
                    - Net Program Cost Congregate
                    - Other Assets
                    - Prepaid Loan Fees
                    - Prepaid Land/Ground Lease
                    - Refundable Deposits
                    - Syndication Fee
                    - Tax Credit Monitoring Fees
                    - Title and Record Fee                            
            
            - ## Liabilities  Chart of Accounts (CoA)
                - Accounts Payable
                    - Accounts Payable / AP-Trade
                    - AP - Other Projects
                    - HAP - Payable 
                    - Intercompany Payable
                        - If Payable or due to any company
                            - E.g. DuetoRichSmithManagement                
                - Accrued Property Taxes
                    - Accrued Pilot
                    - Accrued property taxes
                    - Accrued Real Estate Taxes                
                - Other Accrued Expenses
                    - Account Payable - HUD
                    - Accrued Operating Expenses
                    - Accrued Payroll and Wages
                    - Accrued Wage and Payroll Tax
                    - Other Accrued Liabilities
                    - Project Control
                    - State Franchise Tax Payable                
                - Tenant Security Deposits
                    - Interest on Security deposit
                    - Other Tenant Deposits
                    - Pet Security Deposits
                    - Tenant Security deposits                
                - Accrued Management Fees
                    - Accrued Property Management Fees                
                - Prepaid Rent
                    - Deferred Rent / Deferred Revenue
                    - Prepaid Rent
                    - Unearned Revenue                
                - Accrued Interest Payable
                    - 1st Mortgage Accrued Interest Payable
                    - 2nd Mortgage Accrued Interest Payable
                    - 3rd Mortgage Accrued Interest Payable
                    - 4th Mortgage Accrued Interest Payable
                    - 5th  Mortgage Accrued Interest Payable                
                - Mortgage Notes Payable - Current Portion
                    - 1st Mortgage Note Payable Current Portion
                    - 2nd Mortgage Note Payable Current Portion
                    - 3rd Mortgage Note Payable Current Portion
                    - 4th Mortgage Note Payable Current Portion
                    - 5th Mortgage Note Payable Current Portion
                    - Converted Permanent Debt (former construction loan)                
                - Construction Payable
                    - Construction Cost Payable
                - Miscellaneous Current Liabilities
                    - Adjustments
                    - Escheatment Liabilities
                    - Insurance Payable
                    - Miscellaneous Current Liabilities
                    - Unclaimed Property                
                
                - Mortgage Notes Payable - Long Term
                    - 1st Mortgage Note Payable
                    - 2nd Mortgage Note Payable
                    - 3rd Mortgage Note Payable
                    - 4th Mortgage Note Payable
                    - 5th Mortgage Note Payable
                    - Bond Payable
                    - Loans Payable MCTC
                    - Permanent Loan                
                - Loan Issuance Costs (Net of Accum. Amort.)
                    - Debt Issuance Costs
                - Construction Loan
                    - Construction Loan Payable
                - Developer Fee Payable
                    - Accrued Contractor Fee/Overhead
                    - Accrued Interest on Developer Fee
                    - Developer Fee Payable                
                - Development Advances
                - Project Expense Loans
                    - Project Expense Loans
                    - Advance from GP
                    - Due to GP / Affiliate GP only                
                - Working Capital Loans
                    - Working Capital Loans
                    - Due to GP / Affiliate GP only              
                - Accrued Distributions Fees to ILPI
                    - Accrued Asset Management Fee LP
                    - Lend Lease Payments
                    - Priority Distribution Payable
                    - Due to Limited Partner                
                - Soft Debt Payable
                    - Notes Payable (Long-Term)
                    - Converted Permanent Debt (former Construction Loan)                
                - Accrued Soft Debt Interest
                - ILP Loans
                    - Interest Bearing - Secured Notes Payable to LP
                    - LP Deficit Funding - Non Interest Bearing - Unsecured
                    - Accured Interest on Notes Payable to LP                
                - Other Long Term Liabilities
                    - Accrued Monitoring fees
                    - Accrued Partnership Fees General Partner
                    - Asset Management Fee Payable
                    - Contingent management fees
                    - Deferred Management fees
                    - Ground Lease
                    - Incentive Management Fee
                    - Interest Rate Swap Agreement
                    - Investor Servicing Fee
                    - Other Partnership Fees 
                    - Partnership Management Fee
                    - Subordinate Management Fees
                    - Supervisory Management Fees 
                    - Supplemental Management Fees                                
                    - Other Long Term Liabilities
                        - Liabilities that could not be mapped to other CoA
                
                - Limited Partners' Equity/(Deficiency)
                - Other Partners' Equity/(Deficiency)
                    - General Partner's Equity
                    - Other Partners' Equity / Deficiency
                    - Special Limited Partner Equity                
                - Miscellaneous Equity/(Deficiency)
                    - Current Year Earnings (Retained Earnings)
                    - Miscellaneous Equity / Deficiency                
            

         ## extracted Balance Sheet Text: 
            ```{extracted_text}```   

         
         ## Respond in the JSON format as described below for the given extracted document text, do not remove any json fields, even if the field is not present or does not have any value:
               {json.dumps(balance_sheet_response_format, indent=2)}

            '''
   return balance_sheet_user_prompt

def get_income_statement_user_prompt(extracted_text):
   income_statement_user_prompt = f'''
            Please process the extracted text for Income Statement" for a property provided between triple backticks, ensuring below guidelines are followed strictly:
               - ** Please Extract field values for Chart of Accounts (CoA) as per the guidelines mentioned for Income Statement.
               - ** Your task is to map all fields from extracted text to any Chart of Accounts that is most similar or most related match
                    - If you are unable to map any field to a CoA then search for CoA with most similar or most related match, All fields should be mapped
               - ** Each CoA can have multiple unique fields mapped to it
               - ** Output for each CoA is a list of fields in format ["field_label", "field_value", "pdf_document_page_number"]
                    - "field_label" is the label of the field
                    - "field_value" is the value of the extracted field which is a decimal value
                    - "pdf_document_page_number" is an integer value
               - ** pdf_document_page_number is a number present in the format "<!-- PdfDocumentPageNumber 7 -->" at the begining of each page
               - ** If a value is surrounded by round paranthesis, then the value will be negative
                    - E.g. (14,876) will be -14,876
               - ** Income Statement: 
                    - Document title for Income Statement could be labelled as Income Statement, Profit & Loss
                    - Income Statement contains Income / Revenue and Expenses
                    - Classify the fields under Assets and liabilities as per the CoA mentioned for Income Statement
                    - Any value from extracted text should be mapped to the field that matches the CoA
                    - Income Statement values should be extracted from Year to Date column
                    - All Actual Year to Date values should be extracted and no values should be skipped
                    - "Net Income" field denotes the end of Income Statement
                    - If you were unable to extract any value for either of the following fields from Income Statement, then extract the value from Property Status Update Form, the value extracted from income statement takes precedence if it's not empty
                        - Total YTD Hard Debt INTEREST Expense
                        - Total YTD Hard Debt PRINCIPAL Payments
                        - Total YTD Required Replacement Reserve Deposits (excluding interest)
                        - Total YTD Replacement Reserve Withdrawals
               - ** If Income Statement is not present in the extracted text then income_statement key will be 'null'
               - ** "pdf_subheader_category" is the subheader under which the field is present in the extracted text table
                        - subheader can be identified as cells that do not have any value against them
                        - "pdf_subheader_category" can only be either "income" or "expenses"
                        - any cells with value against them must be mapped to a CoA as per the income statement guidelines and it's not dependent on "pdf_subheader_category"
               - ** Any field must only be mapped once to a CoA


         ## Income Statement guidelines:
            - ## Income / Revenue Chart of Accounts (CoA)
                - Apartment Revenue
                    - Apartment Revenue
                    - Deferred Income
                    - HAP or HUD Subsidy
                    - Lease Differential
                    - Net Change A/R
                    - Prepaid Rent
                    - Prior Month Adjustment
                    - Prorated Rent from Previous Month
                    - Rent Abatement 
                    - Rent Refund
                    - Rental Assistance
                    - Rental Income
                    - Section 8 Income
                    - Subsidy Income
                    - Tenant Assistance Payments
                    - Tenant Subsidy
                    - Tenant Utility Payment
                    - Utility Allowance                
                - Gain/Loss to Lease
                - Commercial Revenue
                    - Commercial Revenue
                    - Salon Revenue
                    - Store Revenue                

                - Vacancy - Apartments
                    - Prior Month Vacancy
                    - Vacancy- Apartments                
                - Vacancy - Commercial
                    - Vacancy - Garage and Parking
                    - Vacancy - Miscellaneous
                    - Vacancy - Stores and Commercial                

                - Bad Debt
                    - Allowance for Bad Debt
                    - Bad Debt
                    - Collections Loss
                    - Collections or Reimbursements against Bad Debt
                        - E.g. Bad Debt Collections
                    - Delinquent Rent
                    - Recovery of Bad Debt
                    - Rental Write Offs
                    - Tenant Uncollectibles
                    - Uncollected Rent
                    - Write Off Other Income                
                - Concessions
                    - Concessions
                    - Free Rent
                    - Renewal incentives
                    - Rent Credits - Tenants
                    - Rental Allowance
                    - Rental discounts                

                - Laundry
                    - Coin Operations
                    - Dryer Income
                    - Laundry Income
                    - Vending Income
                    - Washer/Dryer Rentals                
                - Parking
                    - Carport Rental
                    - Garage Income
                    - Parking Spaces                
                - Interest Income
                    - Dividend Income
                    - Financial Revenue
                    - Interest Income - Miscellaneous
                    - Interest Income - Operations
                    - Interest Income - Replacement Reserves
                    - Interest Income - Residual Receipts
                    - Interest Income - Security Deposit
                    - Revenue from Investments                
                - Miscellaneous Revenue
                    - Application Fees
                    - Credit Loss
                    - Credit Report Income
                    - Damages and Cleaning Fees
                    - Day Care Income/Revenue
                    - Forfeited Tenant Security Deposit
                    - Grant Revenue
                    - Keys
                    - Late Charges
                    - Non-Revenue Units
                    - NSF and Late Charges
                    - Other Revenue
                    - Pet Income 
                    - Relocation Income
                    - Resident Referral
                    - Security Forfeitures
                    - Storage Income
                    - Tenant Charges
                    - Tenant Legal Charges
                    - Tenant Service income
                    - Utility Reimbursement/Utility Income
                    - Cable Fees, Break Lease Fees, Cancellation Fees (OTHER FEES)                

            - ## Expenses  Chart of Accounts (CoA)
                - Administrative Payroll
                    - 401K 
                    - Bonuses
                        - Employee Bonuses
                    - Casual Laboar
                    - Commissions
                    - Employe Rent Concessions
                    - Employee Housing
                    - Employee Incentives
                        - Bonuses
                        - Incentives
                        - Benefits
                        - Relations
                        - Reimbursements
                    - Employee Units/ Employee rental discounts
                    - Employee Discounts
                    - Health Insurance and Other Benefits
                    - Leasing Salary
                    - Manager Salary
                    - Manager Utilities
                    - Manager's or Security Rent Free Unit
                    - Office Salaries
                    - Payroll Burden
                    - Payroll Reserve
                    - Payroll Taxes (FICA)
                        - Payroll Taxes
                    - Social Security Taxes
                    - Supportive Services Payroll
                    - Temp Labor
                    - Contract Labor
                    - Unemployment Insurance
                    - Workmen's Compensation
                        - Workmans Comp Insurance                
                - Management Fee
                    - Property Management fee
                    - Management Services                
                - Administrative Expenses
                    - Admin Rent Free Unit
                    - Administrative unit
                    - Advertising
                    - Association Fees
                    - Auditing Expenses (Project/HUD)
                    - Auto/Travel/Lodge
                    - Bank charges
                        - Bank Service Charges
                        - Finance Charges / Late Fees
                    - Bookkeeping Fees/Accounting Services
                    - CA Taxes
                    - Cable expense
                        - Cable
                        - TV
                    - Collection Costs - Legal
                    - Collection Fees
                    - Compliance fees
                    - Computer expenses
                    - Consultant Insurance
                    - Consulting fees
                    - Dues and Subscriptions
                    - Entity Expense 
                    - Employee training
                    - Employee Uniforms
                        - All Uniforms are Admin Expenses (including Maintenance Uniforms)
                    - Fidelity Bond Insurance
                    - Fidelity Crime Insurance
                    - Franchise Tax
                    - Home Owner Association (HOA) Dues
                    - Insurance Repairs
                    - Interest on Security deposits
                    - Internet fees
                    - Lease up Fee
                    - Leasing Agents
                    - Legal expenses (Project)
                    - Marketing fees
                    - Miscellaneous Administrative Expenses
                        - Marketing Materials
                    - Miscellaneous Expenses
                    - Miscellaneous Taxes, Licenses, and Permits
                    - Model Unit
                    - Models, Quarters
                    - Monitoring Fee(Tax Credits, Compliance)
                    - Non-Profit Center Operations & Rent
                    - Office Rent
                    - Office Supplies
                    - Other insurance expenses
                    - Other taxes 
                    - Oversight fee
                    - Partnership expenses 
                    - Partnership legal fees
                    - Pass through entity tax
                    - Payroll Fees
                    - Payroll processing fee
                    - personal property tax
                    - Postage
                    - Pre-employment
                        - Credit and Background Checks
                    - Printing/Copier/Mailing fees
                    - Professional Fees
                    - Promotions
                    - Referrals (tenant and non-tenant referrals) 
                    - Renting Expense
                    - Residential service expense
                    - Signage / Sign placements
                    - Social Activities
                    - Social service
                    - Staff costs/Meals & Entertainment
                    - Tax Compliance Fees
                    - Telephone and Answering Service
                    - Tenant Discrimination Insurance
                    - Training Expense                

                - Water & Sewer
                    - Irrigation / Drainage
                    - Sewage
                    - Sewer
                    - Water                 
                - Other Utilities Expense
                    - Electricity
                    - Fuel Oil/Coal
                    - Gas
                    - Lightsource
                    - Miscellaneous utilities
                    - Utilities for vacant/occupied unites                

                - Maintenance Payroll
                    - Any insurance or other benefits specifically for Maintenance
                    - Caretaker Salary
                    - Courtesy Officer Payroll
                    - Decorating Payroll
                    - Engineer Salary
                    - Floater Salary
                    - Grounds Payroll
                    - Janitor and Cleaning Payroll
                    - Maid Salary
                    - Maintenance Supervisor
                    - Night Monitor
                    - Porter Payroll
                    - Repairs Payroll
                    - Superintendent Salary
                    - Tempory Help - Maintenance
                    - Union Benefits                
                - Trash Removal
                    - Garbage Removal 
                    - Trash Removal 
                    - Rubbish Removal, 
                    - Recycling
                    - Refuse Service
                    - Solid/Waste Management                
                - Maintenance Expenses
                    - Alarm Service
                    - Appliances
                    - Caretaker/Maid
                    - Courtesy Officer Expense
                    - Decorating Payroll/Contract
                    - Decorating Supplies
                        - Decor Supplies
                    - Elevator maintenance/contract
                    - Exterminating Payroll/Contract
                    - Exterminating Supplies
                    - Fire Protection Fee
                    - Furniture Repair
                    - Grounds Contract
                    - Grounds Supplies
                    - Heating/Cooling Repairs and Maintenance
                    - HVAC Maintenance
                    - Janitor and Cleaning Contract
                    - Janitor and Cleaning Supplies
                    - Landscape supplies
                    - Locks and Keys
                    - Miscellaneous Operating and Maintenance
                    - Other, Gasoline
                    - Painting / Decorating Supplies
                    - Repairs Contract
                    - Repairs Material
                    - Routine Replacements/Recurring Capital Expenses
                    - Security Payroll/Contract
                    - Snow Removal
                    - Swimming Pool Maintenance/Contract
                    - Termite Bond Expense
                    - Tools and Equipments
                    - Turnover 
                    - Utility Consulting                

                - Real Estate Taxes
                    - Pilot Payment
                    - Real Estate Tax Refund
                    - Real Estate taxes
                    - TIF Revenue (should reduce)                
                - Property and Liability Insurance
                    - Earthquake Insurance
                    - Flood Insurance
                    - Hazard Insurance
                    - Insurance Premiums
                    - Package Insurance
                    - Property and Liability insurance
                    - Umbrella Insurance                

                - Interest Expense - Hard Debt
                    - Debt Service
                    - FHMA Debt Payment
                    - Financing Expense
                    - Interest on 1st Mortgage (All Hard)
                    - Interest on 2nd Mortgage
                    - Interest on 3rd Mortgage
                    - Interest on 4th Mortgage
                    - Mortage Debt Payment
                    - Mortgage Payment
                    - USDA - RD interest                
                - Interest Expense - Construction
                    - Interest on Construction Loan                
                - Interest Expense - Soft Debt
                    - Interest Expense - Soft Debt
                    - SAIL  - HOME Interest                
                - Interest on Notes
                    - Interest Bridge Loan
                    - Interest on Developer Fees
                    - Interest on Ground Lease
                    - Interest on Notes Payable (Long Term)
                    - Interest on Partnership Loans
                    - Interest on Line of Credit
                    - Interest on Trust                
                - Amortization of Loan Issuance Costs
                    - Loan Issuance Costs

                - Loan Fees
                    - Lender Fee
                    - Servicing Fee
                    - Bond Issuer Fee
                    - Trustee Fee
                - Mortgage Insurance Premium (MIP)
                - Miscellaneous Financial Expenses
                    - Miscellaneous Financial Expenses
                    - Mortgage Overage                

                - Other Non-Cash Expenses (Income)
                    - Recurring (Non Recurring Non-Cash Expenses/Income) Items                
                - Depreciation/ Other Amortization
                    - Depreciation expense
                    - Amortization expense
                    - Land Lease (Amort of up front land lease pmts)
                    - Ground Lease (Amort of up front ground lease pmts)                
                - Partnership Fees
                    - Asset Management Fees
                    - Contingent Management Fees
                    - Deferred Management Fees
                    - Incentive Management Fees
                    - Investor Servicing Fee
                    - Lend Lease Payments
                    - Other Partnership Fees
                    - Partnership Management Fee
                    - Priority Distribution/Investor Distribution
                    - Special Limited Partner Fees
                    - Subordinate Management Fees
                    - Supervisory Management Fees 
                    - Supplemental Management Fees                
                - Non Recurring Non-Cash Expense
                    - Loss on Sale of Property
                    - Loss on Sale of Fixed Assets
                    - Realized Loss on Investments
                    - Prior Period Adjustments
                        - Prior Year Accounting Adjustment
                    - Casualty Loss Expense
                        - Loss from Property Damage                
                - Non Recurring Non-Cash (Income)
                    - Forgiveness of Debt
                    - Gain on Sale of Property
                    - Gain on Sale of Fixed Assets
                    - Realized Gain on Investments
                    - Prior Period Adjustment
                    - Loss on Extinguishment of Debt
                    - Casualty Gain

                - Capital Repairs Not Capitalized
                    - Capitalized Maintenance Expenses
                    - Non-Recurring Captial Expenses
                    - Extraordinary Expenses
                        - Any extraordinary maintenance expenses belongs to Capital Repairs Not Capitalized                
                - Non Recurring Cash Expense
                - Insurance Loss 
                - Legal Settlement Expense
                - Legal Fees related to Lawsuit
                - Mortgage Prepayment Penalty 
                - Organizational/Start Up Costs - DRM
                - Syndication Fee                
                - Non Recurring Cash (Income)
                - Insurance recovery/proceeds
                - Reserve Release
                - Grant Revenue - One time Grants (review footnotes to check if is annual grant - would not be Non - Recurring if so)
                - Bankruptcy Proceeds
                - Legal Settlement Income                
                - Impairment

                - Principal Payments - Hard Debt
                    - 1st Mortgage Principal Payment
                        - This item should be (-) 
                    - 2nd Mortgage Principal Payment
                        - This item should be (-) 
                    - 3rd Mortgage Principal Payment
                        - This item should be (-) 
                    - 4th Mortgage Principal Payment            
                        - This item should be (-) 
                - Principal Payments - Soft Debt
                        - This item should be (-) 
                - Principal Payments - Bonds - A
                        - This item should be (-) 
                - Principal Payments - Bonds - B
                        - This item should be (-) 
                - Principal Payments - Subordinate Taxable
                        - This item should be (-) 
                - Actual Replacement Reserve Deposits
                    - Actual Replacement Reserve Deposits
                    - Reserve Funding
                    - Replacement. Reserve - Held by SLN            
                - Replacement Reserve Withdrawals
                    - Capital Improvement Reimbursement
                    - Maintenance Paid Out of Reserve
                    - Replacement Reserve Withdrawals 
                    - Reserve Maintenance
                    - Reserve Reimbursement            
                - Interest Expense - Soft Debt Accrued           
                - Accrued Partnership Fees
                - Capital Improvements not Expensed
                    - Acquisition of property/equipment
                    - Capital Improvements/Expenditures
                    - Major Repairs and Maintenance
                    - Purchase of Fixed Assets
                    - Replacements
                    - Fixed Asset Replacements
                    - Total Capitalized Expenses
                    - Total Non-Capital Replacements             
                - Preferred Equity Distribution
                    - This item should be (-)
                - Other Adjustments

                - Capital Contributions
                - Deficit Funding
                - ILP Fund Advances
                - Other Cash Flow Adjustments

         ## extracted Income Statement Text: 
            ```{extracted_text}```   

         
         ## Respond in the JSON format as described below for the given extracted document text, do not remove any json fields, even if the field is not present or does not have any value:
               {json.dumps(income_statement_response_format, indent=2)}

            '''
   return income_statement_user_prompt
