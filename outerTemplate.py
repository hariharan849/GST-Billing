from os.path import dirname, join
from json import load

filePath = join(dirname(dirname(__file__)), 'template.json')
print filePath
with open(filePath) as fileObj:
    lokriDict = load(fileObj)
    CUSTOMER_NAME = lokriDict['companyName']
    GSTIN = lokriDict['gstin']
    STATE_CODE = lokriDict['stateCode']
    STATE_NAME = lokriDict['stateName']
    ADDRESS1_ROW, ADDRESS1_COLUMN, ADDRESS1 = lokriDict['address1']
    ADDRESS2_ROW, ADDRESS2_COLUMN, ADDRESS2 = lokriDict['address2']
    DC_ROW, DC_COL = lokriDict['dcData']
    CUSTOMER_ROW, CUSTOMER_COL = lokriDict['companyData']
    COMPANY_TAG = lokriDict['companyTag']
    TAG_ROW, TAG_COL = lokriDict['tagData']
    BANK_CUSTOMER_NAME = lokriDict['bankCustomerName']
    BANK_BRANCH = lokriDict['bankBranchName']
    ACCOUNT_NO = lokriDict['accountNo']
    IFSC_CODE = lokriDict['ifscCode']
    BANK_FONT = lokriDict['bankFont']


def _createBillHeader(canvas, title):
    ''' Create bill header with customer details on top of PDF
    '''
    canvas.setFont('Helvetica-Bold', 25)
    canvas.drawString(int(CUSTOMER_ROW), int(CUSTOMER_COL), CUSTOMER_NAME)
    if COMPANY_TAG:
        canvas.setFont('Helvetica', 11)
        canvas.drawString(int(TAG_ROW) ,int(TAG_COL), COMPANY_TAG)
    canvas.setFont('Helvetica', 10)
    canvas.drawString(int(ADDRESS1_ROW), int(ADDRESS1_COLUMN), ADDRESS1)
    canvas.drawString(int(ADDRESS2_ROW), int(ADDRESS2_COLUMN), ADDRESS2)

    canvas.drawString(500, 780, title)
    canvas.setFont('Helvetica', 8)
    canvas.line(35, 770, 110, 770)
    canvas.line(35, 750, 110, 750)
    canvas.line(35, 750, 35, 770)
    canvas.line(110, 770, 110, 750)
    canvas.drawString(60, 761, 'GSTIN')
    canvas.drawString(36, 753, '{}'.format(GSTIN))

    canvas.line(297, 770, 360, 770)
    canvas.line(297, 758, 360, 758)
    canvas.line(297, 770, 297, 758)
    canvas.line(360, 770, 360, 758)
    canvas.drawString(300, 761, 'GST - INVOICE')

    canvas.line(470, 770, 570, 770)
    canvas.line(470, 750, 570, 750)
    canvas.line(470, 750, 470, 770)
    canvas.line(570, 770, 570, 750)
    canvas.drawString(500, 761, '{}'.format(STATE_NAME))
    canvas.drawString(490, 753, 'STATE CODE: {}'.format(STATE_CODE))

def _createDCHeader(canvas):
    ''' Creates Delivery challan template
    '''
    canvas.setFont('Helvetica-Bold', 25)
    canvas.drawString(int(DC_ROW), int(DC_COL), CUSTOMER_NAME.upper())

    canvas.setFont('Helvetica', 10)
    canvas.drawString(int(ADDRESS1_ROW), int(ADDRESS1_COLUMN), ADDRESS1)
    canvas.drawString(int(ADDRESS2_ROW), int(ADDRESS2_COLUMN), ADDRESS2)

    _createGstinStateCode(canvas)

    canvas.line(287, 758, 370, 758)
    canvas.line(287, 770, 370, 770)
    canvas.line(287, 770, 287, 758)
    canvas.line(370, 770, 370, 758)
    canvas.drawString(290, 761, 'Delivery Challan')

def _createGstinStateCode(canvas):
    ''' Creates Gstin and state code template
    '''
    canvas.setFont('Helvetica', 8)
    canvas.line(35, 770, 140, 770)
    canvas.line(35, 750, 140, 750)
    canvas.line(35, 750, 35, 770)
    canvas.line(140, 770, 140, 750)
    canvas.drawString(36, 761, 'GSTIN-{}'.format(GSTIN))
    canvas.drawString(36, 753, 'STATE CODE: {}'.format(STATE_CODE))

def _createQuotationBillHeader(canvas):
    ''' Create bill header with customer details on top of PDF
    '''

    canvas.setFont('Helvetica-Bold', 25)
    canvas.drawString(int(CUSTOMER_ROW), int(CUSTOMER_COL), CUSTOMER_NAME)
    canvas.setFont('Helvetica', 10)
    canvas.drawString(int(ADDRESS1_ROW), int(ADDRESS1_COLUMN), ADDRESS1)
    canvas.drawString(int(ADDRESS2_ROW), int(ADDRESS2_COLUMN), ADDRESS2)

    canvas.drawString(500, 780, 'quotation')
    _createGstinStateCode(canvas)

    canvas.drawString(40, 175, 'Remarks')

    canvas.line(297, 770, 340, 770)
    canvas.line(297, 758, 340, 758)
    canvas.line(297, 770, 297, 758)
    canvas.line(340, 770, 340, 758)
    canvas.drawString(300, 761, 'Quotation')

def _createBillInfoTemplate(canvas):
    ''' Creates template for bill information
    '''
    _createCustomerInfoTemplate(canvas)
    canvas.drawString(305 ,672 ,'Bill NO.')
    canvas.drawString(450 ,672 ,'Date')
    canvas.line(53 ,663 ,300 ,663)
    canvas.drawString(305 ,656 ,'PO No.')
    canvas.drawString(450 ,656 ,'Date')
    canvas.line(30 ,641 ,300 ,641)
    canvas.drawString(305 ,640 ,'Vendor Code')
    canvas.drawString(430 ,640 ,'Payment Terms')
    canvas.line(30, 619, 300, 619)
    canvas.drawString(305 ,624 ,'DC No.')
    canvas.drawString(450 ,624 ,'Date')
    canvas.line(30, 597, 580, 597)
    canvas.drawString(305 ,607 ,'Vehicle No.')
    canvas.drawString(425 ,611 ,'Dispatched')
    canvas.drawString(425, 603, 'Through')

def _createDCInfoTemplate(canvas):
    ''' Creates template for DC information
    '''
    _createCustomerInfoTemplate(canvas)

    canvas.drawString(305, 672, 'DC NO.')
    canvas.drawString(450, 672, 'Date')
    canvas.line(53, 663, 300, 663)
    canvas.drawString(305, 651, 'PO No.')
    canvas.drawString(450, 651, 'Date')
    canvas.line(30, 641, 300, 641)
    canvas.drawString(305, 629, 'Vendor Code')
    canvas.drawString(430, 629, 'Payment Terms')

    canvas.line(30, 619, 300, 619)
    canvas.drawString(305, 607, 'Vehicle No.')
    canvas.drawString(425, 611, 'Dispatched')
    canvas.drawString(425, 603, 'Through')
    canvas.line(30, 597, 580, 597)

def _createCustomerInfoTemplate(canvas):
    '''Creates Customer Information template
    '''
    canvas.line(30, 685, 580, 685)
    canvas.setFont('Helvetica', 8.5)
    canvas.drawString(35, 675.5, 'TO,')
    canvas.drawString(35, 665, 'M/s')
    canvas.line(300, 685, 300, 597)

def _createQuotationInfoTemplate(canvas):
    '''Creates Quotation Information template
    '''
    _createCustomerInfoTemplate(canvas)
    canvas.drawString(305, 672, 'Quotation NO.')
    canvas.line(53, 663, 300, 663)
    canvas.drawString(305, 642, 'Quotation Date')
    canvas.line(30, 641, 300, 641)
    canvas.line(30, 619, 300, 619)
    canvas.drawString(305, 612, 'Valid Until')
    canvas.line(30, 597, 580, 597)

def _createTransportTemplate(canvas):
    ''' Creates template for transport information
    '''
    canvas.setFont('Helvetica-Bold', 8)
    canvas.drawString(35 ,581 ,'Customer GSTIN:')
    canvas.drawString(275 ,581 ,'State Code.')
    canvas.drawString(350, 581, 'E-way bill no.')
    canvas.line(30 ,575 ,580 ,575)

def _createTableTemplate(canvas):
    ''' Creates template for table in bill
    '''
    canvas.line(30 ,552 ,580 ,552)
    canvas.drawString(35 ,555 ,'SI No.')
    canvas.line(60, 190, 60, 575)
    canvas.drawString(195 ,555 ,'Particulars')
    canvas.line(320 ,190 ,320 ,575)
    canvas.drawString(340 ,562 ,'HSN')
    canvas.drawString(340 ,554 ,'Code')
    canvas.line(375 ,100 ,375 ,575)
    canvas.drawString(390 ,555 ,'Qty.')
    canvas.line(435 ,100 ,435 ,575)
    canvas.drawString(450 ,565 ,'Rate')
    canvas.line(476 ,100 ,476 ,552)
    canvas.drawString(445 ,554 ,'Rs.')
    canvas.drawString(480 ,554 ,'P.')
    canvas.line(500 ,100 ,500 ,575)
    canvas.drawString(520 ,565 ,'AMOUNT')
    canvas.line(560 ,100 ,560 ,552)
    canvas.drawString(522 ,554 ,'Rs.')
    canvas.drawString(566 ,554 ,'P.')

def _createDCTableInfo(canvas):
    ''' Creates Delivery Challan Table template
    '''
    canvas.line(30, 552, 580, 552)
    canvas.drawString(35, 555, 'SI No.')
    canvas.line(60, 95, 60, 575)
    canvas.drawString(75, 555, 'Material Code')
    canvas.line(140, 95, 140, 575)
    canvas.drawString(245, 555, 'Particulars')
    canvas.line(420, 120, 420, 575)
    canvas.drawString(450, 555, 'Quantity')
    canvas.line(500, 120, 500, 575)
    canvas.drawString(520, 555, 'Remarks')
    canvas.line(420, 120, 580, 120)
    canvas.setFont('Helvetica-Bold', 10)
    canvas.drawString(390, 110, 'Total')
    canvas.line(30, 95, 580, 95)

def _createQuotationTableInfo(canvas):
    ''' Creates Quoatation Table template
    '''
    canvas.setFont('Helvetica-Bold', 8)

    canvas.line(30, 575, 580, 575)
    canvas.line(60, 190, 60, 597)
    canvas.drawString(35, 580, 'SI No.')
    canvas.drawString(195, 580, 'Particulars')
    canvas.line(320, 190, 320, 597)
    canvas.drawString(340, 585, 'HSN')
    canvas.drawString(340, 577, 'Code')
    canvas.line(375, 100, 375, 597)
    canvas.drawString(390, 580, 'Qty.')
    canvas.line(435, 100, 435, 597)
    canvas.drawString(450, 585, 'Rate')
    canvas.line(476, 100, 476, 575)
    canvas.drawString(445, 577, 'Rs.')
    canvas.drawString(480, 577, 'P.')
    canvas.line(500, 100, 500, 597)
    canvas.drawString(520, 585, 'AMOUNT')
    canvas.line(560, 100, 560, 575)
    canvas.drawString(522, 577, 'Rs.')
    canvas.drawString(566, 577, 'P.')

    canvas.line(30, 190, 580, 190)
    canvas.line(225, 100, 225, 190)

    _createAmountTemplate(canvas)

def _createBankTemplate(canvas):
    ''' Creates bank template in bill
    '''
    canvas.setFont('Helvetica-Bold', int(BANK_FONT))
    canvas.drawString(40, 175, BANK_CUSTOMER_NAME)
    canvas.drawString(40, 155, BANK_BRANCH)
    canvas.drawString(40, 135, ACCOUNT_NO)
    canvas.drawString(40, 115, IFSC_CODE)
    canvas.line(30 ,190 ,580 ,190)
    canvas.line(225 ,100 ,225 ,190)

def _createAmountTemplate(canvas):
    ''' Create amount template in bill
    '''
    canvas.setFont('Helvetica', 8.5)
    canvas.drawString(250, 180, 'Total Amount Before Tax')
    canvas.line(375, 175, 580, 175)
    canvas.drawString(300, 165, 'Add: CGST')
    canvas.line(375, 160, 580, 160)
    canvas.drawString(300, 150, 'Add: SGST')
    canvas.line(375, 145, 580, 145)
    canvas.drawString(300, 135, 'Add: IGST')
    canvas.line(375, 130, 580, 130)
    canvas.drawString(300, 120, 'Round Off')
    canvas.line(375, 115, 580, 115)
    canvas.drawString(250, 105, 'Total Amount After Tax')
    canvas.line(30, 100, 580, 100)

def _createAuthorityTemplate(canvas):
    ''' Create authority template for bill
    '''
    canvas.setFont('Helvetica', 7.9)
    canvas.drawString(36, 86, 'Rupees')
    canvas.line(350 ,26 ,350 ,100)
    canvas.setFont('Helvetica', 7)
    canvas.drawString(365, 85, 'Certified that the particulars given above are true and correct')
    canvas.setFont('Helvetica', 9)
    canvas.drawString(365, 70, 'For')
    canvas.setFont('Helvetica-Bold', 11)
    canvas.drawString(390, 70, CUSTOMER_NAME)
    canvas.setFont('Helvetica', 7)
    canvas.drawString(425, 28, 'Authorized Signature')

def _createDCAuthorityInfo(canvas):
    ''' Creates DC Authority information
    '''
    canvas.setFont('Helvetica', 8)
    canvas.drawString(35, 80, 'Received the above material in good condition')
    canvas.drawString(35, 40, "Receiver's signature")
    canvas.setFont('Helvetica', 9)
    canvas.drawString(425, 80, 'For {}'.format(CUSTOMER_NAME))

def _setCompanyLogo(canvas):
    ''' Sets company logo to PDF
    '''
    canvas.drawImage(
        join(dirname(dirname(dirname(__file__))), 'logos', 'logo.png'), 40, 715, 50, 30)
    canvas.drawImage(
        join(dirname(dirname(dirname(__file__))), 'logos', 'iso.png'), 505, 715, 50, 30)

def _createOuterTemplate(canvas, pageNo, billNo):
    ''' Creates outermost template
    '''
    canvas.setFillColorRGB(0, 0, 1)
    canvas.setLineWidth(.3)

    canvas.setFont('Helvetica', 7)
    canvas.drawString(260, 15, 'Page {} for bill {}'.format(pageNo, billNo))
    canvas.roundRect(30, 25, 550, 750, 5, stroke=1, fill=0)

def createBillOuterTemplate(canvas, pageNo, billNo, title='original'):
    '''
    Creates outer template for the bill invoice(sales, performa)

    Params
        canvas (Canvas): Canvas object used to write in pdf
        pageNo (int): Page no to display in bill
        billNo (int): Bill No to display in bill
    '''
    _createOuterTemplate(canvas, pageNo, billNo)
    _setCompanyLogo(canvas)
    _createBillHeader(canvas, title)
    _createBillInfoTemplate(canvas)
    _createTransportTemplate(canvas)
    _createTableTemplate(canvas)
    _createBankTemplate(canvas)
    _createAmountTemplate(canvas)
    _createAuthorityTemplate(canvas)

def createDeliveryChallanOuterTemplate(canvas, pageNo, billNo):
    '''
    Creates outer template for delivery challan

    Params
        canvas (Canvas): Canvas object used to write in pdf
        pageNo (int): Page no to display in bill
        billNo (int): Bill No to display in bill
    '''
    _createOuterTemplate(canvas, pageNo, billNo)
    _setCompanyLogo(canvas)
    _createDCHeader(canvas)
    _createDCInfoTemplate(canvas)
    _createTransportTemplate(canvas)
    _createDCTableInfo(canvas)
    _createDCAuthorityInfo(canvas)

def createQuotationOuterTemplate(canvas, pageNo, billNo):
    '''
    Creates outer template for quotation

    Params
        canvas (Canvas): Canvas object used to write in pdf
        pageNo (int): Page no to display in bill
        billNo (int): Bill No to display in bill
    '''
    _createOuterTemplate(canvas, pageNo, billNo)
    _createQuotationBillHeader(canvas)
    _createQuotationInfoTemplate(canvas)
    _createQuotationTableInfo(canvas)
    _createAuthorityTemplate(canvas)


if __name__ == '__main__':
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen.canvas import Canvas
    canvas = Canvas(str('E:\darshan_auto_cable\pdf_templates\sample.pdf'), pagesize=letter)
    createOuterTemplate(canvas, '1', '3')