import pandas as pd

psqa_paitient_list=r'C:\AitangResearch\IQMAnalyzer\testData\xls\PSQA_patient_list_combined_results.xls'


psqa_df=pd.read_excel(psqa_paitient_list)

iqm_patient_list=r'C:\AitangResearch\IQMAnalyzer\testData\xls\IQM_patientQA_combined_results.xls'

iqm_df=pd.read_excel(iqm_patient_list)


#merged_df=psqa_df.merge(iqm_df,how='left',on='mrn')

#merged_df.to_excel('test2.xls')

merged_iqm_psqa=iqm_df.merge(psqa_df,how='left',on='mrn')

merged_iqm_psqa.to_excel('iqm_psqa.xls')