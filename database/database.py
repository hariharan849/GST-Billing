from peewee import SqliteDatabase, Model, TextField, DateField, FloatField, ForeignKeyField, IntegerField

db = SqliteDatabase('lokri.db')


class Voucher(Model):
    voucherNo = TextField()
    customerName = TextField()
    voucherDate = DateField()
    remarks = TextField()
    paymentType = TextField()
    chequeNo = TextField()
    amount = TextField()
    type = TextField()
    cancelReason = TextField()
    class Meta:
        database = db

class CompanyItems(Model):
    itemCode = TextField()
    itemName = TextField()
    hsnCode = TextField()
    quantity = TextField()
    itemPrice = FloatField()
    type = TextField()
    class Meta:
        database = db

class CustomerNames(Model):
    custCode = TextField()
    custName = TextField()
    custAddress = TextField()
    gstin = TextField()
    stateCode = IntegerField()
    contactNo = IntegerField()
    class Meta:
        database = db

class InvoiceDatabase(Model):
    customerName = TextField()
    customerAddress = TextField()
    customerGstin = TextField()
    stateCode = IntegerField()
    paidBy = TextField()
    billNo = TextField()
    billDate = DateField()
    poNo = TextField()
    poDate = TextField()
    vendorCode = TextField()
    paymentTerms = TextField()
    dcCode = TextField()
    dcDate = TextField()
    vehicleNo = TextField()
    dispatchedThrough = TextField()
    amount = FloatField()
    total = FloatField()
    amountPaid = FloatField()
    remarks = TextField()
    class Meta:
        database = db

class ParticularMapping(Model):
    billNo = ForeignKeyField(InvoiceDatabase, to_field="billNo")
    particular = TextField()
    hsnCode = TextField()
    quantity = TextField()
    rate = FloatField()
    cgst = FloatField()
    sgst = FloatField()
    igst = FloatField()
    class Meta:
        database = db

class QuotationDetails(Model):
    customerName = TextField()
    customerAddress = TextField()
    quotationNo = IntegerField()
    quotationValidity = DateField()
    quotationDate = DateField()
    estAmount = FloatField()
    estTotal = FloatField()
    remarks = TextField()
    cancelReason = TextField()
    class Meta:
        database = db

class QuotationItems(Model):
    quotationNo = ForeignKeyField(QuotationDetails, to_field="quotationNo")
    itemCode = TextField()
    particular = TextField()
    hsnCode = TextField()
    quantity = TextField()
    rate = FloatField()
    cgst = FloatField()
    sgst = FloatField()
    igst = FloatField()
    class Meta:
        database = db

class PurchaseOrder(Model):
    customerName = TextField()
    poNo = IntegerField()
    poDate = DateField()
    remarks = TextField()
    cancelReason = TextField()
    class Meta:
        database = db

class PurchaseOrderProducts(Model):
    poNo = ForeignKeyField(PurchaseOrder, to_field="poNo")
    itemCode = TextField()
    particular = TextField()
    hsnCode = TextField()
    quantity = TextField()
    class Meta:
        database = db

class SalesInvoice(Model):
    customerName = TextField()
    customerAddress = TextField()
    customerGstin = TextField()
    customerStateCode = IntegerField()
    paidBy = TextField()
    billNo = TextField()
    billDate = DateField()
    poNo = TextField()
    poDate = TextField()
    vendorCode = TextField()
    paymentTerms = TextField()
    dcCode = TextField()
    dcDate = TextField()
    vehicleNo = TextField()
    dispatchedThrough = TextField()
    amount = FloatField()
    total = FloatField()
    amountPaid = FloatField()
    remarks = TextField()
    type = TextField()
    cancelReason = TextField()
    class Meta:
        database = db

class SalesProducts(Model):
    billNo = ForeignKeyField(InvoiceDatabase, to_field="billNo")
    itemCode = TextField()
    particular = TextField()
    hsnCode = TextField()
    quantity = TextField()
    rate = FloatField()
    cgst = FloatField()
    sgst = FloatField()
    igst = FloatField()
    type = TextField()
    class Meta:
        database = db

class PurchaseInvoice(Model):
    vendorName = TextField()
    vendorAddress = TextField()
    vendorGstin = TextField()
    vendorStateCode = TextField()
    billNo = TextField()
    billDate = DateField()
    dueDate = DateField()
    payBy = TextField()
    total = FloatField()
    tax = FloatField()
    amountPaid = FloatField()
    remarks = TextField()
    cancelReason = TextField()
    class Meta:
        database = db

class PurchasedProducts(Model):
    billNo = ForeignKeyField(PurchaseInvoice, to_field="billNo")
    itemCode = TextField()
    particular = TextField()
    hsnCode = TextField()
    quantity = TextField()
    rate = FloatField()
    cgst = FloatField()
    sgst = FloatField()
    igst = FloatField()

    class Meta:
        database = db


try:
    db.create_tables([SalesInvoice])
except:
    pass


try:
    db.create_tables([SalesProducts])
except:
    pass

try:
    db.create_tables([PurchasedProducts])
except:
    pass

try:
    db.create_tables([PurchaseInvoice])
except:
    pass

try:
    db.create_tables([PurchaseOrderProducts])
except:
    pass

try:
    db.create_tables([PurchaseOrder])
except:
    pass


try:
    db.create_tables([QuotationDetails])
except:
    pass


try:
    db.create_tables([QuotationItems])
except:
    pass

try:
    db.create_tables([Voucher])
except:
    pass

try:
    db.create_tables([ParticularMapping])
except:
    pass

try:
    db.create_tables([CompanyItems])
except:
    pass

try:
    db.create_tables([CustomerNames])
except:
    pass

try:
    db.create_tables([InvoiceDatabase])
except:
    pass
