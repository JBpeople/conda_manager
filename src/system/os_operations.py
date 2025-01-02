import os
import platform
import subprocess
from typing import List

class OSOperations:
    """操作系统相关操作的类"""
    
    @staticmethod
    def open_folder(path: str) -> None:
        """打开文件夹"""
        if platform.system() == "Windows":
            subprocess.run(["explorer", path])
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", path])
        else:  # Linux
            subprocess.run(["xdg-open", path])
    
    @staticmethod
    def open_terminal_with_conda_env(env_name: str) -> None:
        """打开终端并激活conda环境"""
        if platform.system() == "Windows":
            activate_command = f"conda activate {env_name} && cmd /k"
            subprocess.Popen(["cmd", "/k", activate_command])
        else:
            script_path = OSOperations._create_conda_activation_script(env_name)
            OSOperations._open_terminal_with_script(script_path)
    
    @staticmethod
    def _create_conda_activation_script(env_name: str) -> str:
        """创建conda环境激活脚本"""
        script_content = f'''#!/bin/bash
        eval "$(conda shell.bash hook)"
        conda activate {env_name}
        exec bash
        '''
        script_path = os.path.expanduser("~/.conda_activate_temp.sh")
        with open(script_path, "w") as f:
            f.write(script_content)
        os.chmod(script_path, 0o755)
        return script_path
    
    @staticmethod
    def _open_terminal_with_script(script_path: str) -> None:
        """使用脚本打开终端"""
        if platform.system() == "Darwin":
            subprocess.run(["open", "-a", "Terminal", script_path])
        else:
            terminals = ["gnome-terminal", "xterm", "konsole"]
            for terminal in terminals:
                try:
                    subprocess.run([terminal, "-e", script_path])
                    break
                except FileNotFoundError:
                    continue 