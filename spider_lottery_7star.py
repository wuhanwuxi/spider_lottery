#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib.request
import datetime
from bs4 import BeautifulSoup

#g_year = ""
g_year_short = ""

def spider_7star():
    lottery_file = open("7star.txt", "wb")
    finish = False
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
    for history_index in range(1, 113):
        webstr = 'http://www.lottery.gov.cn/historykj/history_%d.jspx?_ltype=qxc' % history_index
        print(webstr.encode('utf-8'))

        request = urllib.request.Request(webstr, headers=header)
        response = urllib.request.urlopen(request, timeout=10)
        soup = BeautifulSoup(response, "html.parser")
        response.close()
        tables = soup.findAll('table')
        tab = tables[0]

        row=0
        for tr in tab.findAll('tr'):
            column = 0
            row=row+1
            if(row == 1 or row == 2):
                continue
            for td in tr.findAll('td'):
                if(column == 0 or column == 1 or column == 17):
                    lotteryvalue = td.getText()+'\t'
                    lottery_file.write(lotteryvalue.encode('utf-8'))
                    #print(td.getText())
                column = column+1
            if (finish):
                break
            lottery_file.write("\n".encode('utf-8'))
        if (finish):
            break
    lottery_file.close()


def spider_7star_recent():
    lottery_file = open("7star.txt", "wb")
    finish = False
    for history_index in range(1, 113):
        webstr = 'http://www.lottery.gov.cn/historykj/history_%d.jspx?_ltype=qxc' % history_index
        print(webstr.encode('utf-8'))

        response = urllib.request.urlopen(webstr)
        soup = BeautifulSoup(response, "html.parser")
        response.close()
        tables = soup.findAll('table')
        tab = tables[0]

        row=0
        for tr in tab.findAll('tr'):
            column = 0
            row=row+1
            if(row == 1 or row == 2):
                continue
            for td in tr.findAll('td'):
                if(history_index > 6):
                    if(column == 0):
                        if(not td.getText().startswith(g_year_short)):
                            finish = True
                            break

                if(column == 0 or column == 1 or column == 17):
                    lotteryvalue = td.getText()+'\t'
                    lottery_file.write(lotteryvalue.encode('utf-8'))
                    #print(td.getText())
                column = column+1
            if (finish):
                break
            lottery_file.write("\n".encode('utf-8'))
        if (finish):
            break
    lottery_file.close()


def regular_forward(input_filename, output_filename):
    print ("regular_forward")
    lottery_file = open(input_filename, "r")
    output_file = open(output_filename, "wb")

    listA = []
    for fline in lottery_file.readlines():
        s = fline[0:14]
        listA.append(s)

    listA.reverse()
    for s in listA:
        output_file.write(s.encode('utf-8'))
        output_file.write('\r\n'.encode('utf-8'))

    lottery_file.close()
    output_file.close()


def regular_filter(prefix, input_filename, output_filename):
    print ("regular_filter")
    lottery_file = open(input_filename, "r")
    output_file = open(output_filename, "wb")
    for fline in lottery_file.readlines():
        if fline.startswith(prefix):
            output_file.write(fline.encode('utf-8'))
    lottery_file.close()
    output_file.close()


def regular_compress(columns, rows_each_page, input_filename, output_filename):
    print ("regular_compress")
    lottery_file = open(input_filename, "r")
    output_file = open(output_filename, "wb")

    list_data = []
    for fline in lottery_file.readlines():
        list_data.append(fline[0:14])

    list_page = []
    column=0
    row=0
    for s in list_data:
        if (row == rows_each_page):
            column = column + 1;
            row = 0;

        if (column == 0):
            list_page.append(s)
        else:
            if(column == columns):
                output_file.write('期号\t结果\t\t期号\t结果\t\t期号\t结果\t\t期号\t结果\t\r\n'.encode('utf-8'))
                for output_row in list_page:
                    output_file.write(output_row.encode('utf-8'))
                    output_file.write('\r\n'.encode('utf-8'))
                list_page=list()
                list_page.append(s)
                column = 0
                row=1
                continue
            else:
                list_page[row] = list_page[row] + "\t" + s
        row = row + 1

    if ( len(list_page) != 0):
        output_file.write('期号\t结果\t\t期号\t结果\t\t期号\t结果\t\t期号\t结果\t\r\n'.encode('utf-8'))
        for output_row in list_page:
            output_file.write(output_row.encode('utf-8'))
            output_file.write('\r\n'.encode('utf-8'))

    lottery_file.close()
    output_file.close()


def regular_compress_groupbyyear(columns, rows_each_page, input_filename, output_filename):
    print ("regular_compress")
    lottery_file = open(input_filename, "r")
    output_file = open(output_filename, "wb")

    curyear = '04'
    list_data = []
    for fline in lottery_file.readlines():
        list_data.append(fline[0:14])

    list_page = []
    column=0
    row=0
    for s in list_data:
        if (row == rows_each_page):
            column = column + 1;
            row = 0;

        if (not s.startswith(curyear)):
            column = columns
            curyear = s[0:2]
            print('curyear is %2s, data is %18s\n' % (curyear, s))

        if (column == 0):
            list_page.append(s)
        else:
            if(column == columns):
                output_file.write('期号\t结果\t\t期号\t结果\t\t期号\t结果\t\t期号\t结果\t\r\n'.encode('utf-8'))
                row_in_page=0
                for output_row in list_page:
                    output_file.write(output_row.encode('utf-8'))
                    output_file.write('\r\n'.encode('utf-8'))
                    row_in_page=row_in_page+1
                while(row_in_page<rows_each_page):
                    output_file.write('\r\n'.encode('utf-8'))
                    row_in_page = row_in_page + 1

                list_page=list()
                list_page.append(s)
                column = 0
                row=1
                continue
            else:
                list_page[row] = list_page[row] + "\t" + s
        row = row + 1

    if ( len(list_page) != 0):
        output_file.write('期号\t结果\t\t期号\t结果\t\t期号\t结果\t\t期号\t结果\t\r\n'.encode('utf-8'))
        for output_row in list_page:
            output_file.write(output_row.encode('utf-8'))
            output_file.write('\r\n'.encode('utf-8'))

    lottery_file.close()
    output_file.close()


def get_prefix():
    today = datetime.date.today()
    #g_year = today.year
    g_year_short = today.strftime("%y")

    return g_year_short

if __name__ == "__main__":
    g_year_short = get_prefix()
    #spider_7star()
    #regular_forward("7star.txt", "7star_forward.txt")
    #regular_filter("18", "7star_forward.txt", "7star_filtered.txt")
    #regular_compress(4, 34, "7star_forward.txt", "7star_compress.txt")
    regular_compress_groupbyyear(4, 39, "7star_forward.txt", "7star_compress_byyear.txt")