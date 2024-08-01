
import os,sys

import datetime

from collections import OrderedDict

import shutil

import pandas as pd

current_file_dir = os.path.dirname(os.path.abspath(__file__))

sys.path.append(current_file_dir)

sys.path.append('C:\\AitangResearch\\IQMAnalyzer')



class ExcelIQMReport(object):
    
    """
    
    A class for processing the IQM excel file.
        
    """
    
    def __init__(self,excel_iqm_report_file):
        
        self.excel_report=excel_iqm_report_file
        
    @staticmethod
    
    def is_excel_delivered(iqm_excel_report_file):
        
        """
        To judge if the excel report was delivered.
        
        """
        
        file_name_split=iqm_excel_report_file.split('_')
      
              
        if 'TreatmentFieldReport' in file_name_split:
          
            treated=True
        
        return(treated)    
          
    def excel2df(self):
        
        """
        Reading the excel file into dataframe.
        
        """
        
        
        iqm_df=pd.read_excel(self.excel_report,sheet_name='IQM Report',header=2)
        
                     
        return (iqm_df)
    
    def get_sbs_df(self):
        
        """
        Get sub dataframe containg sbs info.
        
        """
        sbs_subdf=pd.DataFrame()
        
                
        if ExcelIQMReport.is_excel_delivered(self.excel_report):
        
            sbs_heads=['Patient ID','Plan Name','Treatment Machine Name','Field ID',r'Field Energy [MV]','IQM Detector Serial','MU','SbS Reference Signal',	'SbS Measured Signal',r'SbS Relative Deviation [%]']
            
            iqm_df=self.excel2df()
            
                      
                     
            sbs_subdf=iqm_df[sbs_heads]
            
            sbs_subdf=sbs_subdf[sbs_subdf['Patient ID'] !='Period:']
            
            sbs_subdf=sbs_subdf[sbs_subdf['Patient ID'] !='Template v1.0.20']
                         
        return(sbs_subdf)
        
        
    def get_tms_df(self):
        
        """
        
        Get sub dataframe containg total measurement signal.
        
        """
        
        tms_heads=['Patient ID','Plan Name','Treatment Machine Name','Field ID',r'Field Energy [MV]','IQM Detector Serial',u'Field MU/Fraction','Total Reference Signal','Total Measured Signal']
               
        iqm_df=self.excel2df()
                         
        tms_subdf=iqm_df[tms_heads]
                                         
        return(tms_subdf)        
        
           
                
if __name__=='__main__':
    
    """
    Unit test.
    """
    
    # 0
    
    excel_report=r'C:\AitangResearch\IQMAnalyzer\testData\ExcelReport\1029525\2022-01-31_09-04-12_TreatmentFieldReport_PatientId_1029525_Field_102.xlsx'
    
    #excel_report=r'C:\AitangResearch\IQMAnalyzer\testData\ExcelReport\1662308\2022-01-27_05-08-27_CalculationReport_PatientId_1662308_PlanName_LNODESBRSTSIB.xlsx'
    
    # 1 
    
    excel_iqm_obj=ExcelIQMReport(excel_report)
    
    excel_iqm_obj.excel2df()
    
    # 2 
    
    sbs_df=excel_iqm_obj.get_sbs_df()
    
    print(len(sbs_df ))
    
    # 3 
    
    #tms_df=excel_iqm_obj.get_tms_df()
    
    #print(tms_df)
    
    
    
    