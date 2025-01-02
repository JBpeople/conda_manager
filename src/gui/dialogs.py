import wx

class CreateEnvironmentDialog(wx.Dialog):
    """创建环境对话框"""
    
    def __init__(self, parent):
        super().__init__(parent, title="创建新环境", size=(300, 150))
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # 环境名称输入
        name_label = wx.StaticText(panel, label="环境名称:")
        self.name_ctrl = wx.TextCtrl(panel)
        
        # Python版本选择
        version_label = wx.StaticText(panel, label="Python版本:")
        versions = ["3.12", "3.11", "3.10", "3.9", "3.8", "3.7"]
        self.version_ctrl = wx.Choice(panel, choices=versions)
        self.version_ctrl.SetSelection(0)
        
        # 按钮
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button(panel, wx.ID_OK, "确定")
        cancel_button = wx.Button(panel, wx.ID_CANCEL, "取消")
        
        # 布局
        grid = wx.FlexGridSizer(2, 2, 5, 5)
        grid.Add(name_label, 0, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self.name_ctrl, 1, wx.EXPAND)
        grid.Add(version_label, 0, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self.version_ctrl, 1, wx.EXPAND)
        
        btn_sizer.Add(ok_button, 0, wx.ALL, 5)
        btn_sizer.Add(cancel_button, 0, wx.ALL, 5)
        
        vbox.Add(grid, 0, wx.ALL | wx.EXPAND, 10)
        vbox.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        
        panel.SetSizer(vbox)
    
    def get_env_name(self) -> str:
        """获取环境名称"""
        return self.name_ctrl.GetValue()
    
    def get_python_version(self) -> str:
        """获取选择的Python版本"""
        return self.version_ctrl.GetString(self.version_ctrl.GetSelection()) 

class ProgressDialog(wx.Dialog):
    """进度对话框"""
    def __init__(self, parent, title, message):
        super().__init__(parent, title=title, size=(300, 150))
        self.init_ui(message)
        
    def init_ui(self, message):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # 添加消息文本
        message_text = wx.StaticText(panel, label=message)
        vbox.Add(message_text, 0, wx.ALL | wx.CENTER, 10)
        
        # 添加进度条
        self.gauge = wx.Gauge(panel, range=100, size=(250, 25))
        vbox.Add(self.gauge, 0, wx.ALL | wx.EXPAND, 10)
        
        # 添加取消按钮
        self.cancel_button = wx.Button(panel, wx.ID_CANCEL, "取消")
        vbox.Add(self.cancel_button, 0, wx.ALL | wx.CENTER, 10)
        
        panel.SetSizer(vbox)
        
    def update_progress(self, value: int):
        """更新进度条"""
        self.gauge.SetValue(value)
        
    def pulse(self):
        """进度条脉冲动画"""
        self.gauge.Pulse() 