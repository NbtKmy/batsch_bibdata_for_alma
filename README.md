# Creating CSV file for the importing bibliographic data into ALMA

## Requirements
* pykakasi
* pandas
* requests 
* urllib3

and CiNii API Access Token https://support.nii.ac.jp/ja/cinii/api/developer

## Usage

1. Put your CiNii API Access Token in your environment variable

`export 'API_TOKEN'='<your token>'`

1. Run the Code with an augument (csv file name) like:

`python createBibdata.py test.csv`

