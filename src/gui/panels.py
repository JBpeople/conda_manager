import wx
from typing import Callable, Dict, List

class EnvironmentListPanel(wx.ListCtrl):
    """环境列表面板"""
    
    def __init__(self, parent, on_select: Callable, on_right_click: Callable):
        super().__init__(parent, style=wx.LC_REPORT)
        self.on_select = on_select
        self.on_right_click = on_right_click
        
        self.InsertColumn(0, "环境名称", width=150)
        self.InsertColumn(1, "Python版本", width=100)
        
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self._on_item_selected)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self._on_item_right_click)
    
    def update_environments(self, envs_data: Dict):
        """更新环境列表"""
        self.DeleteAllItems()
        for env in envs_data["envs"]:
            index = self.GetItemCount()
            self.InsertItem(index, env["name"])
            self.SetItem(index, 1, env["python_version"])
    
    def get_selected_env(self) -> str:
        """获取选中的环境名称"""
        selected = self.GetFirstSelected()
        if selected != -1:
            return self.GetItem(selected, 0).GetText()
        return ""
    
    def _on_item_selected(self, event):
        """处理项目选择事件"""
        env_name = self.GetItem(event.GetIndex(), 0).GetText()
        self.on_select(env_name)
    
    def _on_item_right_click(self, event):
        """处理右键点击事件"""
        env_name = self.GetItem(event.GetIndex(), 0).GetText()
        self.on_right_click(env_name)

class PackageListPanel(wx.ListCtrl):
    """包列表面板"""
    
    def __init__(self, parent):
        super().__init__(parent, style=wx.LC_REPORT)
        
        self.InsertColumn(0, "包名称", width=200)
        self.InsertColumn(1, "版本", width=100)
    
    def update_packages(self, packages: List[Dict]):
        """更新包列表"""
        self.DeleteAllItems()
        for pkg in packages:
            index = self.GetItemCount()
            self.InsertItem(index, pkg["name"])
            self.SetItem(index, 1, pkg["version"]) 