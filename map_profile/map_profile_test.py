import pdfplumber
import os
from map_profile import settings
from map_profile import ExtractDataMap


def parse_map_pdf():
    filename = "Student+Profile.pdf"
    pdffilestored = os.path.join(settings.MEDIA_ROOT, filename)

    with pdfplumber.open(pdffilestored) as pdf:
        content = ''
        # len(pdf.pages)为PDF文档页数
        for i in range(len(pdf.pages)):
            # pdf.pages[i] 是读取PDF文档第i+1页
            page = pdf.pages[i]
            # page.extract_text()函数即读取文本内容，下面这步是去掉文档最下面的页码
            page_content = '\n'.join(page.extract_text().split('\n')[:-1])
            content = content + page_content
        # print(content)

    pdffilenameportion = os.path.splitext(filename)

    txtfilename = pdffilenameportion[0] + '.txt'

    txtfilestored = os.path.join(settings.MEDIA_ROOT, txtfilename)

    with open(txtfilestored, "w", encoding='utf-8') as f:
        f.write(content)

    ExtractDataMap(txtfilestored, '15895901300')