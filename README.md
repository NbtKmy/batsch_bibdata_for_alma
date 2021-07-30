# Creating a CSV file for the importing bibliographic data into ALMA
With this Code you can create a csv file which contains many bibliographical data. 
The bibliographical information is created from the CiNii Books. Thus the user of this code needs a CiNii API token and must 
follow the Academic Content Service Usage Regulations and CiNii Articles Usage Detailed Regulations by NII.
A commercial use of the CiNii data is not allowed, if you don't have any agreement with NII.

About the format of the CSV for ALMA import see the [Importing Records with CSV or Excel Files](https://knowledge.exlibrisgroup.com/Alma/Product_Documentation/010Alma_Online_Help_(English)/040Resource_Management/060Record_Import/075Importing_Records_with_CSV_or_Excel_Files) in the Exlibris Knowledge Center


## Requirements
* pykakasi
* pandas
* requests 
* urllib3

and CiNii API Access Token https://support.nii.ac.jp/ja/cinii/api/developer

## Usage

1. Put your CiNii API Access Token in your environment variable:  
`export 'API_TOKEN'='<your token>'`

1. Run the Code with an argument (csv file name) like:  
`python createBibdata.py test.csv`

## Result
You find the result csv file under [res_test.csv](https://github.com/NbtKmy/batsch_bibdata_for_alma/blob/main/res_test.csv).

