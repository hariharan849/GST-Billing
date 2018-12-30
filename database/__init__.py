try:
    from mongodatabase import (
        Voucher, CompanyItems, CustomerNames,
        QuotationItems, QuotationDetails, PurchaseOrder, PurchaseOrderProducts,
        PurchaseInvoice, PurchasedProducts, SalesInvoice, SalesProducts)

    from mongodbManager import (
        VoucherManager, CustomerManager, CompanyItemManager,
        PurchaseOrderManager, QuotationManager, PurchaseManager, SalesManager)
except:
    from database import (
        Voucher, CompanyItems, CustomerNames,
        QuotationItems, QuotationDetails, PurchaseOrder, PurchaseOrderProducts,
        PurchaseInvoice, PurchasedProducts, SalesInvoice, SalesProducts)

    from dbManager import (
        VoucherManager, CustomerManager, CompanyItemManager,
        PurchaseOrderManager, QuotationManager, PurchaseManager, SalesManager)