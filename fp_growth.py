import pandas as pd
import json
import os.path
from project_handling import Handling  
from train import Train
from search import Search

def main():
    
    
    #############
    #   CREATE  #
    #############
    #### if given a projectName ####
    '''
    # projectName = "Project_2"  # 設定要創建的資料夾名稱
    h = Handling(projectName) 
    h.createProject()
    '''
    ###############
    #    DELET    #
    ###############
    #### if remove prejectName ####
    '''
    # projectName = ("Project_XX2")
    h = Handling(projectName) 
    h.deleteProject()
    '''
    
    ###############
    #    TRAIN    #
    ###############
    #### if use train(projectName,logFile[])  
    projectName = "Project_2"
    t = Train(projectName)
    count = t.count_files()
    input_dic = t.estimate_file_fail_train()
    input_list = t.formulate_input(input_dic)
    t.rule_mining(input_list)
   
    df_rules = pd.read_json(t.FP_FILE)
    # Estimate the score of training files.
    score_cal_train = t.train_score_calculation(
        df_rules, input_dic)
    
    ###############
    #     TEST    #
    ###############
    projectName = "Project_2"
    logfile =  "logFileForTest/forTest.log"
    s = Search(projectName, logfile)
    # Estimate fail rates of testing files
    searchFile_failRate_dic = s.estimate_file_fail_test()
    
    # Estimate the score of testing files
    df_rules = pd.read_json(s.FP_FILE)
    score_cal_test = s.test_score_calculation(
        df_rules, searchFile_failRate_dic)

    # Estimate the similarity between the Training/Testing file
    result = s.similar(score_cal_train, score_cal_test)
    print(result)
    


if __name__ == "__main__":
    main()
