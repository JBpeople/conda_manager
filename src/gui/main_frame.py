import wx
import threading
from typing import Callable
from src.conda.manager import CondaManager
from src.system.os_operations import OSOperations
from .panels import EnvironmentListPanel, PackageListPanel
from .dialogs import CreateEnvironmentDialog, ProgressDialog


class CondaManagerFrame(wx.Frame):
    """主窗口类"""

    def __init__(self):
        super().__init__(parent=None, title="Conda Manager", size=(800, 600))
        self.conda_manager = CondaManager()
        self.init_ui()
        self.load_environments()

    def init_ui(self):
        """初始化UI"""
        self._set_icon()
        panel = wx.Panel(self)

        # 创建分割窗口
        splitter = wx.SplitterWindow(panel)

        # 创建环境列表和包列表面板
        self.env_panel = EnvironmentListPanel(splitter, self.on_env_selected, self.on_env_right_click)
        self.pkg_panel = PackageListPanel(splitter)

        # 设置分割窗口
        splitter.SplitVertically(self.env_panel, self.pkg_panel)
        splitter.SetMinimumPaneSize(200)

        # 创建工具栏
        self._create_toolbar(panel)

        # 创建布局
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.toolbar, 0, wx.EXPAND)
        sizer.Add(splitter, 1, wx.EXPAND)
        panel.SetSizer(sizer)

    def _set_icon(self):
        """设置窗口图标"""
        try:
            icon = wx.Icon("resource/icon.png", wx.BITMAP_TYPE_PNG)
            self.SetIcon(icon)
        except Exception as e:
            print(f"无法加载图标文件: {e}")

    def _create_toolbar(self, panel):
        """创建工具栏"""
        self.toolbar = wx.ToolBar(panel)

        # 添加工具栏按钮（增加tooltip）
        refresh_tool = self.toolbar.AddTool(
            wx.ID_ANY, 
            "刷新",
            wx.ArtProvider.GetBitmap(wx.ART_REDO),
            shortHelp="刷新环境列表"  # 添加tooltip
        )
        
        create_tool = self.toolbar.AddTool(
            wx.ID_ANY, 
            "新建环境",
            wx.ArtProvider.GetBitmap(wx.ART_NEW_DIR),
            shortHelp="创建新的Python环境"  # 添加tooltip
        )
        
        delete_tool = self.toolbar.AddTool(
            wx.ID_ANY, 
            "删除环境",
            wx.ArtProvider.GetBitmap(wx.ART_DELETE),
            shortHelp="删除选中的环境"  # 添加tooltip
        )
        
        self.toolbar.Realize()
        
        # 绑定工具栏事件
        self.Bind(wx.EVT_TOOL, self.on_refresh, refresh_tool)
        self.Bind(wx.EVT_TOOL, self.on_create_env, create_tool)
        self.Bind(wx.EVT_TOOL, self.on_delete_env, delete_tool)

    def run_async(self, func: Callable, callback: Callable = None):
        """异步执行函数"""

        def _async_call():
            try:
                result = func()
                if callback:
                    wx.CallAfter(callback, result)
            except Exception as e:
                wx.CallAfter(self.show_error, str(e))

        thread = threading.Thread(target=_async_call)
        thread.start()

    def load_environments(self):
        """加载环境列表"""
        self.run_async(self.conda_manager.get_environments_with_python_versions, self.env_panel.update_environments)

    def on_env_selected(self, env_name: str):
        """处理环境选择事件"""
        self.run_async(lambda: self.conda_manager.get_packages(env_name), self.pkg_panel.update_packages)

    def on_env_right_click(self, env_name: str):
        """处理环境右键点击事件"""
        menu = wx.Menu()

        open_folder = menu.Append(wx.ID_ANY, "打开环境文件夹")
        open_terminal = menu.Append(wx.ID_ANY, "在终端中打开")

        self.Bind(wx.EVT_MENU, lambda evt: self.open_env_folder(env_name), open_folder)
        self.Bind(wx.EVT_MENU, lambda evt: self.open_terminal(env_name), open_terminal)

        self.PopupMenu(menu)
        menu.Destroy()

    def open_env_folder(self, env_name: str):
        """打开环境文件夹"""
        try:
            env_path = self.conda_manager.get_env_path(env_name)
            if env_path:
                OSOperations.open_folder(env_path)
            else:
                wx.MessageBox(f"找不到环境 {env_name} 的路径", "错误")
        except Exception as e:
            self.show_error(str(e))

    def open_terminal(self, env_name: str):
        """打开终端"""
        try:
            OSOperations.open_terminal_with_conda_env(env_name)
        except Exception as e:
            self.show_error(str(e))

    def on_refresh(self, event):
        """刷新环境列表"""
        self.load_environments()

    def on_create_env(self, event):
        """创建新环境"""
        dialog = CreateEnvironmentDialog(self)
        if dialog.ShowModal() == wx.ID_OK:
            env_name = dialog.get_env_name()
            python_version = dialog.get_python_version()
            if env_name:
                self.create_environment_with_progress(env_name, python_version)
        dialog.Destroy()

    def create_environment_with_progress(self, env_name: str, python_version: str):
        """带进度显示的环境创建"""
        progress_dialog = ProgressDialog(
            self, "创建环境", f"正在创建环境 {env_name} (Python {python_version})...\n请耐心等待"
        )

        def progress_callback():
            wx.CallAfter(progress_dialog.pulse)

        def create_env():
            try:
                self.conda_manager.create_environment(env_name, python_version, progress_callback)
                wx.CallAfter(progress_dialog.EndModal, wx.ID_OK)
                wx.CallAfter(self.load_environments)
            except Exception as e:
                wx.CallAfter(progress_dialog.EndModal, wx.ID_CANCEL)
                wx.CallAfter(self.show_error, str(e))

        # 在新线程中创建环境
        thread = threading.Thread(target=create_env)
        thread.start()

        # 显示进度对话框
        progress_dialog.ShowModal()
        progress_dialog.Destroy()

    def on_delete_env(self, event):
        """删除环境"""
        env_name = self.env_panel.get_selected_env()
        if not env_name:
            wx.MessageBox("请先选择要删除的环境", "提示")
            return

        if wx.MessageBox(f"确定要删除环境 {env_name} 吗？", "确认", wx.YES_NO | wx.NO_DEFAULT) == wx.YES:
            self.run_async(lambda: self.conda_manager.delete_environment(env_name), lambda _: self.load_environments())

    def show_error(self, message: str):
        """显示错误信息"""
        wx.MessageBox(message, "错误", wx.OK | wx.ICON_ERROR)
