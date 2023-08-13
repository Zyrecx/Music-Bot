import wavelink

class MusicPlayer(wavelink.Player):
    def __init__(self, textchannel,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.textchannel = textchannel
        self.autoplay = True

