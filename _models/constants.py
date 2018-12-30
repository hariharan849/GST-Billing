from collections import namedtuple


_columnId = 0
_columnName = 1
_columnLinkedId = 2
_columnType = 3

_voucherSettings = [
    ['voucherNo', 'Voucher No', 0, 0],
    ['customerName', 'Customer Name', 0, 0],
    ['debitDate', 'Credit Date', 0, 0],
    ['remarks', 'Remarks', 0, 0],
    ['paymentType', 'Payment Mode', 0, 0],
    ['chequeNo', 'Cheque No', 0, 0],
    ['amount', 'Amount', 0, 0],
    ['cancelReason', 'Cancel Reason', 0, 0]
]


_addCustomerSettings = [
    ['customerCode', 'Customer Code', 0, 0],
    ['customerName', 'Customer Name', 0, 0],
    ['customerAddress', 'Customer Address', 0, 0],
    ['gstin', 'GSTIN', 0, 0],
    ['contactNo', 'Customer Contact', 0, 0],
    ['stateCode', 'State Code', 0, 0]
]


_companyItemSettings = [
    ['itemCode', 'Item Code', 0, 0],
    ['particulars', 'Particulars', 0, 0],
    ['hsnCode', 'HSN Code', 0, 0],
    ['quantity', 'Quantity', 0, 0],
    ['rate', 'Rate', 0, 0]
]


_quotationSettings = [
    ['itemCode', 'Item Code', 0, 0],
    ['particulars', 'Particulars', 0, 0],
    ['hsnCode', 'HSN Code', 0, 0],
    ['quantity', 'Qty', 0, 0],
    ['rate', 'Rate', 0, 0],
    ['cgstValue', 'CGST', 0, 0],
    ['sgstValue', 'SGST', 0, 0],
    ['igstValue', 'IGST', 0, 0],
    ['amount', 'Amount', 0, 0],
    ['tax', 'Tax', 0, 0],
    ['total', 'Total', 0, 0]
]


_quotationReportSettings = [
    ['customerName', 'Customer Name', 0, 0],
    ['customerAddress', 'Customer Address', 0, 0],
    ['quotationNo', 'Quotation No', 0, 0],
    ['quotationDate', 'Quotation Date', 0, 0],
    ['validUntilDate', 'Valid Until', 0, 0],
    ['amount', 'Amount', 0, 0],
    ['tax', 'Tax', 0, 0],
    ['total', 'Total', 0, 0],
    ['cancelReason', 'Cancel Reason', 0, 0]
]


_purchaseOrderSettings = [
    ['itemCode', 'Item Code', 0, 0],
    ['particulars', 'Particulars', 0, 0],
    ['hsnCode', 'HSN Code', 0, 0],
    ['quantity', 'Qty', 0, 0]
]


_purchaseOrderReportSettings = [
    ['customerName', 'Customer Name', 0, 0],
    ['poNo', 'Purchase Order No', 0, 0],
    ['poDate', 'Purchase Order Date', 0, 0],
    ['remarks', 'Remarks', 0, 0],
    ['cancelReason', 'Cancel Reason', 0, 0]
]


_salesReportSettings = [
    ['customerName', 'Customer Name', 0, 0],
    ['customerAddress', 'Customer Address', 0, 0],
    ['billNo', 'Bill No', 0, 0],
    ['paidBy', 'Paid By', 0, 0],
    ['invoiceDate', 'Invoice Date', 0, 0],
    ['vendorCode', 'Vendor Code', 0, 0],
    ['paymentTerms', 'Payment Terms', 0, 0],
    ['amount', 'Amount', 0, 0],
    ['tax', 'Tax', 0, 0],
    ['total', 'Total', 0, 0],
    ['amountPaid', 'Amount Paid', 0, 0],
    ['balance', 'Balance', 0, 0],
    ['paymentRemarks', 'Payment Remarks', 0, 0],
    ['status', 'Status', 0, 0],
    ['cancelReason', 'Cancel Reason', 0, 0]
]

_purchaseReportSettings = [
    ['vendorName', 'Vendor Name', 0, 0],
    ['vendorAddress', 'Vendor Address', 0, 0],
    ['vendorGstin', 'GSTIN', 0, 0],
    ['vendorStateCode', 'State Code', 0, 0],
    ['billNo', 'Bill No', 0, 0],
    ['billDate', 'Bill Date', 0, 0],
    ['dueDate', 'Due Date', 0, 0],
    ['paidBy', 'Paid By', 0, 0],
    ['amount', 'Amount', 0, 0],
    ['tax', 'Tax', 0, 0],
    ['total', 'Total', 0, 0],
    ['amountPaid', 'Amount Paid', 0, 0],
    ['balance', 'Balance', 0, 0],
    ['remarks', 'Payment Remarks', 0, 0],
    ['status', 'Status', 0, 0],
    ['cancelReason', 'Cancel Reason', 0, 0]
]


valueWrapper = namedtuple('valueWrapper', 'value flag')
dateFilter = namedtuple('dateFilter', 'fromDate toDate')