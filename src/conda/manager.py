import subprocess
import json
from typing import List, Dict, Optional

class CondaManager:
    """Conda环境管理的核心类"""
    
    @staticmethod
    def get_environments() -> Dict:
        """获取所有conda环境"""
        result = subprocess.run(["conda", "env", "list", "--json"], 
                              capture_output=True, text=True)
        return json.loads(result.stdout)
    
    @staticmethod
    def get_python_version(env_name: str) -> str:
        """获取指定环境的Python版本"""
        try:
            result = subprocess.run(
                ["conda", "run", "-n", env_name, "python", "--version"],
                capture_output=True, text=True
            )
            return result.stdout.strip().split()[-1]
        except Exception:
            return "未知"
    
    @staticmethod
    def get_packages(env_name: str) -> List[Dict]:
        """获取指定环境的包列表"""
        result = subprocess.run(
            ["conda", "list", "--json", "-n", env_name],
            capture_output=True, text=True
        )
        return json.loads(result.stdout)
    
    @staticmethod
    def create_environment(env_name: str, python_version: str, progress_callback=None) -> None:
        """创建新的conda环境"""
        process = subprocess.Popen(
            ["conda", "create", "-n", env_name, f"python={python_version}", "-y"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # 读取输出并更新进度
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output and progress_callback:
                progress_callback()
            
        if process.returncode != 0:
            raise Exception(f"创建环境失败: {process.stderr.read()}")
    
    @staticmethod
    def delete_environment(env_name: str) -> None:
        """删除指定的conda环境"""
        subprocess.run(
            ["conda", "env", "remove", "-n", env_name, "-y"],
            check=True
        )
    
    @staticmethod
    def get_env_path(env_name: str) -> Optional[str]:
        """获取环境的路径"""
        envs_data = CondaManager.get_environments()
        for env in envs_data["envs"]:
            if env.endswith(env_name):
                return env
        return None 
    
    @staticmethod
    def get_environments_with_python_versions() -> Dict:
        """获取所有conda环境及其Python版本"""
        envs_data = CondaManager.get_environments()
        result = {"envs": []}
        
        for env in envs_data["envs"]:
            env_name = env.split("\\")[-1] if "\\" in env else env.split("/")[-1]
            if env_name:
                python_version = CondaManager.get_python_version(env_name)
                result["envs"].append({
                    "path": env,
                    "name": env_name,
                    "python_version": python_version
                })
        
        return result 