import wx
from gui.main_frame import CondaManagerFrame

def main():
    app = wx.App()
    frame = CondaManagerFrame()
    frame.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()
