from tkinter import *

color_win_bg='#483D8B'
color_btn_bg='#7B68EE'
color_light_text='#FFFFFF'
color_btn_active='#8A2BE2'

class Tl(Toplevel):
    def __init__(self,*arg, **kwarg):
        super().__init__(bg=color_win_bg,padx=7,pady=7,*arg, **kwarg)

class Fr(Frame):
    def __init__(self,*arg, **kwarg):
        super().__init__(bg=color_win_bg,padx=7,pady=7,*arg, **kwarg)

class Sc(Scale):
    def __init__(self,*arg, **kwarg):
        super().__init__(orient=HORIZONTAL,width=10,length=250,bg=color_win_bg,fg=color_light_text,
                         highlightbackground=color_win_bg,font=('Courier New',13),*arg, **kwarg)

class Butt(Button):
    def __init__(self,*arg, **kwarg):
        super().__init__(bg=color_btn_bg,fg=color_light_text,activebackground=color_btn_active,borderwidth=5,relief='ridge',
            font=('Courier New',12),*arg, **kwarg)

class Rb(Radiobutton):
    def __init__(self,*arg, **kwarg):
        super().__init__(indicatoron=0, bg=color_win_bg,fg=color_light_text,borderwidth=5,font=('Courier New',12),
                         selectcolor=color_btn_bg,activebackground=color_btn_active,*arg, **kwarg)

class Lbl (Label):
    def __init__(self, *arg, **kwarg):
        super().__init__(bg=color_win_bg,fg=color_light_text,font=('Courier New',13),pady=5,*arg, **kwarg)


info_img=[]
info_txt=['для начала нажмите левой кнопкой\nмыши на любую ячейку. ячейка\nс точкойв середине означает,\nчто вокруг неё мин точно нет',
          'открывайте ячейки до ячеек\nс цифрами. цифра показывает,\nсколько мин рядом с ячейкой в\nрадиусе одной клетки в 8 сторон',
          'если вам кажестся, что где-то мина,\nнажмите туда правой кнопкой мыши,\nлевой - на безопасные ячейки',
          'после окончания игры вам начислятся\nстолько монеток, сколько мин\nвы разминировали. вы молодец!']
for i in range (4):
    info_img.append('files\info_'+str(i)+'.gif')
page=1
def info():
    def pas():
        pass
    if 'info_win' in locals():
        info_win.destroy()
    global page
    page=1
    
    def page_turn(next=True):
        global page
        for widget in info_page.winfo_children():
            widget.destroy()
        page = page - 1 if next else page + 1
        if page==0:
            up.config(command = pas)
        else:
            up.config(command = lambda: page_turn(True))
        if page==3:
            down.config(command = info_win.destroy)
        else:
            down.config(command = lambda: page_turn(False))
        
        img=PhotoImage(file=info_img[page])
        lbl=Lbl(info_page,image=img)
        lbl.image=img
        lbl.grid()
        Lbl(info_page,text=info_txt[page]).grid()
        Butt(info_win,text=page+1).grid(row=1,column=1)

    info_win=Tl()
    info_win.resizable(False,False)
    info_page=Fr(info_win)
    info_page.grid(columnspan=3)
    up=Butt(info_win,text='пред.')
    up.grid(row=1,column=0,sticky='w')
    down=Butt(info_win,text='след.')
    down.grid(row=1,column=2,sticky='e')
    page_turn(True)
    info_win.mainloop()
