import database as _database
# from mongoengine.queryset.visitor import Q

class QuotationManager(object):
    '''
    Manager class for QuotationManager Database
    '''
    def __init__(self):
        super(QuotationManager, self).__init__()

    @staticmethod
    def getQuotationItemInfo(quotationNo):
        # quotationInfo = QuotationManager.getQuotationDetailsInfo(quotationNo)
        return _database.QuotationItems.select().join(_database.QuotationDetails).where(
            _database.QuotationItems.quotationNo == quotationNo)

    @staticmethod
    def saveQuotationItemInfo(quotationNo, itemCode, particular, hsnCode, quantity, rate, cgst, sgst, igst):
        quotationItem = _database.QuotationItems.create(
            quotationNo=QuotationManager.getQuotationDetailsInfo(quotationNo),
            itemCode=itemCode,
            particular=particular,
            hsnCode=hsnCode,
            quantity=quantity,
            rate=rate,
            cgst=cgst,
            sgst=sgst,
            igst=igst
        )
        quotationItem.save()

    @staticmethod
    def getOrderedQuotationNoInfo():
        return _database.QuotationDetails.select().order_by(_database.QuotationDetails.quotationNo.desc()).get()

    @staticmethod
    def saveQuotationInfo(customerName, customerAddress , quotationNo, quotationValidity, quotationDate, estAmount, estTotal, remarks):
        '''
        Saves the Quotation information to the database
        '''
        quotation = _database.QuotationDetails.create(
            customerName=customerName,
            customerAddress=customerAddress ,
            quotationNo=quotationNo,
            quotationValidity=quotationValidity,
            quotationDate=quotationDate,
            estAmount=estAmount,
            estTotal=estTotal,
            remarks=remarks,
            cancelReason=''
        )
        quotation.save()

    @staticmethod
    def fetchAllQuotationInfo():
        '''
        Returns all Quotation information from the database
        '''
        return _database.QuotationDetails.select()

    @staticmethod
    def getQuotationDetailsInfo(quotationNo):
        '''
        Returns the PO information from the database for the passed poNo
        '''
        return _database.QuotationDetails.select().where(
            _database.QuotationDetails.quotationNo == quotationNo)[0]

    @staticmethod
    def deleteQuotationDetailsInfo(quotationNo=None):
        '''
        Deletes the voucher information to the database
        '''
        if quotationNo:
            quotationInfo = QuotationManager.getQuotationDetailsInfo(quotationNo)
            quotationInfo.delete_instance()
            return
        for quotationInfo in QuotationManager.fetchAllQuotationInfo():
            quotationInfo.delete_instance()

class SalesManager(object):
    '''
    Manager class for PurchaseManager Database
    '''
    def __init__(self, type):
        super(SalesManager, self).__init__()
        self._type = type

    def getOrderedSalesNoInfo(self):
        return _database.SalesInvoice.select().where(_database.SalesInvoice.type==self._type).order_by(_database.SalesInvoice.billNo.desc())[0].get()

    def getItemInfo(self, billNo, type=None):
        type = type or self._type
        return _database.SalesProducts.select().where(
            (_database.SalesProducts.billNo == billNo) &
            (_database.SalesProducts.type == type))

    def fetchAllItemInfo(self):
        return _database.SalesProducts.select().where(
            (_database.SalesProducts.type == type))

    def getItemInfoByCode(self, itemCode):
        return _database.SalesProducts.select().where(
            (_database.PurchasedProducts.itemCode == itemCode) &
            (_database.SalesProducts.type == type))

    def saveSalesItemInfo(self, billNo, itemCode, particular, hsnCode, quantity, rate, cgst, sgst, igst):
        quotationItem = _database.SalesProducts.create(
            billNo=billNo,
            itemCode=itemCode,
            particular=particular,
            hsnCode=hsnCode,
            quantity=quantity,
            rate=rate,
            cgst=cgst,
            sgst=sgst,
            igst=igst,
            type=self._type
        )
        quotationItem.save()

    def saveSalesInfo(self, customerName, customerAddress, customerGstin, customerStateCode, paidBy, billNo,
                      billDate, poNo, poDate, vendorCode, paymentTerms, dcCode, dcDate, vehicleNo,
                      dispatchedThrough, amount, total, amountPaid, remarks, cancelReason):
        '''
        Saves the Purchase information to the database
        '''
        sales = _database.SalesInvoice.create(
            customerName=customerName,
            customerAddress=customerAddress,
            customerGstin=customerGstin,
            customerStateCode=customerStateCode,
            paidBy=paidBy,
            billNo=billNo,
            billDate=billDate,
            poNo=poNo,
            poDate=poDate,
            vendorCode=vendorCode,
            paymentTerms=paymentTerms,
            dcCode=dcCode,
            dcDate=dcDate,
            vehicleNo=vehicleNo,
            dispatchedThrough=dispatchedThrough,
            amount=amount,
            total=total,
            amountPaid=amountPaid,
            remarks=remarks,
            type=self._type,
            cancelReason=cancelReason
        )
        sales.save()

    def fetchAllSalesInfo(self):
        '''
        Returns all Sales information from the database
        '''
        return _database.SalesInvoice.select().where(_database.SalesInvoice.type == self._type)

    def fetchInfoWithinDate(self, fromDate, toDate):
        '''
        Returns all Sales information within date from the database
        '''
        return _database.SalesInvoice.select().where(
            (_database.SalesInvoice.billDate >= fromDate) and
            (_database.SalesInvoice.billDate <= toDate) and
            (_database.SalesInvoice.type == self._type))

    def getSalesInfo(self, billNo, type=None):
        '''
        Returns the Sales information from the database for the passed poNo
        '''
        type = type or self._type
        try:
            return _database.SalesInvoice.select().where(
                (_database.SalesInvoice.billNo == billNo) &
                (_database.SalesInvoice.type==type))[0]
        except:
            return []

    def deleteSalesInfo(self, billNo=None):
        '''
        Deletes the Purchase information to the database
        '''
        if billNo:
            salesInfo = self.getSalesInfo(billNo)
            salesInfo.delete_instance()
            return
        for salesInfo in self.fetchAllSalesInfo():
            salesInfo.delete_instance()

class PurchaseManager(object):
    '''
    Manager class for PurchaseManager Database
    '''
    def __init__(self):
        super(PurchaseManager, self).__init__()

    @staticmethod
    def getOrderedPurchaseNoInfo():
        # QuotationDetails.select().order_by(QuotationDetails.quotationNo.desc()).get()
        return _database.PurchaseInvoice.select().order_by(_database.PurchaseInvoice.billNo.desc()).get()

    @staticmethod
    def getItemInfo(purchaseNo):
        return _database.PurchasedProducts.select().where(
            (_database.PurchasedProducts.billNo == purchaseNo))

    @staticmethod
    def fetchAllItemInfo():
        return _database.PurchasedProducts.select()

    @staticmethod
    def getItemInfoByCode(itemCode):
        return _database.PurchasedProducts.select().where(
            (_database.PurchasedProducts.itemCode == itemCode))

    @staticmethod
    def savePurchaseItemInfo(quotationNo, itemCode, particular, hsnCode, quantity, rate, cgst, sgst, igst):
        purchaseItem = _database.PurchasedProducts.create(
            billNo=quotationNo,
            itemCode=itemCode,
            particular=particular,
            hsnCode=hsnCode,
            quantity=quantity,
            rate=float(rate),
            cgst=float(cgst),
            sgst=float(sgst),
            igst=float(igst)
        )
        purchaseItem.save()

    @staticmethod
    def savePurchaseInfo(vendorName, vendorAddress, vendorGstin, vendorStateCode,
                         billNo, billDate, dueDate, payBy, total, tax, amountPaid, remarks):
        '''
        Saves the Purchase information to the database
        '''
        purchase = _database.PurchaseInvoice.create(
            vendorName=vendorName,
            vendorAddress=vendorAddress,
            vendorGstin=vendorGstin,
            vendorStateCode=vendorStateCode,
            billNo=billNo,
            billDate=billDate,
            dueDate=dueDate,
            payBy=payBy,
            total=float(total),
            tax=float(tax),
            amountPaid=float(amountPaid),
            remarks=remarks,
            cancelReason=''
        )
        purchase.save()

    @staticmethod
    def fetchAllPurchaseInfo():
        '''
        Returns all Purchase information from the database
        '''
        return _database.PurchaseInvoice.select()

    @staticmethod
    def fetchInfoWithinDate(self, fromDate, toDate):
        '''
        Returns all Sales information within date from the database
        '''
        return _database.PurchaseInvoice.select().where(
            (_database.PurchaseInvoice.billDate >= fromDate) and
            (_database.PurchaseInvoice.billDate <= toDate))


    @staticmethod
    def getPurchaseDetailsInfo(purchaseNo):
        '''
        Returns the Purchase information from the database for the passed poNo
        '''
        return _database.PurchaseInvoice.select().where(
            (_database.PurchaseInvoice.billNo == purchaseNo))[0]

    @staticmethod
    def deletePurchaseDetailsInfo(purchaseNo=None):
        '''
        Deletes the Purchase information to the database
        '''
        if purchaseNo:
            purchaseInfo = PurchaseManager.getPurchaseDetailsInfo(purchaseNo)
            purchaseInfo.delete_instance()
            return
        for purchaseInfo in PurchaseManager.fetchAllPurchaseInfo():
            purchaseInfo.delete_instance()

class PurchaseOrderManager(object):
    '''
    Manager class for Companyitem Database
    '''
    def __init__(self):
        super(PurchaseOrderManager, self).__init__()

    @staticmethod
    def savePurchaseOrderProduct(poNo, itemCode, particulars, hsnCode, quantity):
        poItem = _database.PurchaseOrderProducts.create(
            poNo=poNo,
            itemCode=itemCode,
            particular=particulars,
            hsnCode=hsnCode,
            quantity=quantity
        )
        poItem.save()

    @staticmethod
    def savePOInfo(custName, poNo, poDate, remarks):
        '''
        Saves the PurchaseOrder information to the database
        '''
        po = _database.PurchaseOrder.create(
            customerName=custName,
            poNo=int(poNo),
            poDate=poDate,
            remarks=remarks,
            cancelReason=''
        )
        po.save()

    @staticmethod
    def fetchAllPOInfo():
        '''
        Returns all PO information from the database
        '''
        return _database.PurchaseOrder.select()

    def fetchAllpoNo(self):
        return [poInfo.poNo for poInfo in _database.PurchaseOrder.select()]

    @staticmethod
    def getPOInfo(poNo):
        '''
        Returns the PO information from the database for the passed poNo
        '''
        return _database.PurchaseOrder.select().where(
            (_database.PurchaseOrder.poNo == poNo))[0]

    @staticmethod
    def deletePOInfo(poNo=None):
        '''
        Deletes the voucher information to the database
        '''
        if poNo:
            poInfo = PurchaseOrderManager.getPOInfo(poNo)
            poInfo.delete_instance()
            return
        for poInfo in PurchaseOrderManager.fetchAllPOInfo():
            poInfo.delete_instance()

    def getPurchaseOrderItemInfo(self, poNo):
        return _database.PurchaseOrderProducts.select().where(
            (_database.PurchaseOrder.poNo==poNo))

class CompanyItemManager(object):
    '''
    Manager class for Companyitem Database
    '''
    def __init__(self, type):
        super(CompanyItemManager, self).__init__()
        self._type = type

    def fetchAllItemCodes(self):
        return [companyItem.itemCode for companyItem in _database.CompanyItems.select().where(_database.CompanyItems.type==self._type)]

    def saveCompanyItemInfo(self, itemCode, itemName, hsnCode, quantity, itemPrice):
        '''
        Saves the voucher information to the database
        '''
        customer = _database.CompanyItems.create(
            itemCode=itemCode,
            itemName=itemName,
            hsnCode=hsnCode,
            quantity=quantity,
            itemPrice=itemPrice,
            type=self._type
        )
        customer.save()

    def fetchAllCompanyItemInfo(self):
        '''
        Returns all company information from the database
        '''
        return _database.CompanyItems.select().where(_database.CompanyItems.type==self._type)

    def getCompanyItemInfo(self, itemCode):
        '''
        Returns the company information from the database for the passed itemCode
        '''
        return _database.CompanyItems.select().where(
            (_database.CompanyItems.itemCode == itemCode) &
            (_database.CompanyItems.type == self._type))[0]

    def deleteCompanyItemInfo(self, itemCode=None):
        '''
        Deletes the voucher information to the database
        '''
        if itemCode:
            companyItemInfo = self.getCompanyItemInfo(itemCode)
            companyItemInfo.delete_instance()
            return
        for companyItemInfo in self.fetchAllCompanyItemInfo():
            companyItemInfo.delete_instance()

class CustomerManager(object):
    '''
    Manager class for Customer Database
    '''
    def __init__(self):
        super(CustomerManager, self).__init__()

    @staticmethod
    def saveCustomerInfo(custCode, custName, custAddress, gstin, stateCode, contactNo):
        '''
        Saves the voucher information to the database
        '''
        customer = _database.CustomerNames.create(
            custCode=custCode,
            custName=custName,
            custAddress=custAddress,
            gstin=gstin,
            stateCode=stateCode,
            contactNo=contactNo
        )
        customer.save()

    def fetchAllItemCodes(self):
        return [customerInfo.custCode for customerInfo in _database.CustomerNames.select()]

    @staticmethod
    def fetchAllCustomerInfo():
        '''
        Returns all customer information from the database
        '''
        return _database.CustomerNames.select()

    @staticmethod
    def getCustomerInfo(custCode):
        '''
        Returns the customer information from the database for the passed gstinNo
        '''
        return _database.CustomerNames.select().where(
            _database.CustomerNames.custCode == custCode)[0]

    @staticmethod
    def deleteCustomerInfo(custCode=None):
        '''
        Deletes the voucher information to the database
        '''
        if custCode:
            customerInfo = CustomerManager.getCustomerInfo(custCode)
            customerInfo.delete_instance()
            return
        for customerInfo in CustomerManager.fetchAllCustomerInfo():
            customerInfo.delete_instance()

class VoucherManager(object):
    '''
    Manager class for Voucher Database
    '''
    def __init__(self, type):
        super(VoucherManager, self).__init__()
        self._type = type

    def saveVoucherInfo(self, voucherNo, customerName, voucherDate, remarks, paymentType, chequeNo, amount, cancelReason):
        '''
        Saves the voucher information to the database
        '''
        voucher = _database.Voucher.create(
            voucherNo=str(voucherNo),
            customerName=customerName,
            voucherDate=voucherDate,
            remarks=str(remarks),
            paymentType=str(paymentType),
            chequeNo=str(chequeNo if chequeNo.lower() != 'nan' else ''),
            amount=str(amount),
            type=self._type,
            cancelReason=str(cancelReason)
        )
        voucher.save()

    def fetchAllVoucherInfo(self):
        '''
        Returns all voucher information to the database
        '''
        return _database.Voucher.select().where(_database.Voucher.type==self._type)

    def fetchAllVoucherNo(self):
        '''
        Returns all voucher information to the database
        '''
        return [voucherInfo.voucherNo for voucherInfo in _database.Voucher.select().where(_database.Voucher.type==self._type)]


    def getVoucherInfo(self, voucherNo):
        '''
        Returns the voucher information from the database for the passed voucherNo
        '''
        return _database.Voucher.select().where((_database.Voucher.type==self._type) and (_database.Voucher.voucherNo == voucherNo))[0]

    def deleteVoucherInfo(self, voucherNo=None):
        '''
        Deletes the voucher information to the database
        '''
        if voucherNo:
            voucherInfo = self.getVoucherInfo(voucherNo)
            voucherInfo.delete_instance()
            return
        for voucherInfo in self.fetchAllVoucherInfo():
            voucherInfo.delete_instance()