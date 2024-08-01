from dirSearch.iqmfolder import write_qa_results2csv,patient_subfolder2csv


# Prepare the dirs. 

iqm_folder="C:\\AitangResearch\\IQMAnalyzer\\testData\\iqmDir"

export_dir="C:\\AitangResearch\\IQMAnalyzer\\testData\\csv"


#iqm_folder="V:\\CTC-LiverpoolOncology\\temp\\AX\\iqmDir"

#export_dir="V:\\CTC-LiverpoolOncology\\temp\\AX\\csv"

iqm_folder=r"V:\CTC-LiverpoolOncology\temp\IQMReport\2021-05-25_06-00-01-AppServer-LVRHCTC-MAS002\reports"

export_dir=iqm_folder


# call main function to do the job.

write_qa_results2csv(iqm_folder, export_dir)

# write patient delivery status into excel.

patient_subfolder2csv(iqm_folder,export_dir)


