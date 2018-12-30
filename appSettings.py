from os.path import join, dirname
from json import load

file_path = join(dirname(__file__), 'template.json')
with open(file_path) as file_obj:
    lokri_dict = load(file_obj)
    CUSTOMER_NAME = lokri_dict['companyName']
    GSTIN = lokri_dict['gstin']
    STATE_CODE = lokri_dict['stateCode']
    STATE_NAME = lokri_dict['stateName']
    ADDRESS1_ROW, ADDRESS1_COLUMN, ADDRESS1 = lokri_dict['address1']
    ADDRESS2_ROW, ADDRESS2_COLUMN, ADDRESS2 = lokri_dict['address2']
    CUSTOMER_ROW, CUSTOMER_COL = lokri_dict['companyData']
    COMPANY_TAG = lokri_dict['companyTag']
    TAG_ROW, TAG_COL = lokri_dict['tagData']
    BANK_CUSTOMER_NAME = lokri_dict['bankCustomerName']
    BANK_BRANCH = lokri_dict['bankBranchName']
    ACCOUNT_NO = lokri_dict['accountNo']
    IFSC_CODE = lokri_dict['ifscCode']
    BANK_FONT = lokri_dict['bankFont']
    PHONE_NO = lokri_dict['phoneNo']
    INVOICE_BILL_NO = lokri_dict['billStart']
    PERFORMA_BILL_NO = lokri_dict['performaBillStart']