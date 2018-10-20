from os.path import join, dirname
from json import load

file_path = join(dirname(__file__), 'appSettings.json')
with open(file_path) as file_obj:
    lokri_dict = load(file_obj)
    CUSTOMER_NAME = lokri_dict['company_name']
    GSTIN = lokri_dict['gstin']
    STATE_CODE = lokri_dict['state_code']
    STATE_NAME = lokri_dict['state_name']
    ADDRESS1_ROW, ADDRESS1_COLUMN, ADDRESS1 = lokri_dict['address1']
    ADDRESS2_ROW, ADDRESS2_COLUMN, ADDRESS2 = lokri_dict['address2']
    CUSTOMER_ROW, CUSTOMER_COL = lokri_dict['company_data']
    COMPANY_TAG = lokri_dict['company_tag']
    TAG_ROW, TAG_COL = lokri_dict['tag_data']
    BANK_CUSTOMER_NAME = lokri_dict['bank_customer_name']
    BANK_BRANCH = lokri_dict['bank_branch_name']
    ACCOUNT_NO = lokri_dict['account_no']
    IFSC_CODE = lokri_dict['ifsc_code']
    BANK_FONT = lokri_dict['bank_font']
    PHONE_NO = lokri_dict['phone_no']
    INVOICE_BILL_NO = lokri_dict['bill_start']
    PERFORMA_BILL_NO = lokri_dict['performa_bill_start']