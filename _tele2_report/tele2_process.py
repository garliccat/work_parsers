
from glob import glob
import numpy as np
import pandas as pd
from datetime import datetime as dt
import PyPDF2


def operator_find(rawline):
    operators = ['МТС', 'Теле2', 'Билайн', 'Мегафон']
    for operator in operators:
        if operator in rawline:
            return operator

def type_find(rawline):
    cases = {
    'Исх. ': 'call_out',
    'Вх. ': 'call_in',
    'Входящее сообщение': 'sms_in',
    'Исх. сообщение': 'sms_out',
    'Мобильный интернет': 'internet'
    }
    for i in cases.keys():
        if i in rawline:
            return cases[i]


# takes only first one
f = glob('*.pdf')[0]
# df = tabula.read_pdf(f)

file = open(f, 'rb')
filereader = PyPDF2.PdfFileReader(file)

print(filereader.numPages)
print(filereader.getPage(0).extractText())