

from reportlab.lib.pagesizes import letter as _letter
from reportlab.pdfgen.canvas import Canvas as _Canvas
from os.path import join as _join
from re import split as _split
from copy import deepcopy as _deepcopy
from outerTemplate import createQuotationOuterTemplate as _createQuotationOuterTemplate
import utilities as _utilities


class QuotationTemplate(object):
    ''' Template to create Quotation template
    '''
    def __init__(self, canvas, quotationInformation):
        self.__canvas = canvas
        self.__quotationInformation = quotationInformation

        self.__count, self.__pageNo, self.__partIndex = 0, 1, 0
        self.__isNextPage = False

        self._createInnerTemplate()
        _createQuotationOuterTemplate(self.__canvas, 1, 1)
        if self.__isNextPage:
            self.__canvas.showPage()
            nextQuotationInformation = _deepcopy(quotationInformation)
            nextQuotationInformation['particulars'] = nextQuotationInformation['particulars'][self.__count:]
            nextQuotationInformation['hsnCodes'] = nextQuotationInformation['hsnCodes'][self.__count:]
            nextQuotationInformation['quantities'] = nextQuotationInformation['quantities'][self.__count:]
            nextQuotationInformation['rates'] = nextQuotationInformation['rates'][self.__count:]
            nextQuotationInformation['amounts'] = nextQuotationInformation['amounts'][self.__count:]
            QuotationTemplate(canvas, nextQuotationInformation)

    def _setCustomerDetails(self):
        ''' Writes customer details to PDF
        '''
        self.__canvas.setFont('Helvetica', 10)
        self.__canvas.drawString(55, 665, self.__quotationInformation['customerName'])
        formattedCustAddr = _utilities.getCustomerAddress(self.__quotationInformation['customerAddress'])
        self.__canvas.setFont('Helvetica', 8)
        col = 645
        for addr in formattedCustAddr:
            self.__canvas.drawString(35, col, addr)
            col -= 22

    def _setQuotationDetails(self):
        ''' Writes quotation details to PDF
        '''
        self.__canvas.setFont('Helvetica', 8.5)
        self.__canvas.drawString(370, 672, self.__quotationInformation['billNo'])
        self.__canvas.drawString(370, 642, self.__quotationInformation['quotationDate'])
        self.__canvas.drawString(370, 612, self.__quotationInformation['validDate'])

    def _setAmountData(self):
        ''' Writes amount details to PDF
        '''
        self.__canvas.drawString(567, 180, self.__quotationInformation['amountBeforePs'])
        self.__canvas.drawString(400, 165, self.__quotationInformation['cgst'])
        self.__canvas.drawString(567, 165, self.__quotationInformation['cgstPs'])
        self.__canvas.drawString(400, 150, self.__quotationInformation['sgst'])
        self.__canvas.drawString(567, 150, self.__quotationInformation['sgstPs'])
        self.__canvas.drawString(400, 135, self.__quotationInformation['igst'])
        # _utilities.formatInPdf(self.__canvas, self.__quotationInformation['igstRs'], 550, 135, 8)
        self.__canvas.drawString(567, 135, self.__quotationInformation['igstPs'])

        _utilities.formatInPdf(self.__canvas, self.__quotationInformation['amountBeforeRs'], 549, 180, 12)
        _utilities.formatInPdf(self.__canvas, self.__quotationInformation['cgstRs'], 549, 165, 8)
        _utilities.formatInPdf(self.__canvas, self.__quotationInformation['sgstRs'], 549, 150, 8)
        _utilities.formatInPdf(self.__canvas, self.__quotationInformation['igstRs'], 549, 135, 8)

        _utilities.formatInPdf(self.__canvas, self.__quotationInformation['origTaxPs'], 572, 120, 12)
        _utilities.formatInPdf(self.__canvas, self.__quotationInformation['afterTaxRs'], 549, 105, 12)
        self.__canvas.drawString(567, 105, self.__quotationInformation['afterTaxPs'])

        self.__canvas.setFont('Helvetica', 11)
        col = 62
        for word in self.__quotationInformation['amountWord']:
            self.__canvas.drawString(36, col, word)
            col -= 14

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

    def _setTableData(self):
        '''
        Writes table data
        '''
        col = 535
        for i, (particular, hsn, qt, rat, amount) in enumerate(
                zip(self.__quotationInformation['particulars'],
                    self.__quotationInformation['hsnCodes'],
                    self.__quotationInformation['quantities'],
                    self.__quotationInformation['rates'],
                    self.__quotationInformation['amounts'])):
            self.__canvas.setFont('Helvetica', 8.5)
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

            rateRs, ratePs = str(round(float(rat), 2)).split('.')

            self.__canvas.drawString(487, col, ratePs)
            amountRs, amountPs = str(round(float(amount), 2)).split('.')

            self.__canvas.drawString(567, col, amountPs)

            _utilities.formatInPdf(self.__canvas, hsn.strip(), 364, col, 10)
            _utilities.formatInPdf(self.__canvas, qt.strip(), 425, col, 13)
            _utilities.formatInPdf(self.__canvas, rateRs, 466, col, 8)
            _utilities.formatInPdf(self.__canvas, amountRs, 549, col, 12)

            col = particularCol - 5
            self.__count += 1
            self.__partIndex += 1
            if col < 195:
                self.__pageNo += 1
                self.__isNextPage = True
                break
        else:
            self.__pageNo += 1

    def _createInnerTemplate(self):
        '''
        Sets argument values
        '''
        self._setCustomerDetails()
        self._setQuotationDetails()
        self._setTableData()

        self.__canvas.setFont('Helvetica', 8.5)
        self._setAmountData()


if __name__ == '__main__':
    # billInfo = {
    #     'customerName': 'Lokri Technologies',
    #     'customerAddress': 'LIG 46 old astc hudco',
    #     'gstin': '33AAFFD3275P1Z5',
    #     'stateCode': '33',
    #     'billNo': '1',
    #     'billDate': '24-12-2017',
    #     'poNo': '2',
    #     'quotationDate': '24-12-2017',
    #     'vendorCode': '2345',
    #     'paymentTerms': 'casg',
    #     'dcNo': '3',
    #     'validDate': '24-12-2017',
    #     'vehicleNo': '7726',
    #     'dispatchedThrough': 'kpn',
    #     'particulars': [
    #                    'wsdfwegerv er',
    #                    'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w'],
    #     'hsnCodes': ['42345345563545', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4','4'],
    #     'quantities': ['23 litres', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4'],
    #     'rates': ['453454563', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4', '4'],
    #     'amounts': ['34534535355', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '4'],
    #     'amount': '234',
    #     'amountBeforeRs': '34',
    #     'amountBeforePs': '0',
    #     'cgst': '3%',
    #     'cgstRs': '3',
    #     'cgstPs': '0',
    #     'sgst': '3%',
    #     'sgstRs': '3',
    #     'sgstPs': '0',
    #     'igst': '3%',
    #     'igstRs': '3',
    #     'igstPs': '0',
    #     'afterTaxPs': '0',
    #     'afterTaxRs': '23',
    #     'origTaxPs': '0',
    #     'amountWithTaxRs': '6',
    #     'amountWithTaxPs': '0',
    #     'amountWord': ['Eight lakh and Twenty two thousand and', ' Twenty-two rupees and  zero paise only'],
    # }
    billInfo = {'afterTaxRs': ' 1', 'customerName': u'Fgjiuoh', 'amountBeforePs': '00', 'amountBeforeRs': ' 1', 'particulars': [u'iufghiug'], 'origTaxPs': '', 'sgst': '0%', 'quotationDate': '21-Aug-18', 'cgstPs': '00', 'rates': [8787.0], 'hsnCodes': [u'iugiug1'], 'cgstRs': ' 0', 'cgst': '0%', 'igst': '0%', 'igstRs': ' 0', 'customerAddress': u'iougouigiu', 'quantities': [u'3'], 'validDate': '21-Aug-18', 'igstPs': '00', 'billNo': u'1', 'sgstPs': '00', 'amountWord': [u'd'], 'sgstRs': ' 0', 'amounts': [26361.0], 'afterTaxPs': '00'}
    {'afterTaxRs': ' 1572', 'customerName': u'Hariharah', 'amountBeforePs': '00', 'amountBeforeRs': ' 1156',
     'particulars': ['dfiugig'], 'origTaxPs': '', 'sgst': '9%', 'quotationDate': '04-Sep-18', 'cgstPs': '00',
     'rates': ['34.0'], 'hsnCodes': ['3i4'], 'cgstRs': ' 0', 'cgst': '9%', 'igst': '18%', 'igstRs': ' 0',
     'customerAddress': u'lig 46 old astc hudcp', 'quantities': ['34'], 'validDate': '04-Sep-18', 'igstPs': '00',
     'billNo': u'1', 'sgstPs': '00',
     'amountWord': [u'Rs.', u'One', u'Thousand', u'Five', u'Hundred', u'And', u'Seventy', u'Two', u'only'],
     'sgstRs': ' 0', 'amounts': ['1156.0'], 'afterTaxPs': '00'}

    canvas = _Canvas('quotation.pdf', pagesize=_letter)
    bill = QuotationTemplate(canvas, billInfo)
    canvas.save()