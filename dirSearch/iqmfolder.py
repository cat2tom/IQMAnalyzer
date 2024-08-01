import os,sys

import datetime

from collections import OrderedDict

import shutil

current_file_dir = os.path.dirname(os.path.abspath(__file__))

sys.path.append(current_file_dir)

sys.path.append('C:\\AitangResearch\\IQMAnalyzer')

import pandas as pd

from pdfConversion.txtconversion import pdf2txt

from reportAnalysis.iqm_delivery_report import  IQMReport  # field_qa_results2df,patient_qa_results2df

from excelReport.excel_report import ExcelIQMReport


pdfbox_jarfile='C:/AitangResearch/IQMAnalyzer/pdfConversion/pdfbox-app-2.0.27.jar'


def copy_specified_files(folder, dest_folder,file_ext,key_words):
  
   
  """
  Copy all files specified from one folder to another folder. 
  
  """
  
  all_iqm_reports=[]
   
  for dirpath, dirs, files in os.walk(folder): 
    for filename in files:
      
      fname = os.path.join(dirpath,filename)
      
                
      if fname.endswith(file_ext) and key_words in fname:
             
        all_iqm_reports.extend([fname])
        
        shutil.copy2(fname, dest_folder)
        
        print('Copied file:'+fname)
        
  print('Finished all the copy.')

def combine_csv_files(iqm_folder):
  
  """
  
  """
  
  df_list=[]
  
  for dirpath, dirs, files in os.walk(iqm_folder): 
    for filename in files:
      
      fname = os.path.join(dirpath,filename)
           
      if fname.endswith('.csv'):
        
        print(fname)
        
        each_df=pd.read_csv(fname)
        
        df_list.append(each_df)
        
       
 
        
        #df_list=df_list+each_df
             
        #df_list.extend([each_df])
        
         
  combined_df=pd.concat(df_list)
  
  combined_file=os.path.join(iqm_folder,'combined_results.csv')
  
  combined_df.to_csv(combined_file)
  
  
  print('All excel files were combined into one excel file.')
  
         
   
  

def get_iqm_daily_reports(iqm_folder): 
  """
  Get all iqm daily report under iqm_foler recursivley 
  
  """

  all_iqm_reports=[]
  
  for dirpath, dirs, files in os.walk(iqm_folder): 
    for filename in files:
      
      fname = os.path.join(dirpath,filename)
           
      if fname.endswith('.pdf') and 'PatientPlanDailyReport' in fname:
             
        all_iqm_reports.extend([fname])
        
  return all_iqm_reports

def get_excel_reports(iqm_folder):
  
  """
  
  Get all excel daily treatment reports containing all measured and calculated info 
  
  """
  
  all_iqm_reports=[]
  
  for dirpath, dirs, files in os.walk(iqm_folder): 
    for filename in files:
      
      fname = os.path.join(dirpath,filename)
           
           
      #if fname.endswith('.xlsx') and 'TreatmentFieldReport' in fname:
        
      if fname.endswith('.xlsx'):
        
          all_iqm_reports.extend([fname])
        
  return all_iqm_reports

def is_excel_delivered(iqm_excel_report_file):
  
  """
  To judge if the excel report was delivered.
  
  """
  
  treated=False
  if 'TreatmentFieldReport ' in iqm_excel_report_file:
    
    treated=True
  
  return(treated)
    

def combine_SBS2df(iqm_folder):
  
  """
  Go through the iqm_folder to get all excel report and write all results into an excel file.   
  
  """
  
  all_iqm_reports=[]
  
  sbs_df_list=[]
    
  for dirpath, dirs, files in os.walk(iqm_folder): 
    
    for filename in files:
      
      fname = os.path.join(dirpath,filename)
           
           
      #if fname.endswith('.xlsx') and 'TreatmentFieldReport' in fname:
        
      if fname.endswith('.xlsx'):
        
        if 'TreatmentFieldReport' in fname:
        
          excel_report_obj=ExcelIQMReport(fname)
          
          sbs_df=excel_report_obj.get_sbs_df()
          
          sbs_df_list.append(sbs_df)
          
    
  return sbs_df_list  

def write_combinedSBS2excel(iqm_folder,combined_sbs_file='combined_sbs_file.xlsx'):
  
  
  """
  Write the combined SBS to an excel file.
  
  """
  
  sbs_df_list=combine_SBS2df(iqm_folder)
  
  print(sbs_df_list)
  
  combined_df=pd.concat(sbs_df_list)
  
  combined_df.to_excel(combined_sbs_file)
    

def write_qa_results2df(iqm_folder):
  
  """
  
  Go through the folder and write patient and field QA results into dataframe.  
  """
  
  all_daily_reports= get_iqm_daily_reports(iqm_folder)
  
  qa_reports_txt=[pdf2txt(each_pdf) for each_pdf in all_daily_reports]
  

  
  # patient qa results under one dir
  
  patients_qa_df=[IQMReport(iqm_report_txt).patient_qa_results2df() for iqm_report_txt in qa_reports_txt]
  
 
  
  if len(patients_qa_df)==1:
    
    dir_patients_qa_df=patients_qa_df[0]
    
  else:
    
  
    dir_patients_qa_df=pd.concat( patients_qa_df)
  
  fields_qa_df=[IQMReport(iqm_report_txt).field_qa_results2df() for iqm_report_txt in qa_reports_txt]
  
  if len(fields_qa_df)==1:
    
    dir_fields_qa_df=fields_qa_df[0]
    
  else:
       
    dir_fields_qa_df=pd.concat(fields_qa_df)
  
  
  return (dir_patients_qa_df,dir_fields_qa_df)


def write_qa_results2csv(iqm_folder, export_dir):
  
  """
  
  Write QA results into csv files for one folder.
  
  """
  
  current_time=datetime.datetime.now().strftime("%I_%M%p_%B_%d_%Y")
  
  patient_qa_csv=os.path.join(export_dir,'patient_qa_result_'+current_time+'.csv')
  
  field_qa_csv=os.path.join(export_dir,'field_qa_result_'+current_time+'.csv')
  
  (dir_patients_qa_df,dir_fields_qa_df)=write_qa_results2df(iqm_folder)
  
  dir_patients_qa_df.to_csv(patient_qa_csv,index=False)
  
  dir_fields_qa_df.to_csv(field_qa_csv,index=False)
  
 
def get_iqm_patient_subfolders(root_iqm_folder):
  
  """
  Get iqm patient subfolders under the root_iqm_folder.
  
  """
  iqm_patient_subfolders=[]
    
  for dirpath, dirs, files in os.walk(root_iqm_folder): 
    
    for dir_name in dirs:
      
      dir_name = os.path.join(dirpath,dir_name)
           
      iqm_patient_subfolders.extend([dir_name])
        
  return iqm_patient_subfolders  


def is_patient_iqm_delivered(patient_subfolder):
  
  """
  
   Return true if patient iqm delivered on the machine.
  
  """
  
  daily_reports=get_iqm_daily_reports(patient_subfolder)
  
   
  is_delivered=False
  
  if daily_reports:
    
    is_delivered=True
    
  return is_delivered

def patient_subfolder2csv(iqm_folder,export_dir):
   
  """
  Write patient folder and deliver info to dataframe 
  """
  
  
  
  mrn_list=[]
  
  delivery_list=[]
  
    
  all_patient_folders=get_iqm_patient_subfolders(iqm_folder)
  
  for each_folder in  all_patient_folders: 
    
    mrn=each_folder.split(os.sep)[-1]
      
    is_delivered=is_patient_iqm_delivered(each_folder)
    
    if is_delivered:
    
      mrn_list.extend([mrn])
      
      delivery_list.extend(['delivered'])
      
 
    else:
      
      mrn_list.extend([mrn])
           
      delivery_list.extend([' '])     
      
    
 
  patient_folder_df=pd.DataFrame({'Patients':mrn_list,'Status':delivery_list})
  
  export_file_name=os.path.join(export_dir,'Patients_IQM_delivered_list.csv')
  
 
  patient_folder_df.to_csv(export_file_name)
  
  return export_file_name
  
   


if __name__=='__main__':
  
  # 0
  iqm_folder="C:\\AitangResearch\\IQMAnalyzer\\testData\\iqmDir"
  
  export_dir="C:\\AitangResearch\\IQMAnalyzer\\testData\\csv"
  
  #iqm_folder="A:\\"
  
  patient_subfolder='C:\\AitangResearch\\IQMAnalyzer\\testData\\iqmDir\\0076730'
  
  patient_subfolder='V:\\CTC-LiverpoolOncology\\temp\\AX\\iqmDir\\1138914 - Copy'
  
     
  #patient_subfolder='C:\\AitangResearch\\IQMAnalyzer\\testData\\iqmDir\\1138914'
  
   
  # # 1  
  
  #all_iqm_report=get_iqm_daily_reports(iqm_folder)
  
  #for each_report in all_iqm_report:
    
    #print(each_report)
        
    
  # # 2 
  #iqm_patient_subfolders=get_iqm_patient_subfolders(iqm_folder)
  
  #print(len(iqm_patient_subfolders))
  
  # # 3 
  
  
  is_deilvered=is_patient_iqm_delivered(patient_subfolder)
  
  #print(is_deilvered)
  
 
  
  # # 4
  
  #patient_qa_df,field_qa_df=write_qa_results2df(iqm_folder)
  
  #input_pdf_file='C:\\AitangResearch\\IQMAnalyzer\\testData\\iqmDir\\0994573\\20220815_PatientPlanDailyReport_PatientId_0994573_PlanName_BLADDER.pdf'
  
  #pdf2txt(pdfbox_jarfile,input_pdf_file)
  
  # # 5
  
  #write_qa_results2csv(iqm_folder, export_dir)
  
  # # 6
  
  #export_file_name='delivered_patient_mrn.csv'
  
  #patient_subfolder2csv(iqm_folder,export_dir)
  
  # # 7
  
  #folder=r"V:\CTC-LiverpoolOncology\temp\IQMReport"
  
  #dest_folder="V:\\CTC-LiverpoolOncology\\PROJECTS\\IQM detector\\NewRSIQMModel\\RetrospectiveStudy\\DeliveredPatientList"
  
  #dest_folder=r"V:\CTC-LiverpoolOncology\PROJECTS\IQM detector\NewRSIQMModel\RetrospectiveStudy\DeliveredPatientList"
  
  ##dest_folder=r"V:\CTC-LiverpoolOncology\PROJECTS\IQM detector\NewRSIQMModel\RetrospectiveStudy\PatientQAResults"
  
  #dest_folder=r"V:\CTC-LiverpoolOncology\PROJECTS\IQM detector\NewRSIQMModel\RetrospectiveStudy\FieldQAResutls"
  
  
  #key_words=r"delivered_list"
  
  key_words=r"delivered_list"
  
  key_words=r"field_qa"
  
  key_words=r"patient_qa"
  
  file_ext=r".csv"
  
  
  
  #copy_specified_files(folder, dest_folder,file_ext,key_words)
  
  # # 8
  
  #dest_folder=r'V:\CTC-LiverpoolOncology\temp\SeparatedCSV\patientQA'
  
  #dest_folder=r'V:\CTC-LiverpoolOncology\temp\SeparatedCSV\fieldQA'
  
  #dest_folder=r'V:\CTC-LiverpoolOncology\temp\SeparatedCSV\deliverList'
  
  dest_folder=r'V:\CTC-LiverpoolOncology\PROJECTS\IQM detector\NewRSIQMModel\RetrospectiveStudy\PSQAPatientList\SeparatedCSVFiles'
  
  #iqm_folder=dest_folder
  #combine_csv_files(iqm_folder)
  
  
  # # 9
  
  excel_iqm_report_folder=r'C:\AitangResearch\IQMAnalyzer\testData\ExcelReport'
  
  #excel_iqm_report_folder=r'C:\AitangResearch\IQMAnalyzer\testData\iqmDir'
  
  #all_excel_report=get_excel_reports(excel_iqm_report_folder)
  
  #print(all_excel_report)
  
  # # 10 
  
  #sbs_df_list=combine_SBS2df(excel_iqm_report_folder)
  
  #print(sbs_df_list)
  
  # # 11 
  
  write_combinedSBS2excel(excel_iqm_report_folder)
  
  
      
        