"""初始化脚手架的操作"""
import os
import shutil


class InitFlaskProjectProcessor:

    def __init__(self, project_name: str) -> None:
        self.project_name = project_name

    def init(self):
        """初始化项目
           1. 判断当前目录下是否有重名的目录, 如果有则抛出异常
           2. 根据 project_name 创建目录
           3. 将 template/base 目录下的文件 copy 到 project_name 目录下
        """
        target_folder = self.project_name
        if os.path.isfile(target_folder):
            raise FileExistsError(f'当前路径下已存在 {self.project_name} 目录, 无法初始化项目')
        source_folder = os.path.join(os.path.abspath(__file__).rsplit(os.sep, 1)[0], 'template', 'base')
        shutil.copytree(source_folder, target_folder)
