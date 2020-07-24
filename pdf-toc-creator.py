# coding: utf8
import os,io
import sys
import getopt,codecs
import PyPDF2
import re
reload(sys)
sys.setdefaultencoding('utf-8') # 解决PyPDF2不能很好处理中文的问题

## 用法
# 参数说明
#   1) offset, 实际pdf文件中的页码应该比toc文件中指定的页码偏移多少，正整数表示pdf文件中页码更大
# toc文件格式说明：
#   1）一行产生一个目录标签，以左边tab缩进表示目录层级(必须是tab)
#   2）页码在每行最后，用半角分号分隔

## 用例
# python pdf-toc-creator.py -f InfoQ-2020中国技术发展白皮书.pdf -o 3 -t toc-infoq.txt


def main(argv):
    origFileName = ''
    tocFileName = ''
    offset = 0
    
    try:
        opts, args = getopt.getopt(argv, "hf:o:t:", ["file=", "offset=", "toc="])
    except getopt.GetoptError:
        print 'python pdf-toc-creator.py -f <pdf_file_name> -o <pageno_offset> -t <toc_file_name>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'python pdf-toc-creator.py -f <pdf_file_name> -o <pageno_offset> -t <toc_file_name>'
            sys.exit()
        elif opt in ("-f", "--file"):
            origFileName = arg
        elif opt in ("-o", "--offset"):
            offset = int(arg)
        elif opt in ("-t", "--toc"):
            tocFileName = arg
    newFileName = re.sub(r'\.pdf$', "_toc.pdf", origFileName)
    pdfFile = open(origFileName,'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFile)
    if pdfReader.isEncrypted:
      pdfReader.decrypt('')
    pdfWriter = PyPDF2.PdfFileWriter()
    # pdfWriter.setPageMode("/UseNone")

    #####################
    # 如果原来被pdf expert编辑过，会有空的outline root, 直接cloneDocumentFromReader在addBookmark会报异常
    # ValueError: {'/Type': '/Outlines'} is not in list
    ###################
    pdfWriter.cloneDocumentFromReader(pdfReader)

    parentsBookmark = []
    MAX_LEVEL = 10
    for i in range(0, MAX_LEVEL):
        parentsBookmark.append(None)
    tocLines = open(tocFileName, 'r')
    for line in tocLines:
        tabCnt = len(re.findall(r'^(\t*)', line)[0])
        if tabCnt >= MAX_LEVEL:
            print 'too many level'
            sys.exit(2)
        title = line.split(';')[0]
        title = re.sub(r'^\t*', '', title)
        pageNo = int((line.split(';')[1]).strip()) + offset
        parent = parentsBookmark[tabCnt - 1] if tabCnt > 0 else None
        parentsBookmark[tabCnt] = pdfWriter.addBookmark(title.decode('utf-8'), pageNo, parent)

    newFile = open(newFileName,'wb')
    pdfWriter.write(newFile)
    newFile.flush()

    pdfFile.close()
    newFile.close()    


if __name__ == "__main__":
    main(sys.argv[1:])
