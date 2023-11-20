import json
import os
from preprocess import Preprocess
import pandas as pd
from scipy import spatial


class Search():
    
    def __init__(self, projectName, logFile):
        self.projectName = projectName  # the minimum times of fail
        self.log_folder = "ATE"
        self.log_path = os.path.join(self.log_folder, self.projectName)
        self.file_paths = []
        self.count = 0
        self.MIN_TIMES = 2
        self.K = 20
        self.logfile = logFile

        self.result_path = 'trainResult'
        self.topM= 10
        self.FP_FILE = os.path.join(self.result_path, f"{self.projectName}_ranking.json")
        self.pullTrainFile()
        
        
    def estimate_file_fail_test(self):
        '''
        Estimate the file rate of training files.
        '''
        print("\n##############  1. Estimate Training File Fail Rate Process ##############\n")

        train_fail_rate_result_file = os.path.join(self.result_path, f"{self.projectName}_Search_failRate.json")

        # # if the training files have not been estimated before
        # if not os.path.isfile(train_fail_rate_result_file):
        searchFile_failRate_dic = {}
            
        # cur_path = DATA_PATH + cur_file
        print(" Estimating training file "  +
            self.logfile + " ")

        # estimate the fail rate of each training file
        p = Preprocess(
            file_name=self.logfile,
            min_times=self.MIN_TIMES)

        train_fail_rate_dic = p.process_file()
       
        searchFile_failRate_dic[self.logfile] = train_fail_rate_dic

        # write file
        json.dump(searchFile_failRate_dic, open(
            train_fail_rate_result_file, "w"))

        return searchFile_failRate_dic


    def test_score_calculation(self,df_filter_rules, fail_result_dic):
        '''
        Estimate the score of testing files.
        '''

        print("\n##############  6. Estimate the score of testing files  ###################")
        test_file_score_dic = {}
        
        self.logfile
    
        scoreList = []
        for j in range(self.K):
            score = 1
            for i in range(len(df_filter_rules['itemsets'][j])):
                tmp = df_filter_rules['itemsets'][j][i]
                if fail_result_dic.get(self.logfile).get(tmp) is not None:
                    score *= fail_result_dic.get(self.logfile).get(tmp)
                else:
                    score = 0.0
            scoreList.append(score)
        test_file_score_dic[self.logfile] = scoreList
  
        print("\n  Estimation testing score Finished.  ")

        return test_file_score_dic

    def pullTrainFile(self):
        distinct_files = set()  # use set to varify distinct
        if os.path.exists(self.log_path) and os.path.isdir(self.log_path):
            files = os.listdir(self.log_path)
            
            sorted_files = sorted(files, key=lambda x: int(x.split('_')[1]) if x.startswith('generated_') else -1)
            for file in sorted_files:
                if file.startswith('.'):
                    continue  

                file_path = os.path.join(self.log_path, file)
                if os.path.isfile(file_path):
                    if file not in distinct_files:
                    # if not in set, then add it
                        self.file_paths.append(file_path)
                        distinct_files.add(file)
                        self.count += 1
            
    
    def similar(self, score_file_score_dic, test_file_score_dic):
        '''
        Similarity comparison and ranking.
        '''

        print("\n##############  7. Estimate the similarity between the Training/Testing file #####################")
        training_file_score = score_file_score_dic
        totalRanking_dic = {}
        
        dataSetI = test_file_score_dic.get(self.logfile)
        rankingList = {}
        for p in range(self.count):
            train_file = self.file_paths[p]
            dataSetII = training_file_score.get(train_file)
            result = 1 - spatial.distance.cosine(dataSetI, dataSetII)
            rankingList[train_file] = result
        afterRanking = dict(sorted(rankingList.items(),
                                key=lambda item: item[1], reverse=True))
        TopMRanking = dict(list(afterRanking.items())[:self.topM])
        keys_only = list(TopMRanking.keys())

        totalRanking_dic[self.logfile] = afterRanking

        jsonFile = open("Result/rankingResult.json", "w")
        jsonFile.write(json.dumps(totalRanking_dic, indent=2))
        jsonFile.close()
        print("\n  Estimation of similarity finished. \n ")
        
        return keys_only
