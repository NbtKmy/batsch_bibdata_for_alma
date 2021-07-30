# Creating CSV file for the importing bibliographic data into ALMA
With this Code you can create a csv file which contains many bibliographical data. 
The bibliographical information is created from the CiNii Books. Thus the user of this code must 
follow the Academic Content Service Usage Regulations and CiNii Articles Usage Detailed Regulations by NII.
The commercial use of the CiNii data is not allowed, if you don't have an agreement with NII.


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

