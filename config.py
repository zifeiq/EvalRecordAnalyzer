LANG_CONFIG = {
    "latin": {
        "en_US",
        "es_ES",
        "fr_FR",
        "de_DE",
        "cz_CZ",
        "da_DA",
        "hu_HU",
        "it_IT",
        "nl_NL",
        "no_NO",
        "pl_PL",
        "pt_PT",
        "single_char",
        "sv_SV",
        "tr_TR",
        "Vertical_BizCard",
        "Vertical_IdDocument",
        "Vertical_Invoice",
        "Vertical_Receipt",
    },
    'latin_hw': {
        'en_US_hw',
        'es_ES_hw',
        'fr_FR_hw',
        'it_IT_hw',
        'pt_PT_hw',
        'de_DE_hw',
    },
    "cjk": {
        "zh_CN",
        "ja_JP",
        "zh_TW",
        "ko_KR",
    },
    "cjk_hw": {
        "zh_CN_hw",
        "ja_JP_hw",
        "ko_KR_hw",
    }
}

DOC_TYPED_SEGMENTS = [
    'Document',
    'Invoice',
    'Receipt',
    'EyeChart',
    'Table',
    'CharacterBox',

    # Handwriting categories
    'BankChecks',
    'TravelerEntryForms',
    'BillsReceipts',
    'Applications',
    'MedicalPrescriptions',
    'Invoices',
    'Contracts',
    'Tables',
    'HandwrittenNotes',
]

ENTITY_UNION_CONFIG = {
    'TextAnalyticsAPI_DateTime_EntityGroup': [
        'TextAnalyticsAPI_DateTime',
        'TextAnalyticsAPI_DateTime_Date',
        'TextAnalyticsAPI_DateTime_Time',
        'TextAnalyticsAPI_DateTime_DateRange',
        'TextAnalyticsAPI_DateTime_TimeRange',
        'TextAnalyticsAPI_DateTime_Duration',
        'TextAnalyticsAPI_DateTime_Set',
    ],
    'TextAnalyticsAPI_Quantity_EntityGroup': [
        'TextAnalyticsAPI_Quantity',
        'TextAnalyticsAPI_Quantity_Number',
        'TextAnalyticsAPI_Quantity_Percentage',
        'TextAnalyticsAPI_Quantity_OrdinalNumbers',
        'TextAnalyticsAPI_Quantity_Age',
        'TextAnalyticsAPI_Quantity_Currency',
        'TextAnalyticsAPI_Quantity_Dimensions',
        'TextAnalyticsAPI_Quantity_Temperature',
    ],
    'Invoice_Identifiers_EntityGroup': [
        'Invoice_PONumber',
        'Invoice_ItemsPO',
        'Invoice_ItemsProductCode',
        'Invoice_InvoiceNumber',
        'Invoice_CustomerID',
    ],
    'Invoice_Address_EntityGroup': [
        'Invoice_BillingAddress',
        'Invoice_CustomerAddress_Other',
        'Invoice_RemittanceAddress',
        'Invoice_ServiceAddress',
        'Invoice_ShippingAddress',
        'Invoice_VendorAddress_Other',
    ],
    'Invoice_Dates_EntityGroup': [
        'Invoice_InvoiceDate',
        'Invoice_DueDate',
        'Invoice_ItemsDate',
        'Invoice_ServiceEndDate',
        'Invoice_ServiceStartDate',
    ],
    'Invoice_Prices_EntityGroup': [
        'Invoice_ItemsAmount',
        'Invoice_ItemsDiscount',
        'Invoice_ItemsTax',
        'Invoice_ItemsUnitPrice',
        'Invoice_PreviousUnpaidBalance',
        'Invoice_Subtotal',
        'Invoice_TotalAmountDue',
        'Invoice_TotalCurrentCharges',
        'Invoice_TotalTax',
    ],
    'Invoice_Numbers_EntityGroup': [
        'Invoice_Prices_EntityGroup',
        'Invoice_Dates_EntityGroup',
        'Invoice_ItemsIndex',
        'Invoice_ItemsOrderQuantity',
        'Invoice_ItemsOthers',
        'Invoice_ItemsQuantity',
    ],
    'Invoice_Names_EntityGroup': [
        'Invoice_BillingName',
        'Invoice_Customer',
        'Invoice_CustomerName',
        'Invoice_RemittanceName',
        'Invoice_ServiceName',
        'Invoice_ShippingName',
        'Invoice_Vendor',
        'Invoice_VendorName_Other',
    ],
    'Receipt_Price_EntityGroup': [
        'Receipt_Total', 'Receipt_Subtotal', 'Receipt_Tax',
        'Receipt_TotalPrice', 'Receipt_Tip'
    ],
    'Receipt_DateTime_EntityGroup':
    ['Receipt_TransactionDate', 'Receipt_TransactionTime'],
    'Receipt_Payment_EntityGroup': [
        'Receipt_PaymentType',
        'Receipt_Amount',
        'Receipt_CardNumber',
        'Receipt_CardTransType',
        'Receipt_TransDate',
        'Receipt_TransTime',
        'Receipt_ApprovalMethod',
        'Receipt_ApprovalCode',
    ],
    'DriverLicense_Date_EntityGroup':
    ['DriverLicense_DateOfBirth', 'DriverLicense_DateOfExpiration'],
    'DriverLicense_Name_EntityGroup': [
        'DriverLicense_FirstName', 'DriverLicense_LastName',
        'DriverLicense_FullName'
    ],
    'BusinessCard_PhoneNumber_EntityGroup': [
        'BusinessCard_WorkPhones',
        'BusinessCard_Faxes',
        'BusinessCard_MobilePhones',
    ],
    'BusinessCard_Name_EntityGroup':
    ['BusinessCard_FirstName', 'BusinessCard_LastName'],
    'BusinessCard_Titles_EntityGroup':
    ['BusinessCard_Title', 'BusinessCard_JobTitles'],
}