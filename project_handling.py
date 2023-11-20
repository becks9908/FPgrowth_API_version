import os

class Handling():
    def __init__(self, projectName):
        self.base_folder = 'ATE/'
        self.projectName = projectName  # the minimum times of fail

    def createProject(self):
        # 設定資料夾路徑
        create_project_folder = os.path.join(self.base_folder, self.projectName)
        # 檢查資料夾是否存在
        if not os.path.exists(create_project_folder):
            # 如果資料夾不存在，則創建它
            os.makedirs(create_project_folder)
            print(f"已成功創建 '{self.projectName}' 資料夾")
        else:
            print(f"'{self.projectName}' 專案已存在")
    
    def deleteProject(self):
        delete_project_folder = os.path.join(self.base_folder, self.projectName)
        try:
            # 確保要刪除的資料夾存在
            if os.path.exists(delete_project_folder):
                # 使用os.rmdir()刪除資料夾
                os.rmdir(delete_project_folder)
                print(f"成功刪除資料夾 '{self.projectName}'")
            else:
                print(f"資料夾 '{self.projectName}' 不存在")
        except Exception as e:
            print(f"刪除資料夾 '{self.projectName}' 時發生錯誤：{str(e)}")
