#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib.request
import datetime
import os
from bs4 import BeautifulSoup


# from spider_lottery_sort5_format import regular_forward
# from spider_lottery_sort5_format import regular_compress


def spider_sort5():
    lottery_file = open("sort5.txt", "wb")
    finish = False
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
    for history_index in range(1, 257):
        webstr = 'http://www.lottery.gov.cn/historykj/history_%d.jspx?_ltype=plw' % history_index
        print(webstr.encode('utf-8'))
        request = urllib.request.Request(webstr, headers=header)
        response = urllib.request.urlopen(request, timeout=10)
        soup = BeautifulSoup(response, "html.parser")
        response.close()
        tables = soup.findAll('table')
        tab = tables[0]

        row = 0
        for tr in tab.findAll('tr'):
            column = 0
            row = row + 1
            if (row == 1 or row == 2):
                continue
            for td in tr.findAll('td'):
                if (column == 0 or column == 1 or column == 7):
                    lotteryvalue = td.getText() + '\t'
                    lottery_file.write(lotteryvalue.encode('utf-8'))
                    # print(td.getText())
                column = column + 1
            if (finish):
                break
            lottery_file.write("\n".encode('utf-8'))
        if (finish):
            break
    lottery_file.close()


def spider_sort5_recent():
    lottery_file = open("sort5.txt", "wb")
    finish = False
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
    for history_index in range(1, 255):
        webstr = 'http://www.lottery.gov.cn/historykj/history_%d.jspx?_ltype=plw' % history_index
        print(webstr.encode('utf-8'))
        request = urllib.request.Request(webstr, headers=header)
        response = urllib.request.urlopen(request, timeout=10)
        soup = BeautifulSoup(response, "html.parser")
        response.close()
        tables = soup.findAll('table')
        tab = tables[0]

        row = 0
        for tr in tab.findAll('tr'):
            column = 0
            row = row + 1
            if (row == 1 or row == 2):
                continue
            for td in tr.findAll('td'):
                if (history_index > 6):
                    if (column == 0):
                        if (not td.getText().startswith(g_year_short)):
                            finish = True
                            break
                if (column == 0 or column == 1 or column == 7):
                    lotteryvalue = td.getText() + '\t'
                    lottery_file.write(lotteryvalue.encode('utf-8'))
                    # print(td.getText())
                column = column + 1
            if (finish):
                break
            lottery_file.write("\n".encode('utf-8'))
        if (finish):
            break
    lottery_file.close()


def spider_sort5_increment():
    ret = False
    try:
        lottery_file = open("sort5.txt", "r")
    except:
        print("open sort5.txt fail\n")
        return False
    try:
        line = lottery_file.readline()
        print("line is \"%s\"\n" % line)
        lastnumber = line[0:5]
        print("lastnumber is \"%s\"\n" % lastnumber)
    except:
        print("get lastnumber from sort5.txt fail\n")
        lottery_file.close()
        return False
    lottery_file.close()

    lottery_file_implement = open("sort5_implement.txt", "wb")
    finish = False
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}

    for history_index in range(1, 255):
        webstr = 'http://www.lottery.gov.cn/historykj/history_%d.jspx?_ltype=plw' % history_index
        print(webstr.encode('utf-8'))
        request = urllib.request.Request(webstr, headers=header)
        response = urllib.request.urlopen(request, timeout=10)
        soup = BeautifulSoup(response, "html.parser")
        response.close()
        tables = soup.findAll('table')
        tab = tables[0]

        row = 0
        for tr in tab.findAll('tr'):
            column = 0
            row = row + 1
            if (row == 1 or row == 2):
                continue
            for td in tr.findAll('td'):
                if (column == 0 and td.getText().startswith(lastnumber)):
                    finish = True
                    break
                if (column == 0 or column == 1 or column == 7):
                    lotteryvalue = td.getText() + '\t'
                    lottery_file_implement.write(lotteryvalue.encode('utf-8'))
                    # print(td.getText())
                column = column + 1
            if (finish):
                break
            lottery_file_implement.write("\n".encode('utf-8'))
        if (finish):
            break

    lottery_file = open("sort5.txt", "r")
    for fline in lottery_file.readlines():
        lottery_file_implement.write(fline.encode('utf-8'))

    lottery_file_implement.close()
    lottery_file.close()

    os.remove("sort5.txt")
    os.rename("sort5_implement.txt", "sort5.txt")
    return True


def regular_forward():
    lottery_file = open("sort5.txt", "r")
    output_file = open("sort5_forward.txt", "wb")

    listA = []
    for fline in lottery_file.readlines():
        s = fline[0:16]
        listA.append(s)

    listA.reverse()
    for s in listA:
        output_file.write(s.encode('utf-8'))
        output_file.write('\r\n'.encode('utf-8'))

    lottery_file.close()
    output_file.close()


def regular_compress(columns, rows_each_page):
    lottery_file = open("sort5_forward.txt", "r")
    output_file = open("sort5_forward_compress.txt", "wb")

    list_data = []
    for fline in lottery_file.readlines():
        list_data.append(fline[0:16])

    list_page = []
    column = 0
    row = 0
    for s in list_data:
        if (row == rows_each_page):
            column = column + 1;
            row = 0;

        if (column == 0):
            list_page.append(s)
        else:
            if (column == columns):
                output_file.write('期号\t结果\t\t期号\t结果\t\t期号\t结果\t\t期号\t结果\t\r\n'.encode('utf-8'))
                for output_row in list_page:
                    output_file.write(output_row.encode('utf-8'))
                    output_file.write('\r\n'.encode('utf-8'))
                list_page = list()
                list_page.append(s)
                column = 0
                row = 1
                continue
            else:
                list_page[row] = list_page[row] + "\t" + s
        row = row + 1

    if (len(list_page) != 0):
        output_file.write('期号\t结果\t\t期号\t结果\t\t期号\t结果\t\t期号\t结果\t\r\n'.encode('utf-8'))
        for output_row in list_page:
            output_file.write(output_row.encode('utf-8'))
            output_file.write('\r\n'.encode('utf-8'))

    lottery_file.close()
    output_file.close()


def regular_compress_groupbyyear(columns, rows_each_page):
    lottery_file = open("sort5_forward.txt", "r")
    output_file = open("sort5_forward_compress_byyear.txt", "wb")

    curyear = '04'
    list_data = []
    for fline in lottery_file.readlines():
        list_data.append(fline[0:16])

    list_page = []
    column = 0
    row = 0
    for s in list_data:

        if (row == rows_each_page):
            column = column + 1;
            row = 0;

        if (column == 0):
            list_page.append(s)
        else:
            if (not s.startswith(curyear)):
                column = columns
                curyear = s[0:2]
                print('curyear is %2s, data is %18s\n' % (curyear, s))

            if (column == columns):
                output_file.write('期号\t结果\t\t期号\t结果\t\t期号\t结果\t\t期号\t结果\t\r\n'.encode('utf-8'))
                for output_row in list_page:
                    output_file.write(output_row.encode('utf-8'))
                    output_file.write('\r\n'.encode('utf-8'))
                list_page = list()
                list_page.append(s)
                column = 0
                row = 1
                continue
            else:
                list_page[row] = list_page[row] + "\t" + s
        row = row + 1

    if (len(list_page) != 0):
        output_file.write('期号\t结果\t\t期号\t结果\t\t期号\t结果\t\t期号\t结果\t\r\n'.encode('utf-8'))
        for output_row in list_page:
            output_file.write(output_row.encode('utf-8'))
            output_file.write('\r\n'.encode('utf-8'))

    lottery_file.close()
    output_file.close()


def regular_filter(prefix, input_filename, output_filename):
    print("regular_filter")
    lottery_file = open(input_filename, "r")
    output_file = open(output_filename, "wb")
    for fline in lottery_file.readlines():
        if fline.startswith(prefix):
            output_file.write(fline.encode('utf-8'))
    lottery_file.close()
    output_file.close()


def get_prefix():
    today = datetime.date.today()
    # g_year = today.year
    g_year_short = today.strftime("%y")

    return g_year_short


def generate_html():
    lottery_file = open("sort5_forward.txt", "r")
    output_file = open("sort5.html", "wb")
    output_file.write("<html  xmlns=\"http://www.w3.org/TR/REC-html40\">\n".encode('utf-8'))
    output_file.write(" <head>\n".encode('utf-8'))
    output_file.write(" <meta charset=\"utf-8\">\n".encode('utf-8'))
    output_file.write(" </head>\n".encode('utf-8'))
    output_file.write(" <body>\n".encode('utf-8'))
    output_file.write("  <button id=\"goto2004\" name=\"goto2004\"><a href=\"#2004\">跳到2004</a></button></br>\n".encode('utf-8'))
    output_file.write("  <button id=\"goto2005\" name=\"goto2005\"><a href=\"#2005\">跳到2005</a></button></br>\n".encode('utf-8'))
    output_file.write("  <button id=\"goto2006\" name=\"goto2006\"><a href=\"#2006\">跳到2006</a></button></br>\n".encode('utf-8'))
    output_file.write("  <button id=\"goto2007\" name=\"goto2007\"><a href=\"#2007\">跳到2007</a></button></br>\n".encode('utf-8'))
    output_file.write("  <button id=\"goto2008\" name=\"goto2008\"><a href=\"#2008\">跳到2008</a></button></br>\n".encode('utf-8'))
    output_file.write("  <button id=\"goto2009\" name=\"goto2009\"><a href=\"#2009\">跳到2009</a></button></br>\n".encode('utf-8'))
    output_file.write("  <button id=\"goto2010\" name=\"goto2010\"><a href=\"#2010\">跳到2010</a></button></br>\n".encode('utf-8'))
    output_file.write("  <button id=\"goto2011\" name=\"goto2011\"><a href=\"#2011\">跳到2011</a></button></br>\n".encode('utf-8'))
    output_file.write("  <button id=\"goto2012\" name=\"goto2012\"><a href=\"#2012\">跳到2012</a></button></br>\n".encode('utf-8'))
    output_file.write("  <button id=\"goto2013\" name=\"goto2013\"><a href=\"#2013\">跳到2013</a></button></br>\n".encode('utf-8'))
    output_file.write("  <button id=\"goto2014\" name=\"goto2014\"><a href=\"#2014\">跳到2014</a></button></br>\n".encode('utf-8'))
    output_file.write("  <button id=\"goto2015\" name=\"goto2015\"><a href=\"#2015\">跳到2015</a></button></br>\n".encode('utf-8'))
    output_file.write("  <button id=\"goto2016\" name=\"goto2016\"><a href=\"#2016\">跳到2016</a></button></br>\n".encode('utf-8'))
    output_file.write("  <button id=\"goto2017\" name=\"goto2017\"><a href=\"#2017\">跳到2017</a></button></br>\n".encode('utf-8'))
    output_file.write("  <button id=\"goto2018\" name=\"goto2018\"><a href=\"#2018\">跳到2018</a></button></br>\n".encode('utf-8'))
    output_file.write("  <button id=\"goto2019\" name=\"goto2019\"><a href=\"#2019\">跳到2019</a></button></br>\n".encode('utf-8'))

    prefix="04"
    output_file.write("  <table id=\"2004\" name=\"2004\" width=\"262\">\n".encode('utf-8'))

    for fline in lottery_file.readlines():
        if fline.startswith(prefix):
            output_file.write("   <tr>\n".encode('utf-8'))
            output_file.write(("    <td>"+fline[0:5]+"</td>\n").encode('utf-8'))
            output_file.write(("    <td>"+fline[6:-1]+"</td>\n").encode('utf-8'))
            output_file.write("   </tr>\n".encode('utf-8'))
        else:
            output_file.write("  </table>\n".encode('utf-8'))
            prefix=fline[0:2]
            output_file.write(("  <table id=\"20%2s\" name=\"20%2s\" width=\"262\">\n" %(prefix,prefix)).encode('utf-8'))
            output_file.write("   <tr>\n".encode('utf-8'))
            output_file.write(("    <td>"+fline[0:5]+"</td>\n").encode('utf-8'))
            output_file.write(("    <td>"+fline[6:-1]+"</td>\n").encode('utf-8'))
            output_file.write("   </tr>\n".encode('utf-8'))

    output_file.write("  </table>\n".encode('utf-8'))
    output_file.write(" </body>\n".encode('utf-8'))
    output_file.write("</html>\n".encode('utf-8'))

    output_file.close()
    lottery_file.close()


if __name__ == "__main__":
    g_year_short = get_prefix()
    # spider_sort5()
    # regular_compress_groupbyyear(4, 33)
    # regular_compress(4, 33)

    can_increment = spider_sort5_increment()
    if(not can_increment):
        spider_sort5()
    regular_forward()
    generate_html()
