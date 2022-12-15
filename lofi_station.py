from dataclasses import replace
from tkinter import *
import pygame 
from tkinter import filedialog
import os
#import playsound 

janela = Tk()
janela.title("lofi-station")
janela.resizable(0,0)
janela.geometry("500x500")
janela.configure(bg='black')
currentdir = os.path.dirname(__file__)
background = PhotoImage(file='./gui/backg1.gif')
janela.option_add('*tearOff',FALSE)


#configurações do fundo
bglabel = Label(janela, image=background)
bglabel.place(x=0, y=0)

#seletor de musica
caixa_seletora = Listbox(janela, bg='black',fg='green', width=33, height=15, 
selectbackground='black', selectforeground='gray')
caixa_seletora.place(x=114, y=60)

#funções

#Adicionar música 
def add_song(): 
    song = filedialog.askopenfilename(initialdir='/home/', title='Escolha uma música', filetypes=(("mp3 Files", "*.mp3"),))
    song = song.replace("/home/", "")
    #song = song.replace(".mp3", " ")
    #song = song.replace(".m4a", " ")
    #song = song.replace(".wav", " ")
    #song = song.replace("/", " ")
    caixa_seletora.insert(END, song)

#Adicionar várias músicas 
def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir='/home/', title='Escolha uma música', filetypes=(("mp3 Files", "*.mp3"),))

    for song in songs:
        song = song.replace("/home/", "")
        caixa_seletora.insert(END, song)

#tocar musica
def play():
    song = caixa_seletora.get(ACTIVE)
    song = f"/home/{song}"
    #song = f'/home/magnus/Projetos/{song}.wav'
    #song = f'/home/magnus/Projetos/{song}.m4a'
    pygame.mixer.music.load(song)
    pygame.mixer.Channel(0).play(pygame.mixer.Sound(song), loops=0)

global pausado
pausado = False

global chovendo
chovendo = 1
chuvis = './gui/rain.mp3'

#Modo Chuva
def chuva(estachovendo):
    global chovendo
    chovendo = estachovendo
    if (estachovendo != 1):
        chovendo = 1 
        pygame.mixer.music.load(chuvis)
        pygame.mixer.Channel(1).play(pygame.mixer.Sound(chuvis), loops=1000)
        
    else:
        chovendo = 2 
        pygame.mixer.Channel(1).pause()       

#pausar musica
def pause(estapausado):
    global pausado
    pausado = estapausado
    if pausado:
        pygame.mixer.Channel(0).unpause()
        pausado = False
    else:
        pausado = True
        pygame.mixer.Channel(0).pause()
        
#foreward button e backforeward button 
def foreward():
    proxima_musica = caixa_seletora.curselection()
    proxima_musica = proxima_musica[0]+1
    song = caixa_seletora.get(proxima_musica)
    song = f"/home/{song}"
    pygame.mixer.music.load(song)
    pygame.mixer.Channel(0).play(pygame.mixer.Sound(song), loops=0)
    caixa_seletora.selection_clear(0, END)
    caixa_seletora.activate(proxima_musica)
    caixa_seletora.selection_set(proxima_musica, last=None) 

def backforeward():
    proxima_musica = caixa_seletora.curselection()
    proxima_musica = proxima_musica[0]-1
    song = caixa_seletora.get(proxima_musica)
    song = f"/home/{song}"
    pygame.mixer.music.load(song)
    pygame.mixer.Channel(0).play(pygame.mixer.Sound(song), loops=0)
    caixa_seletora.selection_clear(0, END)
    caixa_seletora.activate(proxima_musica)
    caixa_seletora.selection_set(proxima_musica, last=None) 

#deleta todas músicas da playlist
def deletesong():
    caixa_seletora.delete(ANCHOR)
    pygame.mixer.Channel(0).stop()

#deleta todas as músicas da playlist 
def deleteallsongs():
    caixa_seletora.delete(0, END)
    pygame.mixer.Channel(0).stop()

#musica pygame
pygame.mixer.init()

#mensagens e widgets 
parnalogo = PhotoImage(file='./gui/parnalogo.png')
parnamirim = Label(janela, image=parnalogo, bg='#06030a', fg='green')
parnamirim.place(x=5, y=400)

gitlogo = PhotoImage(file='./gui/GitH2.png')
mensagem1 = Label(bg='#06030a', fg='green', text='Escola Estadual Santos Dumont', font=('Lucida', 11))
mensagem1.place(x=65, y=420)
caixa_mensagens = Label(
bg='#06030a', text='github.com/MagnusStr', font=('Terminal', 11), 
foreground='green'
)
git = Label(image=gitlogo, bg='#06030a')
git.place(x=20, y=460)
caixa_mensagens.place(x=60, y=470)
versao = Label(janela, text='Beta 2', bg= '#06030a', fg='lightgray', font=('Terminal', 11))
versao.place(x=420, y=480)


#imagens dos botões
rain_button = PhotoImage(file='./gui/cloud.png')
play_button = PhotoImage(file='./gui/play.png')
pause_button = PhotoImage(file='./gui/pause.png')
foreward_button = PhotoImage(file='./gui/foreward.png')
backforeward_button = PhotoImage(file='./gui/backforeward.png')

#controlador dos frames do player
controlador_botoes = Frame(janela)
controlador_botoes.pack()

#botões 
cloudbutton = Button(controlador_botoes, image=rain_button, borderwidth=0 ,bg='lightblue',  fg='lightblue', command=lambda: chuva(chovendo))
cloudbutton.grid(row=0, column=4)
playbutton = Button(controlador_botoes, image=play_button, borderwidth=0, bg='black', fg='black', command=play)
playbutton.grid(row=0, column=1)
pausebutton =  Button(controlador_botoes, image=pause_button, borderwidth=0, bg='black', command=lambda: pause(pausado))
pausebutton.grid(row=0, column=0)
forewardbutton =  Button(controlador_botoes, image=foreward_button, borderwidth=0, bg='black', command=foreward)
forewardbutton.grid(row=0, column=3)
backforewardbutton =  Button(controlador_botoes, image=backforeward_button, borderwidth=0, bg='black', command=backforeward)
backforewardbutton.grid(row=0 , column=2)

#menu
menu = Menu(janela)
janela.config(menu=menu)
sonsmenu = Menu(menu)
menu.add_cascade(label='Músicas', menu=sonsmenu, underline=0)
sonsmenu.add_command(label='Adicione uma música para a lista', command=add_song)
#adicionar várias músicas 
sonsmenu.add_command(label='Adicione várias músicas a lista', command=add_many_songs)
#remover musicas da playlist
remove_songs_menu = Menu(menu)
menu.add_cascade(label='Remover música', menu=remove_songs_menu, underline=0)
remove_songs_menu.add_command(label='Remover uma música da playlist', command= deletesong)
remove_songs_menu.add_command(label='Apagar playlist', command=deleteallsongs)

janela.mainloop()

