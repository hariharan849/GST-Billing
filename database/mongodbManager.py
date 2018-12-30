import mongodatabase as _database
from mongoengine.queryset.visitor import Q

class QuotationManager(object):
    '''
    Manager class for QuotationManager Database
    '''
    def __init__(self):
        super(QuotationManager, self).__init__()

    @staticmethod
    def getQuotationItemInfo(quotationNo):
        quotationInfo = QuotationManager.getQuotationDetailsInfo(quotationNo)
        return _database.QuotationItems.objects(
            Q(quotationNo=quotationInfo))

    @staticmethod
    def saveQuotationItemInfo(quotationNo, itemCode, particular, hsnCode, quantity, rate, cgst, sgst, igst):
        quotationItem = _database.QuotationItems(
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
        return _database.QuotationDetails.objects.order_by('-quotationNo')[0].quotationNo

    @staticmethod
    def saveQuotationInfo(customerName, customerAddress , quotationNo, quotationValidity, quotationDate, estAmount, estTotal, remarks):
        '''
        Saves the Quotation information to the database
        '''
        quotation = _database.QuotationDetails(
            customerName=customerName,
            customerAddress=customerAddress ,
            quotationNo=quotationNo,
            quotationValidity=quotationValidity,
            quotationDate=quotationDate,
            estAmount=estAmount,
            estTotal=estTotal,
            remarks=remarks
        )
        quotation.save()

    @staticmethod
    def fetchAllQuotationInfo():
        '''
        Returns all Quotation information from the database
        '''
        return _database.QuotationDetails.objects

    @staticmethod
    def getQuotationDetailsInfo(quotationNo):
        '''
        Returns the PO information from the database for the passed poNo
        '''
        return _database.QuotationDetails.objects(
            Q(quotationNo = quotationNo))[0]

    @staticmethod
    def deleteQuotationDetailsInfo(quotationNo=None):
        '''
        Deletes the voucher information to the database
        '''
        if quotationNo:
            quotationInfo = QuotationManager.getQuotationDetailsInfo(quotationNo)
            quotationInfo.delete()
            return
        for quotationInfo in QuotationManager.fetchAllQuotationInfo():
            quotationInfo.delete()

class SalesManager(object):
    '''
    Manager class for PurchaseManager Database
    '''
    def __init__(self, type):
        super(SalesManager, self).__init__()
        self._type = type

    def getOrderedSalesNoInfo(self):
        return _database.SalesInvoice.objects(type=self._type).order_by('-billNo')[0].billNo

    def getItemInfo(self, billNo, type=None):
        salesInfo = self.getSalesInfo(billNo, type)
        type = type or self._type
        return _database.SalesProducts.objects(
            Q(billNo=salesInfo) &
            Q(type=type))

    def fetchAllItemInfo(self):
        return _database.SalesProducts.objects(Q(type=type))

    def getItemInfoByCode(self, itemCode):

        return _database.SalesProducts.objects(Q(type=type) &
                                               Q(itemCode=itemCode))

    def saveSalesItemInfo(self, billNo, itemCode, particular, hsnCode, quantity, rate, cgst, sgst, igst):
        quotationItem = _database.SalesProducts(
            billNo=self.getSalesInfo(billNo),
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
                      dispatchedThrough, amount, total, amountPaid, remarks):
        '''
        Saves the Purchase information to the database
        '''
        sales = _database.SalesInvoice(
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
            type=self._type
        )
        sales.save()

    def fetchAllSalesInfo(self):
        '''
        Returns all Sales information from the database
        '''
        return _database.SalesInvoice.objects(type=self._type)

    def getSalesInfo(self, billNo, type=None):
        '''
        Returns the Sales information from the database for the passed poNo
        '''
        type = type or self._type
        return _database.SalesInvoice.objects(
            Q(billNo = billNo) &
            Q(type=type))[0]

    def deleteSalesInfo(self, billNo=None):
        '''
        Deletes the Purchase information to the database
        '''
        if billNo:
            salesInfo = self.getSalesInfo(billNo)
            salesInfo.delete()
            return
        for salesInfo in self.fetchAllSalesInfo():
            salesInfo.delete()

class PurchaseManager(object):
    '''
    Manager class for PurchaseManager Database
    '''
    def __init__(self):
        super(PurchaseManager, self).__init__()

    @staticmethod
    def getOrderedPurchaseNoInfo():
        return _database.PurchaseInvoice.objects.order_by('-billNo')[0].billNo

    @staticmethod
    def getItemInfo(purchaseNo):
        purchaseInfo = PurchaseManager.getPurchaseDetailsInfo(purchaseNo)
        return _database.PurchasedProducts.objects(
            Q(billNo=purchaseInfo))

    @staticmethod
    def fetchAllItemInfo():
        return _database.PurchasedProducts.objects

    @staticmethod
    def getItemInfoByCode(itemCode):
        return _database.PurchasedProducts.objects(
            Q(itemCode=itemCode))

    @staticmethod
    def savePurchaseItemInfo(quotationNo, itemCode, particular, hsnCode, quantity, rate, cgst, sgst, igst):
        purchaseItem = _database.PurchasedProducts(
            billNo=PurchaseManager.getPurchaseDetailsInfo(quotationNo),
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
        purchase = _database.PurchaseInvoice(
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
            remarks=remarks
        )
        purchase.save()

    @staticmethod
    def fetchAllPurchaseInfo():
        '''
        Returns all Purchase information from the database
        '''
        return _database.PurchaseInvoice.objects

    @staticmethod
    def getPurchaseDetailsInfo(purchaseNo):
        '''
        Returns the Purchase information from the database for the passed poNo
        '''
        return _database.PurchaseInvoice.objects(
            Q(billNo = purchaseNo))[0]

    @staticmethod
    def deletePurchaseDetailsInfo(purchaseNo=None):
        '''
        Deletes the Purchase information to the database
        '''
        if purchaseNo:
            purchaseInfo = PurchaseManager.getPurchaseDetailsInfo(purchaseNo)
            purchaseInfo.delete()
            return
        for purchaseInfo in PurchaseManager.fetchAllPurchaseInfo():
            purchaseInfo.delete()

class PurchaseOrderManager(object):
    '''
    Manager class for Companyitem Database
    '''
    def __init__(self):
        super(PurchaseOrderManager, self).__init__()

    @staticmethod
    def savePurchaseOrderProduct(poNo, itemCode, particulars, hsnCode, quantity):
        poItem = _database.PurchaseOrderProducts(
            PurchaseOrderManager.getPOInfo(poNo),
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
        po = _database.PurchaseOrder(
            customerName=custName,
            poNo=poNo,
            poDate=poDate,
            remarks=remarks
        )
        po.save()

    @staticmethod
    def fetchAllPOInfo():
        '''
        Returns all PO information from the database
        '''
        return _database.PurchaseOrder.objects

    def fetchAllpoNo(self):
        return [poInfo.poNo for poInfo in _database.PurchaseOrder.objects]

    @staticmethod
    def getPOInfo(poNo):
        '''
        Returns the PO information from the database for the passed poNo
        '''
        return _database.PurchaseOrder.objects(
            Q(poNo = poNo))[0]

    @staticmethod
    def deletePOInfo(poNo=None):
        '''
        Deletes the voucher information to the database
        '''
        if poNo:
            poInfo = PurchaseOrderManager.getPOInfo(poNo)
            poInfo.delete()
            return
        for poInfo in PurchaseOrderManager.fetchAllPOInfo():
            poInfo.delete()

    def getPurchaseOrderItemInfo(self, poNo):
        poInfo = PurchaseOrderManager.getPOInfo(poNo)
        return _database.PurchaseOrderProducts.objects(
            Q(poNo=poInfo))

class CompanyItemManager(object):
    '''
    Manager class for Companyitem Database
    '''
    def __init__(self, type):
        super(CompanyItemManager, self).__init__()
        self._type = type

    def fetchAllItemCodes(self):
        return [companyItem.itemCode for companyItem in _database.CompanyItems.objects(type=self._type)]

    def saveCompanyItemInfo(self, itemCode, itemName, hsnCode, quantity, itemPrice):
        '''
        Saves the voucher information to the database
        '''
        customer = _database.CompanyItems(
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
        return _database.CompanyItems.objects(type=self._type)

    def getCompanyItemInfo(self, itemCode):
        '''
        Returns the company information from the database for the passed itemCode
        '''
        return _database.CompanyItems.objects(
            Q(itemCode = itemCode) &
            Q(type=self._type))[0]

    def deleteCompanyItemInfo(self, itemCode=None):
        '''
        Deletes the voucher information to the database
        '''
        if itemCode:
            companyItemInfo = self.getCompanyItemInfo(itemCode)
            companyItemInfo.delete()
            return
        for companyItemInfo in self.fetchAllCompanyItemInfo():
            companyItemInfo.delete()

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
        customer = _database.CustomerNames(
            custCode=custCode,
            custName=custName,
            custAddress=custAddress,
            gstin=gstin,
            stateCode=stateCode,
            contactNo=contactNo
        )
        customer.save()

    def fetchAllItemCodes(self):
        return [customerInfo.custCode for customerInfo in _database.CustomerNames.objects]

    @staticmethod
    def fetchAllCustomerInfo():
        '''
        Returns all customer information from the database
        '''
        return _database.CustomerNames.objects

    @staticmethod
    def getCustomerInfo(custCode):
        '''
        Returns the customer information from the database for the passed gstinNo
        '''
        return _database.CustomerNames.objects(
            Q(custCode = custCode))[0]

    @staticmethod
    def deleteCustomerInfo(custCode=None):
        '''
        Deletes the voucher information to the database
        '''
        if custCode:
            customerInfo = CustomerManager.getCustomerInfo(custCode)
            customerInfo.delete()
            return
        for customerInfo in CustomerManager.fetchAllCustomerInfo():
            customerInfo.delete()

class VoucherManager(object):
    '''
    Manager class for Voucher Database
    '''
    def __init__(self, type):
        super(VoucherManager, self).__init__()
        self._type = type

    def saveVoucherInfo(self, voucherNo, customerName, voucherDate, remarks, paymentType, chequeNo, amount):
        '''
        Saves the voucher information to the database
        '''
        voucher = _database.Voucher(
            voucherNo=str(voucherNo),
            customerName=customerName,
            voucherDate=voucherDate,
            remarks=str(remarks),
            paymentType=str(paymentType),
            chequeNo=str(chequeNo if chequeNo.lower() != 'nan' else ''),
            amount=str(amount),
            type=self._type
        )
        voucher.save()

    def fetchAllVoucherInfo(self):
        '''
        Returns all voucher information to the database
        '''
        return _database.Voucher.objects(type=self._type)

    def fetchAllVoucherNo(self):
        '''
        Returns all voucher information to the database
        '''
        return [voucherInfo.voucherNo for voucherInfo in _database.Voucher.objects(type=self._type)]


    def getVoucherInfo(self, voucherNo):
        '''
        Returns the voucher information from the database for the passed voucherNo
        '''
        return _database.Voucher.objects(
            Q(voucherNo = voucherNo) &
            Q(type = self._type))[0]

    def deleteVoucherInfo(self, voucherNo=None):
        '''
        Deletes the voucher information to the database
        '''
        if voucherNo:
            voucherInfo = self.getVoucherInfo(voucherNo)
            voucherInfo.delete()
            return
        for voucherInfo in self.fetchAllVoucherInfo():
            voucherInfo.delete()