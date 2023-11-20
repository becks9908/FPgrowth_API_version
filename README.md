# FPgrowth_API_version
# NXP_FPGROWTH
## Description
Use fpgrowth to quickly find similar fail testing files and improve the traditional manual query method.
## Current directory
Description for each file in the directory:
- [fp_growth.py]() - Main file.
- [preprocess.py]() - 處理讀檔.
- [project_handling.py]() - 負責創建/刪除資料夾.
- [train.py]() - Train files 讀取一個project資料夾的files.
- [search.py]() - Search files.
- [ATE]() - 存放log資料夾 底下細分project name.
- [logFileForTest]() - 暫時當作inpu的欲搜尋log.
- [Result]() - (可有可無)暫時存放最終結果.
- [trainResult]() - 暫時存放training結果.
- [requirements.txt]() - Required dependencies that need to be install.

## CREATE PROJECT **
```python
# 在fp_growth.py
#############
#   CREATE  #
#############
#### if given a projectName ####

# projectName = "Project_2"  # 設定要創建的資料夾名稱
h = Handling(projectName) 
h.createProject()

```

## DELETE PROJECT **
```python
# 在fp_growth.py

###############
#    DELET    #
###############
#### if remove prejectName ####
# projectName = ("Project_XX2")
h = Handling(projectName) 
h.deleteProject()

```

## TRAIN FILES **
```python
# 在fp_growth.py

###############
#    TRAIN    #
###############
#### if use train(projectName,logFile[])  
'''
projectName = "Project_2"
'''
t = Train(projectName)
count = t.count_files()
input_dic = t.estimate_file_fail_train()
input_list = t.formulate_input(input_dic)
t.rule_mining(input_list)

df_rules = pd.read_json(t.FP_FILE)
# Estimate the score of training files.
score_cal_train = t.train_score_calculation(
    df_rules, input_dic)
```

## SEARCH FILE **
```python
# 在fp_growth.py
###############
#     TEST    #
###############
'''
#### 給指定的projectName 與 log
projectName = "Project_2"
logfile =  "logFileForTest/forTest.log"
'''

s = Search(projectName, logfile)
# Estimate fail rates of testing files
searchFile_failRate_dic = s.estimate_file_fail_test()

# Estimate the score of testing files
df_rules = pd.read_json(s.FP_FILE)
score_cal_test = s.test_score_calculation(
    df_rules, searchFile_failRate_dic)

# Estimate the similarity between the Training/Testing file
result = s.similar(score_cal_train, score_cal_test)

'''
###Result 是最後回傳10個最接近的檔案(包含路徑的list)
###result is final answer ###
print(result)
###result is final answer ###
'''

```

