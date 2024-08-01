import subprocess

import os 

import ntpath



def get_pdfbox_jar():
    
    '''
    Get pdfbox jar file assuming jar file copied into the same dir as this module file.
        
    '''
       
    pdfbox_jarfile='C:/AitangResearch/IQMAnalyzer/pdfBoxJar/pdfbox-app-2.0.27.jar'
    
       
      
    return(pdfbox_jarfile)


def pdf2txt(input_pdf_file,):
    
       
        
    pdfbox_jarfile=get_pdfbox_jar()
    
    pdf_path,ext=os.path.splitext(input_pdf_file)
    
      
    output_txt_file=pdf_path+'.txt'
    
        
    cmd='java -jar '+pdfbox_jarfile+' ExtractText '+ input_pdf_file +' '+output_txt_file
    
      
    try:
        
        subprocess.check_call(cmd,shell=True)
        
        print('Sucessfully convert pdf to txt for file: '+input_pdf_file)
        
        return  output_txt_file
      
    except subprocess.CalledProcessError:
        
        print('Failed to convert pdf to txt for file: '+input_pdf_file )
        
        return None
        

if __name__=='__main__':

    from pathlib2 import PurePath
    # test get_pdfbox_jar()
    
    pdfbox_jarfile=get_pdfbox_jar()
    
 
    # test data 
    
    input_pdf_file='C:\\AitangResearch\\IQMAnalyzer\\testData\\\oneReport\\20220719_PatientPlanDailyReport_PatientId_0495766_PlanName_LARYNX.pdf'  
    
    #input_pdf_file='C:\AitangResearch\IQMAnalyzer\testData\iqmDir\0994573\20220815_PatientPlanDailyReport_PatientId_0994573_PlanName_BLADDER.pdf'
    
   
    # pdf2txt
    
    pdf2txt(input_pdf_file)
         