
from mongoengine import *
connect('gstDetails')

class Voucher(DynamicDocument):
    voucherNo = StringField(max_length=200, required=True)
    customerName = StringField(max_length=200, required=True)
    voucherDate = DateTimeField(required=True)
    remarks = StringField(max_length=200, required=True)
    paymentType = StringField(max_length=100, required=True)
    chequeNo = StringField(max_length=50, required=True)
    amount = StringField(max_length=50, required=True)
    type = StringField(max_length=50, required=True)


class CompanyItems(DynamicDocument):
    itemCode = StringField(max_length=200, required=True)
    itemName = StringField(max_length=200, required=True)
    hsnCode = StringField(max_length=200, required=True)
    quantity = StringField(max_length=200, required=True)
    itemPrice = FloatField(required=True)
    type = StringField(max_length=100, required=True)


class CustomerNames(DynamicDocument):
    custCode = StringField(max_length=100, required=True)
    custName = StringField(max_length=200, required=True)
    custAddress = StringField(max_length=200, required=True)
    gstin = StringField(max_length=200, required=True)
    stateCode = IntField(required=True)
    contactNo = StringField(max_length=20, required=True)


class PurchaseOrder(DynamicDocument):
    customerName = StringField(max_length=200, required=True)
    poNo = IntField(required=True)
    poDate = DateTimeField(required=True)
    remarks = StringField(max_length=200, required=True)
    cancelReason = StringField(max_length=200, required=False)

class PurchaseOrderProducts(DynamicDocument):
    poNo = ReferenceField('PurchaseOrder', reverse_delete_rule=CASCADE)
    itemCode = StringField(max_length=200, required=True)
    particular = StringField(max_length=200, required=True)
    hsnCode = StringField(max_length=200, required=True)
    quantity = StringField(max_length=100, required=True)


class QuotationDetails(DynamicDocument):
    customerName = StringField(max_length=200, required=True)
    customerAddress = StringField(max_length=200, required=True)
    quotationNo = IntField(required=True)
    quotationValidity = DateTimeField(required=True)
    quotationDate = DateTimeField(required=True)
    estAmount = FloatField(required=True)
    estTotal = FloatField(required=True)
    remarks = StringField(max_length=200, required=True)
    cancelReason = StringField(max_length=200, required=False)

class QuotationItems(DynamicDocument):
    quotationNo = ReferenceField('QuotationDetails', reverse_delete_rule=CASCADE)
    itemCode = StringField(max_length=100, required=True)
    particular = StringField(max_length=200, required=True)
    hsnCode = StringField(max_length=200, required=True)
    quantity = StringField(max_length=200, required=True)
    rate = FloatField(required=True)
    cgst = FloatField(required=True)
    sgst = FloatField(required=True)
    igst = FloatField(required=True)


class PurchaseInvoice(DynamicDocument):
    vendorName = StringField(max_length=200, required=True)
    vendorAddress = StringField(max_length=200, required=True)
    vendorGstin = StringField(max_length=200, required=True)
    vendorStateCode = StringField(max_length=200, required=True)
    billNo = StringField(max_length=200, required=True)
    billDate = DateTimeField(required=True)
    dueDate = DateTimeField(required=True)
    payBy = StringField(max_length=200, required=True)
    total = FloatField()
    tax = FloatField(required=True)
    amountPaid = FloatField(required=True)
    remarks = StringField(max_length=200, required=True)
    cancelReason = StringField(max_length=200, required=False)

class PurchasedProducts(DynamicDocument):
    billNo = ReferenceField('PurchaseInvoice', reverse_delete_rule=CASCADE)
    itemCode = StringField(max_length=100, required=True)
    particular = StringField(max_length=200, required=True)
    hsnCode = StringField(max_length=200, required=True)
    quantity = StringField(max_length=200, required=True)
    rate = FloatField(required=True)
    cgst = FloatField(required=True)
    sgst = FloatField(required=True)
    igst = FloatField(required=True)


class SalesInvoice(DynamicDocument):
    customerName = StringField(max_length=200, required=True)
    customerAddress = StringField(max_length=200, required=True)
    customerGstin = StringField(max_length=200, required=True)
    customerStateCode = IntField(required=True)
    paidBy = StringField(max_length=200, required=True)
    billNo = StringField(max_length=200, required=True)
    billDate = DateTimeField(required=True)
    poNo = StringField(max_length=200, required=True)
    poDate = StringField(max_length=200, required=True)
    vendorCode = StringField(max_length=200, required=True)
    paymentTerms = StringField(max_length=200, required=True)
    dcCode = StringField(max_length=200, required=True)
    dcDate = StringField(max_length=200, required=True)
    vehicleNo = StringField(max_length=200, required=True)
    dispatchedThrough = StringField(max_length=200, required=True)
    amount = FloatField(required=True)
    total = FloatField(required=True)
    amountPaid = FloatField(required=True)
    remarks = StringField(max_length=200, required=True)
    type = StringField(max_length=50, required=True)
    cancelReason = StringField(max_length=200, required=False)

class SalesProducts(DynamicDocument):
    billNo = ReferenceField('SalesInvoice', reverse_delete_rule=CASCADE)
    itemCode = StringField(max_length=50, required=True)
    particular = StringField(max_length=200, required=True)
    hsnCode = StringField(max_length=200, required=True)
    quantity = StringField(max_length=200, required=True)
    rate = FloatField(required=True)
    cgst = FloatField(required=True)
    sgst = FloatField(required=True)
    igst = FloatField(required=True)
    type = StringField(max_length=100, required=True)