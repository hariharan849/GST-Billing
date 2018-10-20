from os.path import join as _join
from re import split as _split


def formatInPdf(canvas, text, rowNo, colNo, maxLen):
    ''' Formats the info based on the len of the table and text
    '''
    actualText = []
    i = 0
    if len(text) == 1:
        actualText.append(text)
    while i < len(text) - 1:
        actualText.append(text[i:i + maxLen])
        i += maxLen

    for i in range(len(actualText)):
        if i != len(actualText) - 1:
            actualText[i] += '-'

    rowNo += 2
    for i in range(len(actualText)):
        for j in range(len(actualText[i])):
            canvas.drawString(rowNo - (j * 4.3) - 1, colNo - (i * 8), actualText[i][-j - 1])

def getCustomerAddress(customerAddress):
    ''' Returns customer address by splitting to set in table
    '''
    count = 0
    formattedAddress = []
    sample_str = ''
    for cust in _split('[^a-zA-Z0-9\.\,]', customerAddress):
        if isinstance(cust, (str, unicode)) and count + len(cust) < 43:
            sample_str += '{} '.format(cust)
            count += len(cust)
        else:
            formattedAddress.append(sample_str)
            sample_str = '{} '.format(cust)
            count = len(sample_str)
    if len(formattedAddress) > 1 and count + len(formattedAddress[-1]) < 43:
        formattedAddress[-1] += sample_str
    else:
        formattedAddress.append(sample_str)

    return formattedAddress

def getParticular(particular):
    ''' Returns customer address by splitting to set in table
    '''
    particularItem = _split('[^a-zA-Z0-9\.\,]', particular)
    formattedParticular = []

    splitted_customer = []
    for word in particularItem:
        if len(word) > 42:
            for i in range(0, len(word), 42):
                splitted_customer.append(word[i:i+42])
        else:
            splitted_customer.append(word)
    particularItem = splitted_customer
    tempStr = ''
    count = 0
    for cust in particularItem:
        if isinstance(cust, str) and count + len(cust) < 42:
            tempStr += '{} '.format(cust)
            count += len(cust) + 1
        else:
            formattedParticular.append(tempStr)
            tempStr = '{} '.format(cust)
            count = len(tempStr) + 1
    if len(formattedParticular) > 1 and count + len(''._join(formattedParticular[-1])) < 42:
        formattedParticular[-1] += tempStr
    else:
        formattedParticular.append(tempStr)
    return formattedParticular
