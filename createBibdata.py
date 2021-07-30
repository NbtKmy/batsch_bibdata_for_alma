import pykakasi
import pandas as pd
import re
import requests
import urllib3
import time
import os
import argparse 

# To set your environment variables in your terminal run the following line:
# export 'API_TOKEN'='<your_cinii_api_token>'
api_token = os.environ.get('API_TOKEN')

# Fields
Fdldr = [] # LDR - immer "#####nam#a2200409#c#4500" 
Fd008 = [] # 008 - bsp. "######sYYYY####ja ||||######|00|#||jpn#d"
F020a = [] # 020 $a
F040a = [] # 040 $a - immer "CH-ZuSLS UZB UAOI"
F040b = [] # 040 $b - immer "ger"
F040e = [] # 040 $e - immer "rda"
F041a = [] # 041 $a - immer "jpn"
Fd245006 = [] # 245 00 $6 - immer "880-01"
F24500a = [] # 245 00 $a
F24500b = [] # 245 00 $b
F24500c = [] # 245 00 $c
Fd880245006 = [] # 880 00 $6 (für 245 $6) - immer "245-01/Jpan"
F88024500a = [] # 880 00 $a (für 245 $a)
F88024500b = [] # 880 00 $b (für 245 $b)
F88024500c = [] # 880 00 $c (für 245 $c)
Fd2506 = [] # 250 $6 (wenn vorhanden) - immer "880-02"
F250a = [] # 250 $a 
Fd8802506 = [] # 880 $6 (für 250 $6) wenn vorhanden - immer "250-02/Jpan"
F880250a = [] # 880 $a (für 250 $a)
Fd264_16 = [] # 264 _1 $6 - immer "880-03"
F264_1a = [] # 264 _1 $a - immer "Tōkyō"
F264_1b = [] # 264 _1 $b
F264_1c = [] # 264 _1 $c
Fd8802646 = [] # 880 _1 $6 (für 264 _1 $6) - immer "264-03/Jpan"
F880264a = [] # 880 _1 $a (für 264 _1 $a) - immer "東京"
F880264b = [] # 880 _1 $b (für 264 _1 $b)
F880264c = [] # 880 _1 $c (für 264 _1 $c)
F300a = [] # 300 $a 
F300c = [] # 300 $c (Grösse usw.)
F336b = [] # 336 $b - immer "txt"
Fd3362 = [] # 336 $2 - immer "rdacontent"  
F337b = [] # 337 $b - immer "n"
Fd3372 = [] # 337 $2 - immer "rdamedia"
F338b = [] # 338 $b - immer "nc"
Fd3382 = [] # 338 $2 - immer "rdacarrier"
Fd49006 = [] # 490 0_ $6 (wenn vorhanden) - immer "880-04"
F4900a = [] # 490 0_ $a (wenn vorhanden)
Fd88049006 = [] # 880 0_ $6 (für 490 0_ $6) - immer "490-04/Jpan"
F8804900a = [] # 880 0_ $a (für 490 0_ $6)

Failed_list = []


def romaji_convert(text, bool):
    kks = pykakasi.kakasi()
    result = kks.convert(text)
    res_text = ""
    
    for item in result:
        if bool == True:
            res_text += (item['hepburn'].capitalize() + " ")
        else:
            res_text += (item['hepburn'] + " ")
        
    return res_text

def create_cont_Fd008(year):
    global Fd008
    s = "######sYYYY####ja ||||######|00|#||jpn#d"
    cont = re.sub("YYYY", year, s)
    Fd008.append(cont)

def create_cont_F24500ab(tk):
    trom = romaji_convert(tk, False)
    global F24500a
    global F24500b

    if ":" in trom:
        pos = trom.find(":")
        a = trom[0:pos]
        b = trom [pos+1:]
        F24500a.append(a)
        F24500b.append(b)
    else: 
        F24500a.append(trom)
        F24500b.append(None)

def create_cont_F24500c(crt):
    crrom = romaji_convert(crt, True)
    global F24500c
    F24500c.append(crrom)

def create_cont_F88024500ab(ttl):

    global F88024500a
    global F88024500b
    if ":" in ttl:
        pos = ttl.find(":")
        a = ttl[0:pos]
        b = ttl[pos+1:]
        F88024500a.append(a)
        F88024500b.append(b)
    
    elif "=" in ttl:
        pos = ttl.find("=")
        a = ttl[0:pos]
        b = ttl[pos:]
        F88024500a.append(a)
        F88024500b.append(b)

    else:
        F88024500a.append(ttl)
        F88024500b.append(None)

def create_cont_F250(bibdata):

    if 'prism:edition' in bibdata:
        edition = bibdata['prism:edition']
        Fd2506.append("880-02")
        edrom = romaji_convert(edition, False)
        F250a.append(edrom)
        Fd8802506.append("250-02/Jpan")
        F880250a.append(edition)
    else:
        Fd2506.append(None)
        F250a.append(None)
        Fd8802506.append(None)
        F880250a.append(None)

def create_cont_F264_1(publisher, date):
    pubrom = romaji_convert(publisher, True)

    F264_1b.append(pubrom)
    F264_1c.append(date)
    F880264b.append(publisher)
    F880264c.append(date)

def create_cont_F300(extent, size):
    
    if "p" in extent:
        extent = re.sub('p',' Seiten', extent)
    F300a.append(extent)
    F300c.append(size)

def create_cont_F490(bibdata):

    

    if 'dcterms:isPartOf' in bibdata:
        part_of_title = bibdata['dcterms:isPartOf'][0]['dc:title']
        Fd49006.append("880-04")
        pttrom = romaji_convert(part_of_title, False)
        F4900a.append(pttrom)
        Fd88049006.append("490-04/Jpan")
        F8804900a.append(part_of_title)
    else:
        Fd49006.append(None)
        F4900a.append(None)
        Fd88049006.append(None)
        F8804900a.append(None)



def create_data(sheet_name):

    df = pd.read_csv(sheet_name)
    isbn_col = df['ISBN']

    for i in isbn_col:
        j = re.sub('-', '', i)
        #print(j)

        requests.packages.urllib3.disable_warnings()
        requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
        try:
            requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
        except AttributeError:
            # no pyopenssl support used / needed / available
            pass

        cinii_api_isbn_prefix = "https://ci.nii.ac.jp/books/opensearch/search?count=1&isbn=" 
        cinii_api_isbn_suffix = "&format=json"
        cinii_api_isbn_full = cinii_api_isbn_prefix + j + cinii_api_isbn_suffix
        res = requests.get(cinii_api_isbn_full)
        data = res.json()
        l = len(data)
        if l == 0:
            Failed_list.append(j)
            continue
        else:
            cinii_api_link = data['@graph'][0]['items'][0]['rdfs:seeAlso']['@id']
            appid = "?appid=" + api_token
            cinii_api_full = cinii_api_link + appid
            time.sleep(3)
            api_res = requests.get(cinii_api_full)
            api_data = api_res.json()
            bibdata = api_data['@graph'][0]

            ##### Bibliographische Info holen
            title = bibdata['dc:title'][0]['@value']
            title_kata = bibdata['dc:title'][1]['@value']
            creator = bibdata['dc:creator']
            publisher = bibdata['dc:publisher'][0]
            extent = bibdata['dcterms:extent']
            size = bibdata['cinii:size']
            date = bibdata['dc:date']

            ##### eventuell Feld 700 hinzufügen
            #maker = bibdata['foaf:maker'][0]
            #maker_type = maker['@type'] # bspw. "foaf:Person"
            #maker_name = maker['foaf:name'][0]['@value']
            #maker_name_kata = maker['foaf:name'][1]['@value']

            ##### Felder mit immer gleicher Information
            Fdldr.append("#####nam#a2200409#c#4500")
            F020a.append(j)
            F040a.append("CH-ZuSLS UZB UAOI")
            F040b.append("ger")
            F040e.append("rda")
            F041a.append("jpn")
            Fd245006.append("880-01")
            Fd880245006.append("245-01/Jpan")
            F88024500c.append(creator)
            Fd264_16.append("880-03")
            F264_1a.append("Tōkyō")
            Fd8802646.append("264-03/Jpan")
            F880264a.append("東京")
            F336b.append("txt")
            Fd3362.append("rdacontent")
            F337b.append("n")
            Fd3372.append("rdamedia")
            F338b.append("nc")
            Fd3382.append("rdacarrier")

            ##### Weitere Felder erstellen
            create_cont_Fd008(date)
            create_cont_F24500ab(title_kata)
            create_cont_F24500c(creator)
            create_cont_F88024500ab(title)
            create_cont_F250(bibdata)
            create_cont_F264_1(publisher, date)
            create_cont_F300(extent, size)
            create_cont_F490(bibdata)

        
    ##### Alle Arrays in df 
    #print(Fdldr)
    zipped_lists = list(zip(Fdldr, Fd008, F020a, F040a, F040b, F040e, F041a, Fd245006, F24500a, F24500b, F24500c, Fd880245006, F88024500a, F88024500b, F88024500c, Fd2506, F250a, Fd8802506, F880250a, Fd264_16, F264_1a, F264_1b, F264_1c, Fd8802646, F880264a, F880264b, F880264c, F300a, F300c, F336b, Fd3362, F337b, Fd3372, F338b, Fd3382, Fd49006, F4900a, Fd88049006, F8804900a))
    col_name = ["LDR", "008", "020$a", "040$a", "040$b", "040$e", "041$a", "24500$6", "24500$a", "24500$b", "24500$c", "88000$6", "88000$a", "88000$b", "88000$c", "250$6", "250$a", "880$6", "880$a", "264 1$6", "264 1$a", "264 1$b", "264 1$c", "880 1$6", "880 1$a", "880 1$b", "880 1$c", "300$a", "300$c", "336$b", "336$2", "337$b", "337$2", "338$b", "338$2", "4900 $6", "4900 a$", "8800 $6", "8800 $a"]
    res_df = pd.DataFrame(zipped_lists, columns = col_name)
    res_df.head()
    res_df.to_csv("res.csv", index=False, header= True,)

    len_failed = len(Failed_list)
    if len_failed > 0:
        failed_res = "\n無理でしたごめんち ".join(Failed_list)
        with open("failed_list.txt", mode='w') as f:
            f.write(failed_res)




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Dieses Code erstellt eine csv-File für ALMA') 
    parser.add_argument('file_name', help='Bitte gehen Sie den Filenamen ein') 
    args = parser.parse_args() 


    sheet_name = args.file_name
    create_data(sheet_name)