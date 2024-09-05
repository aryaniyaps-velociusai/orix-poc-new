# ############################
# ############################
# BALANCE SHEET
# ############################
# ############################


# calculate_balance_sheet_total_assets
def calculate_balance_sheet_total_assets(balance_sheet):
    try:
        assets = balance_sheet["assets"]

        total_current_assets_subtotal_fields = [
            "cash",
            "tenant_accounts_receivable",
            "accounts_receivable_other",
            "tenant_security_deposits",
            "prepaid_property_insurances",
            "other_prepaid_expenses",
            "miscellaneous_current_assets"
        ]



        total_current_assets = 0

        for field in total_current_assets_subtotal_fields:
            total_current_assets += assets[field]["total"]
        assets["total_current_assets"]["total"] = total_current_assets


        total_reserves_and_deposits_subtotal_fields = [
            "real_estate_taxes_and_insurance_escrow",
            "reserve_for_replacement",
            "operating_deficit_reserve",
            "miscellaneous_escrows"
        ]
        total_reserves_and_deposits = 0

        for field in total_reserves_and_deposits_subtotal_fields:
            total_reserves_and_deposits += assets[field]["total"]

        assets["total_reserves_and_deposits"]["total"] = total_reserves_and_deposits


        total_fixed_assets_subtotal_fields = [
            "land",
            "fixed_assets",
            "accumulated_depreciation"
        ]
        total_fixed_assets = 0

        for field in total_fixed_assets_subtotal_fields:
            total_fixed_assets += assets[field]["total"]
        assets["total_fixed_assets"]["total"] = total_fixed_assets

        total_other_assets_subtotal_fields = [
            "other_assets"
        ]
        total_other_assets = 0

        for field in total_other_assets_subtotal_fields:
            total_other_assets += assets[field]["total"]
        assets["total_other_assets"]["total"] = total_other_assets
        

        total_assets_subtotal_fields = [
            "total_current_assets",
            "total_reserves_and_deposits",
            "total_fixed_assets",
            "total_other_assets"
        ]

        total_assets = 0

        for field in total_assets_subtotal_fields:
            total_assets += assets[field]["total"]
        assets["total_assets"]["total"] = total_assets
    except Exception as e:
        print(f"Error occured in: {calculate_balance_sheet_total_assets.__name__}")
        raise e





# calculate_balance_sheet_total_liabilities
def calculate_balance_sheet_total_liabilities(balance_sheet):
    try:
        liabilities = balance_sheet["liabilities"]

        total_current_liabilities_subtotal_fields = [
            "accounts_payable",
            "other_accrued_expenses",
            "tenant_security_deposits",
            "prepaid_rent",
            "accrued_interest_payable",
            "accrued_property_taxes"
        ]


        total_current_liabilities = 0

        for field in total_current_liabilities_subtotal_fields:
            total_current_liabilities += liabilities[field]["total"]
        liabilities["total_current_liabilities"]["total"] = total_current_liabilities

        total_long_term_liabilities_subtotal_fields = [
            "mortgage_notes_payable_long_term",
            "developer_fee_payable",
            "project_expense_loans",
            "soft_debt_payable"
        ]
        total_long_term_liabilities = 0

        for field in total_long_term_liabilities_subtotal_fields:
            total_long_term_liabilities += liabilities[field]["total"]

        liabilities["total_long_term_liabilities"]["total"] = total_long_term_liabilities


        total_owners_equity_subtotal_fields = [
            "limited_partners_equity_deficiency",
            "other_partners_equity_deficiency",
            "miscellaneous_equity_deficiency"
        ]

        total_owners_equity = 0

        for field in total_owners_equity_subtotal_fields:
            total_owners_equity += liabilities[field]["total"]
        liabilities["total_owners_equity"]["total"] = total_owners_equity
        

        total_liabilities_and_equity_subtotal_fields = [
            "total_current_liabilities",
            "total_long_term_liabilities",
            "total_owners_equity"
        ]
        total_liabilities_and_equity = 0

        for field in total_liabilities_and_equity_subtotal_fields:
            total_liabilities_and_equity += liabilities[field]["total"]
        liabilities["total_liabilities_and_equity"]["total"] = total_liabilities_and_equity
    except Exception as e:
        print(f"Error occured in: {calculate_balance_sheet_total_liabilities.__name__}")
        raise e


# ############################
# ############################
# INCOME STATEMENT
# ############################
# ############################



def calculate_income_statement_total_income(income_statement):
    try:
        revenue_income = income_statement["revenue_income"]

        gross_potential_rent_subtotal_fields = [
            "apartment_revenue",
            "gain_loss_to_lease",
            "commercial_revenue",
        ]

        gross_potential_rent = 0

        for field in gross_potential_rent_subtotal_fields:
            gross_potential_rent += revenue_income[field]["total"]
        revenue_income["gross_potential_rent"]["total"] = gross_potential_rent


        total_vacancy_subtotal_fields = [
            "vacancy_apartments",
            "vacancy_commercial"
        ]

        total_vacancy = 0

        for field in total_vacancy_subtotal_fields:
            total_vacancy += revenue_income[field]["total"]

        revenue_income["total_vacancy"]["total"] = total_vacancy

        net_rental_revenue_subtotal_fields = [
            "gross_potential_rent",
            "total_vacancy",
            "bad_debt",
            "concessions"
        ]
        net_rental_revenue = 0

        for field in net_rental_revenue_subtotal_fields:
            net_rental_revenue += revenue_income[field]["total"]

        revenue_income["net_rental_revenue"]["total"] = net_rental_revenue
        

        total_other_revenue_subtotal_fields = [
            "laundry",
            "parking",
            "interest_income",
            "miscellaneous_revenue"
        ]
        total_other_revenue = 0

        for field in total_other_revenue_subtotal_fields:
            total_other_revenue += revenue_income[field]["total"]

        revenue_income["total_other_revenue"]["total"] = total_other_revenue
        
        net_revenue_subtotal_fields = [
            "net_rental_revenue",
            "total_other_revenue"
        ]
        net_revenue = 0

        for field in net_revenue_subtotal_fields:
            net_revenue += revenue_income[field]["total"]

        revenue_income["net_revenue"]["total"] = net_revenue
    except Exception as e:
        print(f"Error occured in: {calculate_income_statement_total_income.__name__}")
        raise e



def calculate_income_statement_total_expense(income_statement):
    try:
        expenses = income_statement["expenses"]

        total_administrative_expenses_subtotal_fields = [
            "administrative_payroll",
            "management_fee",
            "administrative_expenses",
        ]

        total_administrative_expenses = 0

        for field in total_administrative_expenses_subtotal_fields:
            total_administrative_expenses += expenses[field]["total"]
        expenses["total_administrative_expenses"]["total"] = total_administrative_expenses


        total_utilities_expense_subtotal_fields = [
            "water_sewer",
            "other_utilities_expense"
        ]
        
        total_utilities_expense = 0

        for field in total_utilities_expense_subtotal_fields:
            total_utilities_expense += expenses[field]["total"]
        expenses["total_utilities_expense"]["total"] = total_utilities_expense


        total_maintenance_expenses_subtotal_fields = [
            "maintenance_payroll",
            "trash_removal",
            "maintenance_expenses"
        ]
        
        total_maintenance_expenses = 0

        for field in total_maintenance_expenses_subtotal_fields:
            total_maintenance_expenses += expenses[field]["total"]
        expenses["total_maintenance_expenses"]["total"] = total_maintenance_expenses



        total_taxes_and_insurance_subtotal_fields = [
            "real_estate_taxes",
            "property_liability_insurance"
        ]
        total_taxes_and_insurance = 0

        for field in total_taxes_and_insurance_subtotal_fields:
            total_taxes_and_insurance += expenses[field]["total"]
        expenses["total_taxes_and_insurance"]["total"] = total_taxes_and_insurance

        total_operating_expenses_subtotal_fields = [
            "total_administrative_expenses",
            "total_utilities_expense",
            "total_maintenance_expenses",
            "total_taxes_and_insurance"
        ]
        
        total_operating_expenses = 0

        for field in total_operating_expenses_subtotal_fields:
            total_operating_expenses += expenses[field]["total"]
        expenses["total_operating_expenses"]["total"] = total_operating_expenses


        net_operating_income_subtotal_fields = [ # net_revenue - total_operating_expenses
            "net_revenue", # revenue field, change approach for calculating this field
            "total_operating_expenses",
        ]

        net_operating_income = income_statement["revenue_income"]["net_revenue"]["total"] - expenses["total_operating_expenses"]["total"]

        expenses["net_operating_income"]["total"] = net_operating_income


        total_interest_on_mortgage_notes_subtotal_fields = [
            "interest_expense_hard_debt",
            "interest_expense_construction",
            "interest_expense_soft_debt",
            "interest_on_notes",
            "amortization_of_loan_issuance_costs"
        ]
        total_interest_on_mortgage_notes = 0

        for field in total_interest_on_mortgage_notes_subtotal_fields:
            total_interest_on_mortgage_notes += expenses[field]["total"]
        expenses["total_interest_on_mortgage_notes"]["total"] = total_interest_on_mortgage_notes


        total_financial_expenses_subtotal_fields = [
            "loan_fees",
            "mortgage_insurance_premium",
            "miscellaneous_financial_expenses"
        ]
        total_financial_expenses = 0

        for field in total_financial_expenses_subtotal_fields:
            total_financial_expenses += expenses[field]["total"]
        expenses["total_financial_expenses"]["total"] = total_financial_expenses
        
        net_profit_loss_subtotal_fields = [ # net_operating_income - below
            "total_interest_on_mortgage_notes",
            "total_financial_expenses",
            "other_non_cash_expenses_income",
            "depreciation_other_amortization",
            "partnership_fees",
            "non_recurring_non_cash_expense",
            "non_recurring_non_cash_income",
            "capital_repairs_not_capitalized",
            "non_recurring_cash_expense",
            "non_recurring_cash_income",
            "impairment"
        ]

        net_profit_loss = 0

        for field in net_profit_loss_subtotal_fields:
            net_profit_loss += expenses[field]["total"]
        net_profit_loss = net_operating_income - net_profit_loss
        expenses["net_profit_loss"]["total"] = net_profit_loss

        total_mortgage_principal_payments_subtotal_fields = [
            "principal_payments_hard_debt",
            "principal_payments_soft_debt"
        ]

        total_mortgage_principal_payments = 0

        for field in total_mortgage_principal_payments_subtotal_fields:
            total_mortgage_principal_payments += expenses[field]["total"]
        expenses["total_mortgage_principal_payments"]["total"] = total_mortgage_principal_payments


        depreciation_amort_other_non_cash_subtotal_fields = [
            "other_non_cash_expenses_income",
            "depreciation_other_amortization",
            "partnership_fees",
            "non_recurring_non_cash_expense",
            "non_recurring_non_cash_income",
            "capital_repairs_not_capitalized",
            "non_recurring_cash_expense",
            "non_recurring_cash_income",
            "impairment"
        ]

        depreciation_amort_other_non_cash = 0

        for field in depreciation_amort_other_non_cash_subtotal_fields:
            depreciation_amort_other_non_cash += expenses[field]["total"]
        expenses["depreciation_amort_other_non_cash"]["total"] = depreciation_amort_other_non_cash

        total_operating_cash_flow_subtotal_fields = [
            "net_profit_loss",
            "total_mortgage_principal_payments",
            "depreciation_amort_other_non_cash",
            "actual_replacement_reserve_deposits",
            "replacement_reserve_withdrawals",
            "interest_expense_soft_debt_accrued",
            "accrued_partnership_fees",
            "capital_improvements_not_expensed",
            "preferred_equity_distribution",
            "other_adjustments"
        ]


        total_operating_cash_flow = 0

        for field in total_operating_cash_flow_subtotal_fields:
            total_operating_cash_flow += expenses[field]["total"]
        expenses["total_operating_cash_flow"]["total"] = total_operating_cash_flow


        total_net_cash_flow_subtotal_fields = [ # total_operating_cash_flow - below
            "capital_contributions",
            "deficit_funding",
            "ilp_fund_advances",
            "other_cash_flow_adjustments"
        ]

        total_net_cash_flow = 0

        for field in total_net_cash_flow_subtotal_fields:
            total_net_cash_flow += expenses[field]["total"]
        total_net_cash_flow = total_operating_cash_flow - total_net_cash_flow
        expenses["total_net_cash_flow"]["total"] = total_net_cash_flow
    except Exception as e:
        print(f"Error occured in: {calculate_income_statement_total_expense.__name__}")
        raise e
    


def calculate_dict_total(dict_obj):
    try:
        for key, sub_dict in dict_obj.items():
            sub_dict["total"] = 0

            if isinstance(sub_dict, dict):
                sub_dict_field_total = sum([float(field["value"]) for field in sub_dict["fields"]])
                sub_dict["total"] = sub_dict_field_total
    except Exception as e:
        print(f"Error occured in: {calculate_dict_total.__name__}")
        raise e

def calculate_field_total_values(new_json_response):
    try:
        if new_json_response["is_balance_sheet_present"] == "Yes":
            assets = new_json_response["balance_sheet"]["assets"]
            liabilities = new_json_response["balance_sheet"]["liabilities"]
            calculate_dict_total(assets)
            calculate_dict_total(liabilities)

        if new_json_response["is_income_statement_present"] == "Yes":
            income = new_json_response["income_statement"]["revenue_income"]
            expenses = new_json_response["income_statement"]["expenses"]
            calculate_dict_total(income)
            calculate_dict_total(expenses)

        # print(json.dumps(new_json_response["balance_sheet"], indent=2))
    except Exception as e:
        print(f"Error occured in: {calculate_field_total_values.__name__}")
        raise e

    

    

def calculate_totals(json_response):
    try:
        calculate_field_total_values(json_response)

        if json_response["is_balance_sheet_present"] == "Yes":
            calculate_balance_sheet_total_assets(json_response["balance_sheet"])
            calculate_balance_sheet_total_liabilities(json_response["balance_sheet"])

        if json_response["is_income_statement_present"] == "Yes":
            calculate_income_statement_total_income(json_response["income_statement"])
            calculate_income_statement_total_expense(json_response["income_statement"])
        return json_response
    except Exception as e:
        print(f"Error occured in: {calculate_totals.__name__}")
        raise e

