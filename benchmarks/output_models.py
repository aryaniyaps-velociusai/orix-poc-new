from typing import Annotated

from pydantic import BaseModel, Field


class FieldEntry(BaseModel):
    field_label: Annotated[
        str, Field(description="The label of the field, e.g., 'Cash'")
    ]
    field_value: Annotated[
        str, Field(description="The value corresponding to the field label")
    ]
    pdf_document_page_number: Annotated[
        str,
        Field(
            description="The page number in the PDF document where this information is located",
        ),
    ]


class Assets(BaseModel):
    cash: Annotated[
        list[list[FieldEntry]],
        Field(description="List of entries for cash assets"),
    ]
    tenant_accounts_receivable: Annotated[
        list[list[FieldEntry]],
        Field(description="List of entries for tenant accounts receivable"),
    ]
    accounts_receivable_other: Annotated[
        list[list[FieldEntry]],
        Field(description="List of entries for other accounts receivable"),
    ]
    tenant_security_deposits: Annotated[
        list[list[FieldEntry]],
        Field(description="List of entries for tenant security deposits"),
    ]
    prepaid_property_insurances: Annotated[
        list[list[FieldEntry]],
        Field(description="List of entries for prepaid property insurances"),
    ]
    other_prepaid_expenses: Annotated[
        list[list[FieldEntry]],
        Field(description="List of entries for other prepaid expenses"),
    ]
    miscellaneous_current_assets: Annotated[
        list[list[FieldEntry]],
        Field(description="List of entries for miscellaneous current assets"),
    ]
    total_current_assets: Annotated[
        str, Field(description="Total value of current assets")
    ]
    real_estate_taxes_and_insurance_escrow: Annotated[
        list[list[FieldEntry]],
        Field(
            description="List of entries for real estate taxes and insurance escrow",
        ),
    ]
    reserve_for_replacement: Annotated[
        list[list[FieldEntry]],
        Field(description="List of entries for reserve for replacement"),
    ]
    operating_deficit_reserve: Annotated[
        list[list[FieldEntry]],
        Field(description="List of entries for operating deficit reserve"),
    ]
    bond_escrow: Annotated[
        list[list[FieldEntry]],
        Field(description="List of entries for bond escrow"),
    ]
    construction_escrow: Annotated[
        list[list[FieldEntry]],
        Field(description="List of entries for construction escrow"),
    ]
    miscellaneous_escrows: Annotated[
        list[list[FieldEntry]],
        Field(description="List of entries for miscellaneous escrows"),
    ]
    total_reserves_and_deposits: Annotated[
        str, Field(description="Total value of reserves and deposits")
    ]
    land: Annotated[
        list[list[FieldEntry]], Field(description="List of entries for land")
    ]
    fixed_assets: Annotated[
        list[list[FieldEntry]],
        Field(description="List of entries for fixed assets"),
    ]
    accumulated_depreciation: Annotated[
        list[list[FieldEntry]],
        Field(description="List of entries for accumulated depreciation"),
    ]
    total_fixed_assets: Annotated[str, Field(description="Total value of fixed assets")]
    other_assets: Annotated[
        list[list[FieldEntry]],
        Field(description="List of entries for other assets"),
    ]
    total_other_assets: Annotated[str, Field(description="Total value of other assets")]
    total_assets: Annotated[str, Field(description="Total value of all assets")]


class Liabilities(BaseModel):
    accounts_payable: Annotated[
        list[list[FieldEntry]],
        Field(description="List of entries for accounts payable"),
    ]
    accrued_property_taxes: Annotated[
        list[list[FieldEntry]],
        Field(description="List of entries for accrued property taxes"),
    ]
    other_accrued_expenses: Annotated[
        list[list[FieldEntry]],
        Field(description="List of entries for other accrued expenses"),
    ]
    tenant_security_deposits: Annotated[
        list[list[FieldEntry]],
        Field(description="List of entries for tenant security deposits"),
    ]
    accrued_management_fees: Annotated[
        list[list[FieldEntry]],
        Field(description="List of entries for accrued management fees"),
    ]
    prepaid_rent: Annotated[
        list[list[FieldEntry]],
        Field(description="List of entries for prepaid rent"),
    ]
    accrued_interest_payable: Annotated[
        list[list[FieldEntry]],
        Field(description="List of entries for accrued interest payable"),
    ]
    mortgage_notes_payable_current_portion: Annotated[
        list[list[FieldEntry]],
        Field(
            description="List of entries for mortgage notes payable (current portion)",
        ),
    ]
    construction_payable: Annotated[
        list[list[FieldEntry]],
        Field(description="List of entries for construction payable"),
    ]
    miscellaneous_current_liabilities: Annotated[
        list[list[FieldEntry]],
        Field(description="List of entries for miscellaneous current liabilities"),
    ]
    total_current_liabilities: Annotated[
        str, Field(description="Total value of current liabilities")
    ]
    mortgage_notes_payable_long_term: Annotated[
        list[list[FieldEntry]],
        Field(description="List of entries for mortgage notes payable (long-term)"),
    ]
    loan_issuance_costs_net_of_accum_amort: Annotated[
        list[list[FieldEntry]],
        Field(
            description="List of entries for loan issuance costs net of accumulated amortization",
        ),
    ]
    construction_loan: Annotated[
        list[list[FieldEntry]],
        Field(description="List of entries for construction loan"),
    ]
    developer_fee_payable: Annotated[
        list[list[FieldEntry]],
        Field(description="List of entries for developer fee payable"),
    ]
    development_advances: Annotated[
        list[list[FieldEntry]],
        Field(description="List of entries for development advances"),
    ]
    project_expense_loans: Annotated[
        list[list[FieldEntry]],
        Field(description="List of entries for project expense loans"),
    ]
    working_capital_loans: Annotated[
        list[list[FieldEntry]],
        Field(description="List of entries for working capital loans"),
    ]
    accrued_distributions_fees_to_ilpi: Annotated[
        list[list[FieldEntry]],
        Field(description="List of entries for accrued distributions fees to ILPI"),
    ]
    soft_debt_payable: Annotated[
        list[list[FieldEntry]],
        Field(description="List of entries for soft debt payable"),
    ]
    accrued_soft_debt_interest: Annotated[
        list[list[FieldEntry]],
        Field(description="List of entries for accrued soft debt interest"),
    ]
    ilp_loans: Annotated[
        list[list[FieldEntry]], Field(description="List of entries for ILP loans")
    ]
    other_long_term_liabilities: Annotated[
        list[list[FieldEntry]],
        Field(description="List of entries for other long-term liabilities"),
    ]
    total_long_term_liabilities: Annotated[
        str, Field(description="Total value of long-term liabilities")
    ]
    limited_partners_equity_deficiency: Annotated[
        list[list[FieldEntry]],
        Field(description="List of entries for limited partners' equity deficiency"),
    ]
    other_partners_equity_deficiency: Annotated[
        list[list[FieldEntry]],
        Field(description="List of entries for other partners' equity deficiency"),
    ]
    miscellaneous_equity_deficiency: Annotated[
        list[list[FieldEntry]],
        Field(description="List of entries for miscellaneous equity deficiency"),
    ]
    total_owners_equity: Annotated[
        str, Field(description="Total value of owners' equity")
    ]
    total_liabilities_and_equity: Annotated[
        str, Field(description="Total value of liabilities and equity")
    ]


class BalanceSheet(BaseModel):
    assets: Annotated[
        Assets, Field(description="The assets section of the balance sheet")
    ]
    liabilities: Annotated[
        Liabilities,
        Field(description="The liabilities section of the balance sheet"),
    ]


class BalanceSheetResponse(BaseModel):
    is_balance_sheet_present: Annotated[
        str,
        Field(description="Indicates if the balance sheet is present (Yes/No)"),
    ]
    balance_sheet: Annotated[
        BalanceSheet,
        Field(description="The balance sheet data containing assets and liabilities"),
    ]


class IncomeStatementFieldEntry(BaseModel):
    field_label: Annotated[
        str, Field(..., description="The label of the field, e.g., 'Cash'")
    ]
    field_value: Annotated[
        str, Field(..., description="The value corresponding to the field label")
    ]
    pdf_document_page_number: Annotated[
        str,
        Field(
            ...,
            description="The page number in the PDF document where this information is located",
        ),
    ]
    pdf_subheader_category: Annotated[
        str, Field(..., description="The subheader category from the PDF document")
    ]


class RevenueIncome(BaseModel):
    apartment_revenue: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(..., description="List of entries for apartment revenue"),
    ]
    gain_loss_to_lease: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(..., description="List of entries for gain/loss to lease"),
    ]
    commercial_revenue: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(..., description="List of entries for commercial revenue"),
    ]
    gross_potential_rent: Annotated[
        str, Field(..., description="Gross potential rent value")
    ]
    vacancy_apartments: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(..., description="List of entries for vacancy apartments"),
    ]
    vacancy_commercial: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(..., description="List of entries for vacancy commercial"),
    ]
    total_vacancy: Annotated[str, Field(..., description="Total value of vacancy")]
    bad_debt: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(..., description="List of entries for bad debt"),
    ]
    concessions: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(..., description="List of entries for concessions"),
    ]
    net_rental_revenue: Annotated[
        str, Field(..., description="Net rental revenue value")
    ]
    laundry: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(..., description="List of entries for laundry revenue"),
    ]
    parking: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(..., description="List of entries for parking revenue"),
    ]
    interest_income: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(..., description="List of entries for interest income"),
    ]
    miscellaneous_revenue: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(..., description="List of entries for miscellaneous revenue"),
    ]
    total_other_revenue: Annotated[
        str, Field(..., description="Total other revenue value")
    ]
    net_revenue: Annotated[str, Field(..., description="Net revenue value")]


class Expenses(BaseModel):
    administrative_payroll: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(..., description="List of entries for administrative payroll"),
    ]
    management_fee: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(..., description="List of entries for management fees"),
    ]
    administrative_expenses: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(..., description="List of entries for administrative expenses"),
    ]
    total_administrative_expenses: Annotated[
        str, Field(..., description="Total administrative expenses value")
    ]
    water_sewer: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(..., description="List of entries for water and sewer expenses"),
    ]
    other_utilities_expense: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(..., description="List of entries for other utilities expenses"),
    ]
    total_utilities_expense: Annotated[
        str, Field(..., description="Total utilities expense value")
    ]
    maintenance_payroll: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(..., description="List of entries for maintenance payroll"),
    ]
    trash_removal: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(..., description="List of entries for trash removal"),
    ]
    maintenance_expenses: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(..., description="List of entries for maintenance expenses"),
    ]
    total_maintenance_expenses: Annotated[
        str, Field(..., description="Total maintenance expenses value")
    ]
    real_estate_taxes: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(..., description="List of entries for real estate taxes"),
    ]
    property_liability_insurance: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(..., description="List of entries for property liability insurance"),
    ]
    total_taxes_and_insurance: Annotated[
        str, Field(..., description="Total taxes and insurance value")
    ]
    total_operating_expenses: Annotated[
        str, Field(..., description="Total operating expenses value")
    ]
    net_operating_income: Annotated[
        str, Field(..., description="Net operating income value")
    ]
    interest_expense_hard_debt: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(..., description="List of entries for interest expense on hard debt"),
    ]
    interest_expense_construction: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(..., description="List of entries for interest expense on construction"),
    ]
    interest_expense_soft_debt: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(..., description="List of entries for interest expense on soft debt"),
    ]
    interest_on_notes: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(..., description="List of entries for interest on notes"),
    ]
    amortization_of_loan_issuance_costs: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(
            ..., description="List of entries for amortization of loan issuance costs"
        ),
    ]
    total_interest_on_mortgage_notes: Annotated[
        str, Field(..., description="Total interest on mortgage notes")
    ]
    loan_fees: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(..., description="List of entries for loan fees"),
    ]
    mortgage_insurance_premium: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(..., description="List of entries for mortgage insurance premium"),
    ]
    miscellaneous_financial_expenses: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(..., description="List of entries for miscellaneous financial expenses"),
    ]
    total_financial_expenses: Annotated[
        str, Field(..., description="Total financial expenses")
    ]
    other_non_cash_expenses_income: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(..., description="List of entries for other non-cash expenses/income"),
    ]
    depreciation_other_amortization: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(
            ...,
            description="List of entries for depreciation and amortization of other expenses",
        ),
    ]
    partnership_fees: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(..., description="List of entries for partnership fees"),
    ]
    non_recurring_non_cash_expense: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(..., description="List of entries for non-recurring non-cash expenses"),
    ]
    non_recurring_non_cash_income: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(..., description="List of entries for non-recurring non-cash income"),
    ]
    capital_repairs_not_capitalized: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(..., description="List of entries for capital repairs not capitalized"),
    ]
    non_recurring_cash_expense: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(..., description="List of entries for non-recurring cash expenses"),
    ]
    non_recurring_cash_income: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(..., description="List of entries for non-recurring cash income"),
    ]
    impairment: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(..., description="List of entries for impairment"),
    ]
    net_profit_loss: Annotated[str, Field(..., description="Net profit or loss value")]
    principal_payments_hard_debt: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(..., description="List of entries for principal payments on hard debt"),
    ]
    principal_payments_soft_debt: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(..., description="List of entries for principal payments on soft debt"),
    ]
    total_mortgage_principal_payments: Annotated[
        str, Field(..., description="Total mortgage principal payments value")
    ]
    depreciation_amort_other_non_cash: Annotated[
        str,
        Field(..., description="Depreciation and amortization of other non-cash items"),
    ]
    actual_replacement_reserve_deposits: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(
            ..., description="List of entries for actual replacement reserve deposits"
        ),
    ]
    replacement_reserve_withdrawals: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(..., description="List of entries for replacement reserve withdrawals"),
    ]
    interest_expense_soft_debt_accrued: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(
            ..., description="List of entries for accrued interest expense on soft debt"
        ),
    ]
    accrued_partnership_fees: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(..., description="List of entries for accrued partnership fees"),
    ]
    capital_improvements_not_expensed: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(..., description="List of entries for capital improvements not expensed"),
    ]
    preferred_equity_distribution: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(..., description="List of entries for preferred equity distribution"),
    ]
    other_adjustments: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(..., description="List of entries for other adjustments"),
    ]
    total_operating_cash_flow: Annotated[
        str, Field(..., description="Total operating cash flow value")
    ]
    capital_contributions: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(..., description="List of entries for capital contributions"),
    ]
    deficit_funding: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(..., description="List of entries for deficit funding"),
    ]
    ilp_fund_advances: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(..., description="List of entries for ILP fund advances"),
    ]
    other_cash_flow_adjustments: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(..., description="List of entries for other cash flow adjustments"),
    ]
    total_net_cash_flow: Annotated[
        str, Field(..., description="Total net cash flow value")
    ]


class IncomeStatement(BaseModel):
    revenue_income: Annotated[
        RevenueIncome, Field(..., description="Revenue income details")
    ]
    expenses: Annotated[Expenses, Field(..., description="Expense details")]
    unmapped_fields: Annotated[
        list[list[IncomeStatementFieldEntry]],
        Field(..., description="Unmapped fields with reasons for non-mapping"),
    ]


class IncomeStatementResponse(BaseModel):
    is_income_statement_present: Annotated[
        str,
        Field(
            ...,
            description="Indicates whether the income statement is present (Yes/No)",
        ),
    ]
    income_statement: Annotated[
        IncomeStatement,
        Field(
            ...,
            description="The income statement data containing revenue income, expenses, and unmapped fields",
        ),
    ]
