#! /usr/bin/env python
import wx
import wx.media
import wx.lib.mixins.inspection

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyUI(None)
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True
    
    def win(self, role):
        return self.frame.updateScore(role)

# class MyPanel(wx.Panel):
class MyUI(wx.Frame):
    STATUS = {"start": 0, "end": 1}
    ROLE = {"left": "defend", "right": "terror"}

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="Test", pos=(-1, -1), size=(500, 500))

        self.full = False
        self.right_score = 0
        self.left_score = 0

        # self.mp = wx.media.MediaCtrl(self, size=wx.Size(512,384), szBackend=wx.media.MEDIABACKEND_DIRECTSHOW)
        # self.mp.Load("./defend1.mp4")
        # self.mp.Bind(wx.media.EVT_MEDIA_LOADED,self.OnPlay)   
        self.main_screen_panel = wx.Panel(self, -1)

        score_font = wx.Font(50, wx.FONTFAMILY_SWISS, wx.NORMAL, wx.FONTWEIGHT_BOLD)
        button_font = wx.Font(40, wx.FONTFAMILY_SWISS, wx.NORMAL, wx.FONTWEIGHT_BOLD)

        self.media_control = wx.media.MediaCtrl(self.main_screen_panel, style=wx.SIMPLE_BORDER)
        
        self.leftStartMedia = wx.media.MediaCtrl(self.main_screen_panel, style=wx.SIMPLE_BORDER)
        self.rightStartMedia = wx.media.MediaCtrl(self.main_screen_panel, style=wx.SIMPLE_BORDER)

        self.left_score_text = wx.StaticText(self.main_screen_panel, label="0")
        self.right_score_text = wx.StaticText(self.main_screen_panel, label="0")
        self.left_score_text.SetFont(score_font)
        self.right_score_text.SetFont(score_font)
        white = (255, 255, 255)
        black = (0, 0, 0)
        self.left_score_text.SetForegroundColour(black)
        self.right_score_text.SetForegroundColour(black)

        self._do_layout()

        # self.button = wx.Button(self, label="START")
        # self.button.SetFont(button_font)

        # self.Bind(wx.EVT_BUTTON, self.OnClick, self.button)
        # self.media_control.Bind(wx.media.EVT_MEDIA_LOADED, self.afterLoad)
        self.media_control.Bind(wx.media.EVT_MEDIA_FINISHED, self.init_game)

        self.leftStartMedia.Bind(wx.media.EVT_MEDIA_FINISHED, self.start_real_game)
        self.rightStartMedia.Bind(wx.media.EVT_MEDIA_FINISHED, self.start_left_video)

        self.media_control.SetBackgroundColour(wx.WHITE)
        self.leftStartMedia.SetBackgroundColour(wx.WHITE)
        self.rightStartMedia.SetBackgroundColour(wx.WHITE)

        left_video_path = f"./video/{MyUI.ROLE["left"]}{MyUI.STATUS["start"]+1}.mp4"
        right_video_path = f"./video/{MyUI.ROLE["left"]}{MyUI.STATUS["start"]+1}.mp4"

        
        if not self.leftStartMedia.Load(left_video_path):
            print("Media Load Failed")
            return self.quit(None)
        if not self.rightStartMedia.Load(right_video_path):
            print("Media Load Failed")
            return self.quit(None)
        
        self.init_game()
    
    def _do_layout(self):
        # self.toggleFullScreen()
        # self.SetBackgroundColour('black')
        # self.p = wx.Panel(self, -1)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)

        sizer_1.Add(sizer_2, 1, wx.CENTER, border=20)
        sizer_1.Add(sizer_3, 5, wx.CENTER, border=20)

        sizer_2.Add(self.left_score_text, 0, flag=wx.ALIGN_TOP, border=2)
        sizer_2.Add(self.right_score_text, 0, flag=wx.ALIGN_BOTTOM, border=2)

        sizer_3.Add(self.rightStartMedia, 1, wx.EXPAND, 0)
        sizer_3.Add(self.leftStartMedia, 1, wx.EXPAND, 0)
        sizer_3.Add(self.media_control, 1, wx.EXPAND, 0)

        self.main_screen_panel.SetSizer(sizer_1)
        self.Layout()

    def start_real_game(self, e):
        self.leftStartMedia.HideWithEffect()

    def start_left_video(self, e):
        self.rightStartMedia.HideWithEffect()
        self.leftStartMedia.ShowWithEffect()
        self.leftStartMedia.Play()

    def updateUI(self):
        self.right_score_text.SetLabel(str(self.right_score))
        self.left_score_text.SetLabel(str(self.left_score))
    
    def init_game(self, e=None):
        self.media_control.HideWithEffect()
        self.right_score = 0
        self.left_score = 0
        self.updateUI()

        self.rightStartMedia.ShowWithEffect()
        self.rightStartMedia.Play()
    
    # winner is defend or terror
    # if game is over => True
    # yet over => False
    def updateScore(self, winner):
        if MyUI.ROLE["left"] == winner:
            self.left_score += 1
        elif MyUI.ROLE["right"] == winner:
            self.right_score += 1
        
        self.updateUI()
        
        if self.left_score + self.right_score == 3:
            self.game_ending()
            return True
        return False
    
    def game_ending(self):
        isLeftWin = self.left_score > self.right_score

        if isLeftWin:
            to_play_video = f"./video/{MyUI.ROLE['left']}{MyUI.STATUS["end"]+1}.mp4"
        elif not isLeftWin:
            to_play_video = f"./video/{MyUI.ROLE['right']}{MyUI.STATUS["end"]+1}.mp4"

        self.playMedia(to_play_video)

    def playMedia(self, filepath):
        if not self.media_control.Load(filepath):
            print("Media Load Failed")
            return self.quit(None)
        
        self.ShowWithEffect()
        self.media_control.Play()
    
    def toggleFullScreen(self):
        self.full = not self.full
        self.ShowFullScreen(self.full, wx.FULLSCREEN_ALL)
    
    def quit(self, event):
        # self.Destroy()
        pass

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()