
from collections import OrderedDict

import pandas as pd

class IQMReport(object):
    
    '''
    Class for getting info from converted IQM txt report.    
    
    '''
    
    def __init__(self,iqm_report_txt):
        
        self.iqm_report=iqm_report_txt
    
    def get_all_lines(self):
        
        """
        Read file into a list.        
        
        """
        
        all_line_list=[]
        
        with open(self.iqm_report) as report:
            
            all_line_list=report.readlines()
            
        # remove \n 
        
        all_line_list=[each[:-1] for each in all_line_list]
            
        return (all_line_list)
    
   
    
    def get_string_index(self,key_string):
        
        """
        Get index of search string key_string        
        
        """
        
        all_line_list=self.get_all_lines()
        
        index=all_line_list.index(key_string)
        
        return(index )
    
    def get_patient_inf(self):
        
        """
        
        Return patient information         
        
        """
        
               
        patient_inf=OrderedDict()
        
        all_line_list=self.get_all_lines()
        
        patient_id_index=self.get_string_index('Patient ID')
        
            
        patient_inf['patient_name']=all_line_list[patient_id_index+3]
        
        patient_inf['mrn']=all_line_list[patient_id_index+4]
        
        #patient_inf['birth_date']=all_line_list[patient_id_index+5]
        
    
               
        return (patient_inf)
    
    def get_plan_inf(self):
        
        """
        Return plan info
        
        
        """
        
        plan_inf=OrderedDict()
               
        all_line_list=self.get_all_lines()
        
        plan_index=self.get_string_index('Plan Details')
        
            
        plan_inf['plan_name']=all_line_list[plan_index-4]
        
        plan_inf['field_ids']=all_line_list[plan_index-3]
        
        plan_inf['technique']=all_line_list[plan_index-2]
        
        plan_inf['mu_per_fraction']=all_line_list[plan_index-1]
        
              
        return (plan_inf)
 
 
    def get_overal_qa_result(self):
        
       
        
        """
        Return overal QA results.
        
        """
        
        qa_result=OrderedDict()
        
        all_line_list=self.get_all_lines()
               
        qa_index=self.get_string_index('Aggregated Signal Deviation Scores for All Sessions')
        
        qa_result['overal_result']=all_line_list[qa_index-11]
        
        qa_result['cumulative_watch_SPR']=all_line_list[qa_index-6]
        
        qa_result['segment_by_segment_watch_SPR']=all_line_list[qa_index-5]
        
        qa_result['final_cumulative_deviation']=all_line_list[qa_index-4]
        
        
        
        qa_result['cumulative_watch_SPR_pass_fail']=all_line_list[qa_index-3]
               
        qa_result['segment_by_segment_watch_SPR_pass_fail']=all_line_list[qa_index-2]
        
        qa_result['final_cumulative_deviation_pass_fail']=all_line_list[qa_index-1]
        
           
        
        return (qa_result)
    
    def get_treatment_details(self):
        
        """
        Return treatment details for patients.        
        """
        
        treatment_inf=OrderedDict()
        
        all_line_list=self.get_all_lines()
                       
        treatment_index=self.get_string_index('Treatment Details')  
        
        treatment_tmp=all_line_list[treatment_index-1].split()
        
       
        
        treatment_inf['session_number']= treatment_tmp[0]
        
        try:
            treatment_inf['machine']=treatment_tmp[5]
        
        except IndexError:
            
            pass 
        
        treatment_inf['machine_doc']=treatment_tmp[-1]
        
        return treatment_inf
     
        
    def get_field_evaluation_indices(self):
        
        """
        Return field evaluation indices
        
        """
        
        all_line_list=self.get_all_lines()
        
        field_evalution_indices=[index for (index,item) in enumerate(all_line_list) if 'Evaluation Details for Field' in item]
                                 
                                         
        return  field_evalution_indices
    
    def get_field_evaluation_list(self):
        
        """
        
        Return field evaluation sublist for all fields.
        
                
        """
        
        field_evaluation_list=[]
        
        all_line_list=self.get_all_lines()
        
        field_evalution_indices=self.get_field_evaluation_indices()
        
        for i in range(len(field_evalution_indices)):
            
            if i<len(field_evalution_indices)-1:
                
                low_index=field_evalution_indices[i]
                
                upper_index=field_evalution_indices[i+1]
                
                field_session=all_line_list[low_index:upper_index]
                
                field_evaluation_list.append(field_session)
            
            else:
                
                low_index=field_evalution_indices[i]
                field_session=all_line_list[low_index:-1]
                
                field_evaluation_list.append(field_session)
                
       
        return(field_evaluation_list)
    
    
    def get_one_field_evaluation_details(self, one_field_evaluation_list):
        
        """
        Return one field evaluation details.
        
        """
         
        one_field_evalution_result=OrderedDict()
        
             
        
        field_id=one_field_evaluation_list[0].split()[-1]
        
        one_field_evalution_result['field_id']=field_id
        
        field_name=one_field_evaluation_list[5]
        
        one_field_evalution_result['field_name']=field_name
        
        field_mu=one_field_evaluation_list[6]
        
        one_field_evalution_result['field_mu']=field_mu
        
        field_cp_number=one_field_evaluation_list[7]
        
        one_field_evalution_result['field_cp_number']=field_cp_number
        
        field_energy=one_field_evaluation_list[13]
        
        one_field_evalution_result['field_energy']=field_energy
        
        field_gantry_span=one_field_evaluation_list[14]
        
        one_field_evalution_result['field_gantry_span']=field_gantry_span
        
        
        devation_index=one_field_evaluation_list.index('Deviation [%]')
        
     
        
        total_devation=one_field_evaluation_list[devation_index+1]
        
        one_field_evalution_result['total_devation']=total_devation
        
        
        field_cumulative_watch_SPR=one_field_evaluation_list[devation_index+4]
        
        one_field_evalution_result['field_cumulative_watch_SPR']=field_cumulative_watch_SPR
        
        
        field_cumulative_action_SPR=one_field_evaluation_list[devation_index+7]
        
        one_field_evalution_result['field_cumulative_action_SPR']=field_cumulative_action_SPR
       
        field_Seg_by_Seg_watch_SPR =one_field_evaluation_list[devation_index+10]
        
        one_field_evalution_result['field_Seg_by_Seg_watch_SPR']=field_Seg_by_Seg_watch_SPR
        
        
        field_seg_by_seg_action_SPR=one_field_evaluation_list[devation_index+13]
        
        one_field_evalution_result['field_seg_by_seg_action_SPR']=field_seg_by_seg_action_SPR
        
               
        field_overal_result=one_field_evaluation_list[devation_index+16]
        
        one_field_evalution_result['field_overal_result']= field_overal_result
        
              
        return one_field_evalution_result
        
        
        
    def get_fields_evaluation_results(self):
        
        """
        
        Return all field evaluation resutls as a list.
        
        """
     
        
        fields_evluation_results=[]
        
        fields_session_list=self.get_field_evaluation_list()
        
        
        for each_field_list in fields_session_list:
            
            each_field_result=self.get_one_field_evaluation_details(each_field_list)
            
                        
            fields_evluation_results.extend([each_field_result])
            
      
                    
        return fields_evluation_results
    
    def patient_qa_results2df(self):
        
        """
        Covert patient QA resutls to dataframe.        
        
        """
         
        patient_info=self.get_patient_inf()            
            
        qa_result=self.get_overal_qa_result()
        
        treatment_inf=self.get_treatment_details()
        
        patient_info.update(treatment_inf)
        
        patient_info.update(qa_result)
        
              
        patient_qa_result_df=pd.DataFrame([patient_info.values()],columns=patient_info.keys())
        
           
        print('Sucessfully write patient qa result into dataframe for patient:' + patient_info['patient_name']+","+patient_info['mrn'])
        
          
        return(patient_qa_result_df)
        
        
    def field_qa_results2df(self):
        
        """
        convert patient field QA results to df.
        
        """
        
        field_qa_resutls_list=[]   
          
        field_qa_results=self.get_fields_evaluation_results()
       
        for each_field in field_qa_results:
            
            patient_info=self.get_patient_inf()
            
            patient_info.update(each_field)
            
            treatment_inf=self.get_treatment_details()   
            
            patient_info.update(treatment_inf)
            
            each_field_qa=patient_info
            
            field_qa_resutls_list.extend([each_field_qa])
            
            
        field_qa_results_df=pd.DataFrame([ field_qa_resutls_list[i]  for i, j in enumerate( field_qa_resutls_list)])
        
        return field_qa_results_df
        
 
        
  
        
if __name__=='__main__':
    
    # # 0 
    iqm_report_txt='C:/AitangResearch/IQMAnalyzer/testData/oneTxtReport/20210422_PatientPlanDailyReport_PatientId_1535649_PlanName_RTBREASTSIB.txt'
    
    report=IQMReport(iqm_report_txt)
    
    # # 1
    
    all_line_list=report.get_all_lines()
    
    #print(all_line_list)
    
    # # 2
    
    patient_info=report.get_patient_inf()
    
    #print(patient_info)
    
    plan_info=report.get_plan_inf()
    
    # # 3
    
    qa_inf=report.get_overal_qa_result()
    
    print(qa_inf)
    
    # # 3
    
    treatment_inf=report.get_treatment_details()
    
    # # 4 
    
    field_evaluation_indices=report.get_field_evaluation_indices()
    
    # # 5
    
    field_evalution_list=report.get_field_evaluation_list()
    
    # # 6 
    one_field_list=field_evalution_list[0]
    
    one_field_evaluation_details=report.get_one_field_evaluation_details(one_field_list)
    
    # # 7
    
    fields_evalution_results=report.get_fields_evaluation_results()
    
    # # 8 
    
    qa_result_df=report.patient_qa_results2df()
    
    # # 9
    
    field_qa_df=report.field_qa_results2df()
    
    
   
    
    
    
    
    
            
        
        
        
