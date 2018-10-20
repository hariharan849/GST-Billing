from re import split as _split
from os.path import join as _join
from reportlab.lib.pagesizes import letter as _letter
from reportlab.pdfgen.canvas import Canvas as _Canvas
from copy import deepcopy as _deepcopy
from outerTemplate import createBillOuterTemplate as _createBillOuterTemplate
import utilities as _utilities


class InvoiceTemplate(object):
    ''' Template to create invoice template
    '''
    def __init__(self, canvas, billInformation, title):
        self.__billInformation = billInformation
        self.__canvas = canvas
        self.__count, self.__pageNo, self.__partIndex = 0, 1, 0
        self.__isNextPage = False

        self.__createInnerTemplate()
        _createBillOuterTemplate(self.__canvas, 1, 1, title)
        if self.__isNextPage:
            self.__canvas.showPage()
            nextBillInformation = _deepcopy(billInformation)
            print self.__count
            nextBillInformation['particulars'] = nextBillInformation['particulars'][self.__count:]
            nextBillInformation['hsnCodes'] = nextBillInformation['hsnCodes'][self.__count:]
            nextBillInformation['quantities'] = nextBillInformation['quantities'][self.__count:]
            nextBillInformation['rates'] = nextBillInformation['rates'][self.__count:]
            nextBillInformation['amounts'] = nextBillInformation['amounts'][self.__count:]
            InvoiceTemplate(canvas, nextBillInformation)

    def __formatInPdf(self, text, rowNo, colNo, maxLen):
        '''
        Formats the info based on the len of the table and text
        '''
        actualText = []
        i = 0
        if len(text) == 1:
            actualText.append(text)
        while i < len(text)-1:
            actualText.append(text[i:i+maxLen])
            i += maxLen

        for i in range(len(actualText)):
            if i != len(actualText)-1:
                actualText[i] += '-'

        rowNo += 2
        for i in range(len(actualText)):
            for j in range(len(actualText[i])):
                self.__canvas.drawString(rowNo-(j*4.3)-1, colNo-(i*8), actualText[i][-j-1])

    def __setCustomerDetails(self):
        '''
        Writes customer details to PDF
        '''
        self.__canvas.drawString(55, 665, self.__billInformation['customerName'])
        formattedCustAddr = _utilities.getCustomerAddress(self.__billInformation['customerAddress'])
        self.__canvas.setFont('Helvetica', 8)
        col = 645
        for addr in formattedCustAddr:
            self.__canvas.drawString(35, col, addr)
            col -= 22

    def _setCustomerGstinInformation(self):
        '''
        Writes customer gstin and state code
        '''
        self.__canvas.setFont('Helvetica', 10)
        self.__canvas.drawString(105, 581, self.__billInformation['gstin'])
        self.__canvas.drawString(325, 581, self.__billInformation['stateCode'])

    def __setBillDetails(self):
        '''
        Writes customer billing information
        '''
        self.__canvas.drawString(357, 672, self.__billInformation['billNo'])
        self.__canvas.drawString(495, 672, self.__billInformation['billDate'])
        self.__canvas.drawString(357, 656, self.__billInformation['poNo'])
        self.__canvas.drawString(495, 656, self.__billInformation['poDate'])
        self.__canvas.drawString(357, 640, self.__billInformation['vendorCode'])
        self.__canvas.drawString(495, 640, self.__billInformation['paymentTerms'])
        self.__canvas.drawString(357, 624, self.__billInformation['dcNo'])
        self.__canvas.drawString(495, 624, self.__billInformation['dcDate'])
        self.__canvas.drawString(357, 607, self.__billInformation['vehicleNo'])
        if len(self.__billInformation['dispatchedThrough']) > 13:
            self.__canvas.drawString(495, 613, self.__billInformation['dispatchedThrough'][:13]+'-')
        else:
            self.__canvas.drawString(495, 613, self.__billInformation['dispatchedThrough'][:13])
        self.__canvas.drawString(495, 601, self.__billInformation['dispatchedThrough'][13:])

    def _get_particular(self, particular):
        import re
        customer_particular = re.split('[^a-zA-Z0-9\.\,]', particular)
        count = 0
        return_list = []
        sample_str = ''
        splitted_customer = []
        for word in customer_particular:
            if len(word) > 42:
                for i in range(0, len(word), 42):
                    splitted_customer.append(word[i:i + 42])
            else:
                splitted_customer.append(word)
        customer_particular = splitted_customer
        for cust in customer_particular:
            if (''.join(cust).isupper() or isinstance(cust, str)) and count + len(cust) < 42:
                sample_str += cust + ' '
                count += len(cust) + 1
            elif (''.join(cust).islower() or isinstance(cust, str)) and count + len(cust) < 42:
                sample_str += cust + ' '
                count += len(cust) + 1
            else:
                return_list.append(sample_str)
                sample_str = cust + ' '
                count = len(sample_str) + 1
        if len(return_list) > 1 and count + len(''.join(return_list[-1])) < 42:
            return_list[-1] += sample_str
        else:
            return_list.append(sample_str)
        return return_list

    def __setTableData(self):
        ''' Writes table data
        '''
        col = 535
        self.__canvas.setFont('Helvetica', 8.5)
        for i, (particular, hsn, qt, rate, amount) in enumerate(zip(
                self.__billInformation['particulars'],
                self.__billInformation['hsnCodes'],
                self.__billInformation['quantities'],
                self.__billInformation['rates'],
                self.__billInformation['amounts'])):
            # particular = _utilities.getParticular(particular.strip())
            particular = self._get_particular(particular.strip())
            nextPageCheckCol = col - (15) * len(particular)
            if nextPageCheckCol < 195:
                self.__pageNo += 1
                self.__isNextPage = True
                break
            self.__canvas.drawString(35, col, str(self.__partIndex + 1))

            particularCol = col

            for i in range(len(particular)):
                if not particular[i]:
                    continue
                self.__canvas.drawString(70, particularCol, particular[i])
                particularCol = particularCol-15

            rateRs, ratePs = str(round(float(rate), 2)).split('.')

            self.__canvas.drawString(487, col, ratePs)
            amountRs, amountPs = str(round(float(amount), 2)).split('.')

            self.__canvas.drawString(567, col, amountPs)
            _utilities.formatInPdf(self.__canvas,hsn.strip(), 364, col, 10)
            _utilities.formatInPdf(self.__canvas,qt.strip(), 425, col, 13)
            _utilities.formatInPdf(self.__canvas,rateRs, 466, col, 8)
            _utilities.formatInPdf(self.__canvas,amountRs, 549, col, 12)

            col = particularCol - 5
            self.__count += 1
            self.__partIndex += 1
            if col < 195:
                self.__pageNo += 1
                self.__isNextPage = True
                break
        else:
            self.__pageNo += 1

    def __setAmountInformation(self):
        '''
        Writes amount details in pdf.
        '''
        self.__canvas.drawString(567, 180, self.__billInformation['amountWithoutTaxPs'])
        self.__canvas.drawString(400, 165, self.__billInformation['cgst'])
        self.__canvas.drawString(567, 165, self.__billInformation['cgstPs'])

        self.__canvas.drawString(400, 150, self.__billInformation['sgst'])
        self.__canvas.drawString(567, 150, self.__billInformation['sgstPs'])

        self.__canvas.drawString(400, 135, self.__billInformation['igst'])
        self.__canvas.drawString(567, 135, self.__billInformation['igstPs'])

        _utilities.formatInPdf(self.__canvas,self.__billInformation['amountWithoutTaxRs'], 549, 180, 12)
        _utilities.formatInPdf(self.__canvas,self.__billInformation['cgstRs'], 549, 165, 8)
        _utilities.formatInPdf(self.__canvas,self.__billInformation['sgstRs'], 549, 150, 8)
        _utilities.formatInPdf(self.__canvas,self.__billInformation['igstRs'], 549, 135, 8)
        _utilities.formatInPdf(self.__canvas,self.__billInformation['taxPs'], 572, 120, 12)
        _utilities.formatInPdf(self.__canvas,self.__billInformation['amountWithTaxRs'], 549, 105, 12)
        self.__canvas.drawString(567, 105, self.__billInformation['amountWithTaxPs'])

        self.__canvas.setFont('Helvetica', 11)
        col = 62
        for amountWord in self.__billInformation['amountWord']:
            self.__canvas.drawString(36, col, amountWord)
            col -= 14

    def __createInnerTemplate(self):
        '''
        Sets argument values in pdf
        '''
        self.__canvas.setFont('Helvetica', 10)
        self.__setCustomerDetails()
        self._setCustomerGstinInformation()

        self.__canvas.setFont('Helvetica', 8.5)
        self.__setBillDetails()
        self.__setTableData()

        self.__canvas.setFont('Helvetica', 8.5)
        self.__setAmountInformation()

if __name__ == '__main__':
    billInfo = {
        'CustomerName': 'Lokri Technologies',
        'CustomerAddress': 'LIG 46 old astc hudco',
        'gstin': '33AAFFD3275P1Z5',
        'stateCode': '33',
        'billNo': '1',
        'billDate': '24-12-2017',
        'poNo': '2',
        'poDate': '24-12-2017',
        'vendorCode': '2345',
        'paymentTerms': 'casg',
        'dcNo': '3',
        'dcDate': '24-12-2017',
        'vehicleNo': '7726',
        'dispatchedThrough': 'kpn',
        'particulars': [
                       'wsdfwegerv er wkhgk iubiusgvd iuisv iugisdv iuigsd iugigsdiuiu siudiu iuiugsd iuhiusd uoihihsd iouhiouhds ihiuhd iuhu',
                       'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w'],
        'hsnCodes': ['42345345563545', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4','4'],
        'quantities': ['23 litres', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4'],
        'rates': ['453454563', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4'],
        'amounts': ['34534535355', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '4'],
        'amountWithoutTaxRs': '34',
        'amountWithoutTaxPs': '0',
        'cgst': '3%',
        'cgstRs': '3',
        'cgstPs': '0',
        'sgst': '3%',
        'sgstRs': '3',
        'sgstPs': '0',
        'igst': '3%',
        'igstRs': '3',
        'igstPs': '0',
        'taxPs': '0',
        'amountWithTaxRs': '6',
        'amountWithTaxPs': '0',
        'amountWord': ['Eight lakh and Twenty two thousand and', ' Twenty-two rupees and  zero paise only'],
        'fileName': 'ergerge.pdf'
    }
    canvas = _Canvas('ergerge.pdf', pagesize=_letter)
    bill = InvoiceTemplate(canvas, billInfo)
    canvas.save()