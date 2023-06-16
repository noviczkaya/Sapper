from tkinter import *
from saper_support import *
from random import randint

def start():
    global btn_list,kol_cell_now
    btn_list=[]
    gamewindow.grid_forget()
    for widget in gamewindow.winfo_children():
        widget.destroy()
    gamewindow.grid(row=3)
    gamewindow.config(height=10)
    option.grid(row=2)
 

def level_set(level_var):
    global size1,size2,mine_kol
    if level_var==3:
        opt.grid(row=6)
    else:
        opt.grid_forget()
        if level_var==0:
            size1,size2,mine_kol=9,9,10
        elif level_var==1:
            size1,size2,mine_kol=16,16,40
        elif level_var==2:
            size1,size2,mine_kol=20,30,85

def new_game_field(index=-1,first_press=True):
    global size1,size2,mine_kol
    def random_mine(size1,size2,mine_kol,index):
        mine_index_list=[]
        no_mine=[index]
        no_mine.append(index-1) if index%size2!=0 else () #left
        no_mine.append(index+1) if (index+1)%size2!=0 else () #right
        no_mine.append((index)-size2) if index>=size2 else () #top
        no_mine.append((index)+size2) if index<(size1*size2-size2) else () #bottom
        no_mine.append((index)-size2-1) if (index%size2!=0 and index>=size2) else () #left top
        no_mine.append((index)-size2+1) if ((index+1)%size2!=0 and index>=size2) else () #right top
        no_mine.append((index)+size2-1) if (index%size2!=0 and index<(size1*size2-size2)) else () #left bottom
        no_mine.append((index)+size2+1) if ((index+1)%size2!=0 and index<(size1*size2-size2)) else () #left bottom
        for i in range(mine_kol):
            while True:
                x=randint(0,(size1*size2)-1)
                if ((x not in mine_index_list) and x not in no_mine):
                    mine_index_list.append(x)
                    break
        return mine_index_list
    
    def insert_cell(size1,size2,first_press):
        global btn_list
        cell_index=0
        for i in range (size1):
            for j in range (size2):
                btn=Cell()
                btn.grid(row=i,column=j)
                btn.index=cell_index
                cell_index+=1
                if first_press:
                    btn_list.append(btn)
                    if btn.index in mine_index_list:
                        btn.mine_on=True
                else:
                    btn.first=True
    if first_press:
        mine_index_list=random_mine(size1,size2,mine_kol,index=index)
        for widget in gamewindow.winfo_children():
            widget.destroy()
        insert_cell(size1,size2,True)
        btn_list[index].open()
            
    else:
        global kol_cell_now,kol_mine_now
        option.grid_forget()
        insert_cell(size1,size2,False)
        gameopt.grid(row=5)
        kol_cell_now=(size1*size2)-mine_kol
        kol_mine_now=mine_kol
        kol_mine.config(text=f'Осталость мин: {kol_mine_now}')
        kol_cell.config(text=f'Нужно открыть ячеек: {kol_cell_now}')

def show_info(text1,text2,text3):
    info=Tl()
    info.title(text1)
    Lbl(info,text=text2).grid()
    Butt(info,text=text3,command=lambda: info.destroy()).grid()
    
def ask_ok_cancel(text1,text2):
    info=Tl()
    info.title(text1)
    Lbl(info,text=text2).grid(row=0,columnspan=2)
    yes=Butt(info,text='да')
    yes.grid(row=1,column=0)
    Butt(info,text='нет',command = lambda: info.destroy()).grid(row=1,column=1)
    return yes,info

def help_press():
    def func():
        global help_btn,money
        info.destroy()
        if money<5:
            show_info('ОТМЕНА','У вас не хватает монет!','понятно')     
        else:
            money-=5
            money_lbl.config(text=f'Монеток: {money}')
            help_btn=True
    yes,info=ask_ok_cancel("Открыть ячейку","Потратить 5 монет\nчтобы открыть ячейку?")
    yes.config(command = func)

def game_end(mine):
    global money
    money+=mine
    money_lbl.config(text=f'Монеток: {money}')
    file=open('files\money.txt','w')
    file.write(str(money))
    file.close()
    replay=Butt(gamewindow,text='ИГРАТЬ СНОВА',command=start)
    replay.grid(columnspan=size2)

def game_lose(quest=False):
    def func():
        gameopt.grid_forget()
        if quest:
            info.destroy()
        mine_kol_1=0
        for btn in btn_list:
            if btn.mine_on==True:
                btn.Photo=pixil_lose
                btn.config(image=btn.Photo)
                if btn.clicked==True:
                    mine_kol_1+=1
        show_info('Блин..',f'Вы проиграли!\nВы получаете +{mine_kol_1} монеток','жаль(')
        game_end(mine_kol_1)

    if quest:
         yes,info=ask_ok_cancel("Сдаётесь","Вы точно хотите сдаться?")
         yes.config(command=func)
    else:
        func()
    
def game_win():
    gameopt.grid_forget()
    for btn in btn_list:
        if btn.mine_on==True:
            btn.Photo=pixil_win
            btn.config(image=btn.Photo)
    show_info('УРАААА',f'Вы выиграли!\nВы получаете +{mine_kol} монеток','класс!')
    game_end(mine_kol)

class Cell(Button):

    def __init__(self):
        self.Photo=pixil_none
        super().__init__(master=gamewindow,width=20, height=20,image=self.Photo)
        self.state=NORMAL
        self.clicked=False
        self.first=False
        self.mine_on=False
        self.index=-1
        self.bind('<Button-3>', self.r_click)
        self.bind('<Button-1>', self.open)

    def btn_rank(self):
        global size1,size2,btn_list
        stand_next_index=[]
        self.rank=0
        ind=self.index
        l_free=r_free=False
        if ind%size2!=0:
            stand_next_index.append(btn_list[(ind)-1])
            l_free=True
        if (ind+1)%size2!=0:
            stand_next_index.append(btn_list[(ind)+1])
            r_free=True
        if ind>=size2:
            stand_next_index.append(btn_list[(ind)-size2])
            if l_free==True:
                stand_next_index.append(btn_list[(self.index)-size2-1])
            if r_free==True:
                stand_next_index.append(btn_list[(self.index)-size2+1])
        if ind<(size1*size2-size2):
            stand_next_index.append(btn_list[(ind)+size2])
            if l_free==True:
                stand_next_index.append(btn_list[(self.index)+size2-1])
            if r_free==True:
                stand_next_index.append(btn_list[(self.index)+size2+1])

        self.rank=0
        for i in stand_next_index:
            if i.mine_on==True:
                self.rank+=1
        '''if self.rank==0:
            stand_next_index[0].open()
        if self.rank==0:
            for i in stand_next_index:
                i.open()'''

    def r_click(self,*arg,**kwarg):
        global kol_mine_now
        if self.clicked==False:
            self.Photo=pixil_maybe
            self.config(image=self.Photo)
            self.clicked=True
            kol_mine_now-=1
        else:
            self.Photo=pixil_none
            self.config(image=self.Photo)
            self.clicked=False
            kol_mine_now+=1
        kol_mine.config(text=f'Осталось мин: {kol_mine_now}')

    def open(self,*arg,**kwarg):
        global kol_cell_now,help_btn
        if self.first==True:
            new_game_field(index=self.index)
        elif self.state!=DISABLED:
                if self.mine_on==True:
                    if help_btn==True:
                        self.r_click()
                        help_btn=False
                    else:
                        game_lose()
                else:
                    if help_btn==True:
                        help_btn=False
                    self.btn_rank()
                    self.Photo=pixil_rank_list[self.rank]
                    self.config(image=self.Photo)
                    kol_cell_now-=1
                    kol_cell.config(text=f'Нужно открыть ячеек: {kol_cell_now}')
                    self.state=DISABLED
        if kol_cell_now==0:
            game_win()


root=Tk()

pixil_maybe=PhotoImage(file="files\pixil_maybe.png")
pixil_none=PhotoImage(file="files\pixil_none.png")
pixil_win=PhotoImage(file="files\pixil_win.png")
pixil_lose=PhotoImage(file="files\pixil_lose.png")
pixil_rank_list=[]
for i in range (10):
    file_name='files\pixil_'+str(i)+'.png'
    pixil_rank_list.append(PhotoImage(file=file_name))

root.resizable(False,False)
root.title('САПЁР')
root.iconphoto(True,PhotoImage(file='files\pixil_icon.png'))
root.configure(bg=color_win_bg)

file=open('files\money.txt','r')
money=int(file.read())
file.close()
money_lbl=Lbl(text=f'Монеток: {money}')
money_lbl.grid(row=1)

option=Fr(master=root)

opt=Fr(option)
gamewindow=Fr(master=root)

def change_size1(*arg):
    global size1
    size1=int(var1.get())
def change_size2(*arg):
    global size2
    size2=int(var2.get())
def change_mine_kol(*arg):
    global mine_kol
    mine_kol=int(var3.get())

var1=IntVar(value=9)
Sc(opt,from_=9, to=20,variable=var1,tickinterval=11,command=change_size1, label='Выберите высоту поля').grid(row=0)
var2=IntVar(value=9)
Sc(opt,from_=9, to=30,variable=var2,tickinterval=21,command=change_size2,label='Выберите ширину поля').grid(row=1)

def mine_choise():
    global sc_mine
    sc_mine.destroy()
    sc_mine=Sc(opt, from_=10, to=(size1*size2)//3,variable=var3,command=change_mine_kol)
    sc_mine.grid(row=3)
var3=IntVar(value=10)
size1,size2,mine_kol=var1.get(),var2.get(),var3.get()
sc_mine=Sc()
Butt(opt,text='Выбрать количество мин',command=mine_choise).grid(row=2)
size1,size2,mine_kol=9,9,10

level_var=IntVar()
level_var.set(0)

level_list=['ЛЁГКАЯ ИГРА (9*9)','СРЕДНЯЯ ИГРА (40*40)','СЛОЖНАЯ ИГРА (24*30)','НАСТРОИТЬ']
for i in range(4):
    Rb(option,text=level_list[i],variable=level_var,value=i,command=lambda: level_set(level_var.get())).grid(row=i+2,sticky='we')
Lbl(option).grid(row=7)
start_btn=Butt(option,text='НАЧАТЬ ИГРУ',command=lambda: new_game_field(first_press=False))
start_btn.grid(row=8,sticky='we')
kol_cell_now=(size1*size2)-mine_kol
kol_mine_now=mine_kol

gameopt=Fr(master=root,width=30)
btn_list=[]
start()

kol_mine=Lbl(gameopt)
kol_mine.grid(row=0,columnspan=2,sticky='we')

kol_cell=Lbl(gameopt)
kol_cell.grid(row=1,columnspan=2,sticky='we')

help_btn=False
Butt(gameopt,text='ОТКРЫТЬ ЯЧЕЙКУ',width=15,command=help_press).grid(row=2,column=0)
Butt(gameopt,text='СДАТЬСЯ',width=15,command=lambda: game_lose(quest=True)).grid(row=2,column=1)

Butt(text='КАК ИГРАТЬ?',command=info).grid(row=6)

root.mainloop()