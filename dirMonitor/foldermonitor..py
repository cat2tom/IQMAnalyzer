import os

import sys

import shutil

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler



current_file_dir = os.path.dirname(os.path.abspath(__file__))

sys.path.append(current_file_dir)

sys.path.append('C:/AitangResearch/IQMAnalyzer')


from dirSearch.iqmfolder import write_qa_results2csv,patient_subfolder2csv,is_patient_iqm_delivered




class Watcher:
    
    DIRECTORY_TO_WATCH = "V:/CTC-LiverpoolOncology/temp/AX/iqmDir"
    
    #DIRECTORY_TO_WATCH = "A:/"
    
    DIRECTORY_TO_WATCH = "V:/CTC-LiverpoolOncology/temp/AX/testDir"

    def __init__(self):
     
        self.observer = Observer()

    def run(self):
        
        event_handler = Handler()
        
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        
        self.observer.start()
        
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print "Error"

        self.observer.join()


class Handler(FileSystemEventHandler):
    
    """
    Monitor the folder to write resuts into csv file for one patient in the same folder.
    
    """
    
  
    @staticmethod
    def on_any_event(event):
      
        if event.event_type == 'created':
            
            if event.is_directory:
                
                new_iqm_patient_folder=event.src_path
                
                is_delivered=is_patient_iqm_delivered(new_iqm_patient_folder)
                
                if is_delivered:
                
                    write_qa_results2csv(new_iqm_patient_folder, new_iqm_patient_folder)
                    
                    print("Write patient QA results into "+new_iqm_patient_folder)
                    
                else:
                    
                    print('IQM was not delivered for folder: ' + new_iqm_patient_folder)
                   

     
if __name__ == '__main__':
    
    
    
    w = Watcher( )
    
    w.run()