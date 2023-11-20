import json
import os
from preprocess import Preprocess
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth
import pandas as pd


class Train():
    
    def __init__(self, projectName):
        self.projectName = projectName  # the minimum times of fail
        self.log_folder = "ATE"
        self.log_path = os.path.join(self.log_folder, self.projectName)
        
        ### build a train result dir ###
        self.result_path = 'trainResult'
        if not os.path.isdir(self.result_path):
            os.makedirs(self.result_path)

        self.FP_FILE = os.path.join(self.result_path, f"{self.projectName}_ranking.json")

        self.count = 0
        self.file_paths = [] 
        self.MIN_TIMES = 1
        self.MIN_SUPPORT = 0.1
        self.MAX_LEN = 20
        self.MIN_LEN = 1
        self.K=20
        
    def count_files(self):
        # Count the total number of files and list their paths.
        print(f"############## Counting and Listing Files in '{self.projectName}' ##############\n")
        distinct_files = set()  
        if os.path.exists(self.log_path) and os.path.isdir(self.log_path):
      
            files = os.listdir(self.log_path)
            sorted_files = sorted(files, key=lambda x: int(x.split('_')[1]) if x.startswith('generated_') else -1)

            for file in sorted_files:
                if file.startswith('.'):
                    continue  

                file_path = os.path.join(self.log_path, file)
                if os.path.isfile(file_path):
                    if file not in distinct_files:
                        self.file_paths.append(file_path)
                        distinct_files.add(file)
                        self.count += 1
                        
            print(f"Total {self.count} files")
            
        else:
            print(f"'{self.projectName}' not exist")
        
        return self.count

    def estimate_file_fail_train(self):
        '''
        Estimate the file rate of training files.
        '''
        print("\n##############  1. Estimate Training File Fail Rate Process ##############\n")

        train_fail_rate_result_file = os.path.join(self.result_path, f"{self.projectName}_failRate.json")

        all_train_fail_rate_result_file_dic = {}
            
        for a in range(self.count): 
            cur_file = self.file_paths[a]
           
            p = Preprocess(
                file_name=cur_file,
                min_times=self.MIN_TIMES)

            train_fail_rate_dic = p.process_file()

            all_train_fail_rate_result_file_dic[cur_file] = train_fail_rate_dic

        # write file
        json.dump(all_train_fail_rate_result_file_dic, open(
            train_fail_rate_result_file, "w"))

        return all_train_fail_rate_result_file_dic


    def formulate_input(self,dic):
        '''
        Formulate fail rate dictionary to the input of the algorithm.
        '''
        print("\n##############  2. Input the dataset formula  ############################")
        input_dataset = []

        for file in list(dic):
            input_dataset.append(list(dic[file]))
        print("\n  Dataset formula process finished.  ")

        return input_dataset


    def rule_mining(self,dataset):
        '''
        Implement fp-growth.
        '''
        print("\n##############  3. Implement FP-growth process  ##########################")
        te = TransactionEncoder()
        te_ary = te.fit(dataset).transform(dataset)
        df = pd.DataFrame(te_ary, columns=te.columns_)

        df_rules = fpgrowth(df, min_support=self.MIN_SUPPORT,
                            max_len=self.MAX_LEN, use_colnames=True)
        # sorted by support values
        df_rules = df_rules.sort_values(by='support', ascending=False)
        # create new df
        df_filter_rules = pd.DataFrame(columns=['support', 'itemsets'])

        # filer with the minimum length
        for index, row in df_rules.iterrows():
            if len(df_filter_rules.index) < self.K and len(list(row['itemsets'])) >= self.MIN_LEN:
                df_filter_rules.loc[len(df_filter_rules.index)] = \
                    [row['support'], list(row['itemsets'])]
        print("\n  FP-growth process finished.  ")
        
        df_filter_rules.to_json(self.FP_FILE)


    def train_score_calculation(self, df_filter_rules, fail_result_dic):
        '''
        Estimate the score of training files.
        '''
        print("\n##############  4. Estimate the score of training files  ##################")

        training_file_score_dic = {}
        for r in range(self.count):
            cur_file = self.file_paths[r]
            #print(cur_file)
            scoreList = []
            
            for j in range(self.K):
                score = 1
                for i in range(len(df_filter_rules['itemsets'][j])):
                    tmp = df_filter_rules['itemsets'][j][i]
                    if fail_result_dic.get(cur_file).get(tmp) is not None:
                        score *= fail_result_dic.get(cur_file).get(tmp)
                    else:
                        score = 0.0
                scoreList.append(score)
            training_file_score_dic[cur_file] = scoreList
        print("\n  Estimation training score Finished.  ")
      
        return training_file_score_dic

