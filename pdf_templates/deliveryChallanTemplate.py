from re import split as _split
from copy import deepcopy as _deepcopy

from widgets import utils
from reportlab.lib.pagesizes import letter as _letter
from reportlab.pdfgen.canvas import Canvas as _Canvas
from outerTemplate import createDeliveryChallanOuterTemplate as _createDeliveryChallanOuterTemplate
import utilities as _utilities

class DeliveryChallanTemplate(object):
    ''' Template to create Delivery Challan template
    '''
    def __init__(self, canvas, deliveryChallanInformation):
        self.__deliveryChallanInformation = deliveryChallanInformation
        self.__canvas = canvas
        self.__count, self.__pageNo, self.__partIndex = 0, 1, 0
        self.__isNextPage = False

        self.__createInnerTemplate()
        _createDeliveryChallanOuterTemplate(self.__canvas, 1, 1)
        if self.__isNextPage:
            self.__canvas.showPage()
            nextDeliveryChallanInformation = _deepcopy(deliveryChallanInformation)
            nextDeliveryChallanInformation['particulars'] = nextDeliveryChallanInformation['particulars'][self.__count:]
            nextDeliveryChallanInformation['hsnCodes'] = nextDeliveryChallanInformation['hsnCodes'][self.__count:]
            nextDeliveryChallanInformation['quantities'] = nextDeliveryChallanInformation['quantities'][self.__count:]
            nextDeliveryChallanInformation['rates'] = nextDeliveryChallanInformation['rates'][self.__count:]
            nextDeliveryChallanInformation['amounts'] = nextDeliveryChallanInformation['amounts'][self.__count:]
            DeliveryChallanTemplate(canvas, nextDeliveryChallanInformation)

    def __setCustomerDetails(self):
        ''' Writes customer details to PDF
        '''
        self.__canvas.setFont('Helvetica', 10)
        self.__canvas.drawString(55, 665, self.__deliveryChallanInformation['customerName'])
        formattedCustAddr = _utilities.getCustomerAddress(self.__deliveryChallanInformation['customerAddress'])
        self.__canvas.setFont('Helvetica', 8)
        col = 645
        for addr in formattedCustAddr:
            self.__canvas.drawString(35, col, addr)
            col -= 22

    def _setCustomerGstinInformation(self):
        ''' Writes customer gstin and state code
        '''
        self.__canvas.setFont('Helvetica', 10)
        self.__canvas.drawString(125, 581, self.__deliveryChallanInformation['gstin'])
        self.__canvas.drawString(325, 581, self.__deliveryChallanInformation['stateCode'])

    def _setBillDetails(self):
        ''' Writes customer billing information
        '''
        self.__canvas.setFont('Helvetica', 8.5)
        self.__canvas.drawString(357, 672, self.__deliveryChallanInformation['dcNo'])
        self.__canvas.drawString(495, 672, self.__deliveryChallanInformation['dcDate'])
        self.__canvas.drawString(357, 651, self.__deliveryChallanInformation['poNo'])
        self.__canvas.drawString(495, 651, self.__deliveryChallanInformation['dcDate'])
        self.__canvas.drawString(357, 629, self.__deliveryChallanInformation['vendorCode'])
        self.__canvas.drawString(495, 629, self.__deliveryChallanInformation['paymentTerms'])
        self.__canvas.drawString(357, 607, self.__deliveryChallanInformation['vehicleNo'])
        if len(self.__deliveryChallanInformation['dispatchedThrough']) >13:
            self.__canvas.drawString(495, 613, self.__deliveryChallanInformation['dispatchedThrough'][:13]+'-')
        else:
            self.__canvas.drawString(495, 613, self.__deliveryChallanInformation['dispatchedThrough'][:13])
        self.__canvas.drawString(495, 601, self.__deliveryChallanInformation['dispatchedThrough'][13:])

    def __setTableData(self):
        ''' Writes table data
        '''
        total = 0
        col = 540
        self.__canvas.setFont('Helvetica', 8.5)
        for i, (itemno, particular, qt) in enumerate(
                zip(self.__deliveryChallanInformation['itemCodes'],
                    self.__deliveryChallanInformation['particulars'],
                    self.__deliveryChallanInformation['quantities'])):

            particular = _utilities.getParticular(particular.strip())
            nextPageCheckCol = col - (15) * len(particular)
            if nextPageCheckCol < 155:
                self.__pageNo += 1
                self.__isNextPage = True
                break
            self.__canvas.drawString(35, col, str(self.__partIndex + 1))

            self.__canvas.drawString(70, col, str(itemno.strip()))
            particularCol = col
            for i in range(len(particular)):
                if not particular[i]:
                    continue
                self.__canvas.drawString(150, particularCol, particular[i])
                particularCol = particularCol - 15

            total += float(utils.getIntegralPart(qt))
            _utilities.formatInPdf(self.__canvas,qt.strip(), 484, col, 13)
            col = particularCol - 5
            self.__count += 1
            self.__partIndex += 1
            if col < 155:
                self.__pageNo += 1
                self.__isNextPage = True
                break
        else:
            self.__pageNo += 1

        self.__canvas.setFont('Helvetica', 11)
        self.__canvas.drawString(455, 105, str(total))

    def __createInnerTemplate(self):
        ''' Sets argument values
        '''
        self.__setCustomerDetails()
        self._setCustomerGstinInformation()
        self._setBillDetails()
        self.__setTableData()


if __name__ == '__main__':
    dcInfo = {'customerName': 'Lokri Technologies',
              'customerAddress': 'LIG 46 old astc hudco',
              'gstin': '33AAFFD3275P1Z5',
              'stateCode': '33',
              'billNo': '1',
              'billDate':'24-12-2017',
              'poNo': '2',
              'poDate':'24-12-2017',
              'vendorCode': '2354',
              'paymentTerms': 'casg',
              'dcNo': '3',
              'dcDate':'24-12-2017',
              'vehicleNo': '234',
              'dispatchedThrough': 'KPN',
              'itemCodes':['ergdghdiugheiurghdri', 'erg', 'rthr', 'erg', 'erge', 'erge', 'erge'],
              'particulars':['4', '4', '4', '4', '4', '4', '4'],
              'quantities':['4', '4', '4', '4', '4', '4', '4']
              }
    canvas = _Canvas('dc.pdf', pagesize=_letter)
    bill = DeliveryChallanTemplate(canvas, dcInfo)
    canvas.save()