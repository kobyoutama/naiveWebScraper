# pdf scraper - sourced from "https://www.geeksforgeeks.org/downloading-pdfs-with-python-using-requests-and-beautifulsoup/"

import requests
import pdfkit
import os
from fpdf import FPDF
from bs4 import BeautifulSoup


def scrapePDF(baseURL, links, out):
    # For all links check for pdf link and download
    for link in links:
        if '.pdf' in link.get('href', []):
            file_name = link.get('href')
            file_name = file_name[file_name.rfind('/') + 1:]
            path = os.path.join(out, file_name)
            if(os.path.exists(path)): continue
            print('Downloading pdf file: ', file_name)
            # try:
            # Get response object for link
            # response = requests.get(baseURL+'/'+link.get('href'))
            response = requests.get('https://www.ics.uci.edu/~pattis/ICS-33/'+link.get('href'))

            # Write into pdf
            # with open(path, 'wb') as pdf:
            #     pdf.write(response.content)
            #
            pdf = open(path, 'wb')
            pdf.write(response.content)
            pdf.close()
            print(f"{file_name} Downloaded")
            #except:
            #    print(f'failed to download {file_name}')
    print('Scrape Complete PDF\n')

def htmlToPDF(baseURL, links, out):
    for link in links:
        if '.txt' in link.get('href', []):
            file_name = link.get('href')
            file_name = file_name[file_name.rfind('/') + 1:]
            print('Downloading txt file: ', file_name)
            # try:
            #     # Get response object for link
            #response = requests.get(baseURL + '/' + link.get('href'))
            response = requests.get('https://www.ics.uci.edu/~pattis/ICS-33/' + link.get('href'))
            path = os.path.join(out, file_name)
            with open(path, 'w+', encoding='UTF-8') as f:
                f.write(response.text)
            print(f"{file_name} Downloaded")
            # except:
            #     print(f'failed to download {file_name}')
    print('Scrape Complete TXT\n')

def parse_line():
    line = input("{pdf/txt/q} {URL} {[Optional] Output Directory}\n")
    if line == 'q': quit()
    line = line.split(' ', 1)
    if len(line) == 3 and os.path.exists(line[2]):
        out = line[2]
    else:
        out = os.path.join(os.getcwd(), 'downloaded')
        if not os.path.exists(out):
            os.mkdir(out)
    return line[0], line[1], out

def main():
    option, url, path = parse_line()
    # Requests URL and get response object
    response = requests.get(url)

    # Parse text object
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all hyperlinks present on page
    page = soup.find_all('a')

    if (option == 'pdf'):
        scrapePDF(url, page, path)
    elif (option == 'txt'):
        htmlToPDF(url, page, path)
    elif (option == 'all'):
        scrapePDF(url, page, path)
        htmlToPDF(url, page, path)

def txt_to_pdf(file):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', size=12)
    dire, file_name = os.path.split(file)
    file_name, _ = os.path.splitext(file_name)
    print(f'working on {file_name}')
    file_name = "conv_"+ file_name + '.pdf'
    f = open(file, 'r', encoding='UTF-8')
    try:
        for x in f.readlines():
            pdf.cell(200,3,txt=x,ln=1,align='L')
        pdf.output(os.path.join(dire, file_name))
    except:
        print(f'unsuccessful on {file_name}')
    finally:
        f.close()

def delFiles():
    path = os.path.join(os.getcwd(), 'downloaded')
    for file in os.listdir(path):
        os.remove(os.path.join(path, file))

if __name__ == '__main__':
    # main()
    path = os.path.join(os.getcwd(), 'downloaded')
    for file in os.listdir(path):
        if file.endswith('.txt'):
            txt_to_pdf(os.path.join(path, file))
    # delFiles()
