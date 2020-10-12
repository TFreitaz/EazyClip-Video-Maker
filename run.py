from tkinter import *
from tkinter import filedialog, ttk
from moviepy.editor import *
from PIL import Image
import shutil
import os

window = Tk()
window.title("EazyClip")
window.geometry('1000x600')

class VideoGenerator:
    def __init__(self):
        self.img_formats = ['png', 'jpg', 'jpeg']
        self.audio_formats = ['.mp3']
        self.img_folder = None
        self.audio = True
        self.audiofile = None
        self.convert_text = Label(window, text = 'Selecione a pasta dos arquivos para o clip.')
        self.convert_text.grid(column = 0, row = 0, padx = 5, pady = 5)
        self.convert_entry = Entry(window, width = 60)
        self.convert_entry.grid(column = 0, row = 1, padx = 5, pady = 5)
        self.convert_entry.insert(END, 'Diretório de arquivos')
        self.select_button = Button(window, text = 'Selecionar', command = self.select_folder)
        self.select_button.grid(column = 1, row = 1, padx = 5, pady = 5)
        self.processing_text = StringVar()
        self.processing_label = Label(window, textvariable = self.processing_text)
        self.processing_label.grid(column = 0, row = 2, padx = 5, pady = 5)
        self.audio_checkbox = Checkbutton(window, text="Audio", variable=self.audio, onvalue=True, offvalue=False, state=NORMAL)
        self.audio_checkbox.select()
        self.audio_checkbox.grid(column=2, row=1, padx=5, pady=5)
        self.duration_method_text = Label(window, text='Duração do vídeo.')
        self.duration_method_text.grid(column=3, row=0, padx=5, pady=5)
        self.duration_method_cb = ttk.Combobox(window, width=25)
        self.duration_method_cb.grid(column=3, row=1, padx=5, pady=5)
        self.duration_method_cb['values'] = ['-SELECIONAR-', 'Definir duração total', 'Definir duração por imagem', 'Ajustar ao áudio']
        self.duration_method_cb.current(0)
        self.duration_method_cb.bind("<<ComboboxSelected>>", self.change_duration_method)
        self.convert_button = Button(window, text = 'Gerar video', command = self.makeclip)
        self.convert_button.grid(column = 4, row = 1, padx = 5, pady = 5)
        
    def change_duration_method(self, event):
        if self.duration_method_cb.get() == 'Definir duração total':
            if 'img_duration_entry' in self.__dict__:
                self.img_duration_entry.destroy()
            self.total_duration_entry = Entry(window, width = 25)
            self.total_duration_entry.grid(column = 3, row = 2, padx = 5, pady = 5)
            self.total_duration_entry.insert(END, '0')
        elif self.duration_method_cb.get() == 'Definir duração por imagem':
            if 'total_duration_entry' in self.__dict__:
                self.total_duration_entry.destroy()
            self.img_duration_entry = Entry(window, width = 25)
            self.img_duration_entry.grid(column = 3, row = 2, padx = 5, pady = 5)
            self.img_duration_entry.insert(END, '0')
        else:
            if 'img_duration_entry' in self.__dict__:
                self.img_duration_entry.destroy()
            if 'img_duration_entry' in self.__dict__:
                self.img_duration_entry.destroy()
        
    def select_folder(self):
        self.path = filedialog.askdirectory(initialdir = "/",title = "Selecionar pasta").replace('/', '\\')
        self.convert_entry.delete(0, 'end')
        self.convert_entry.insert(END, self.path)
        
    def makeclip(self):
        self.search_images_folder()
        self.processing_text.set(f'Redimensionando imagens.')
        self.reshape()
        if self.audio:
            self.search_audio()
            self.processing_text.set(f'Obtendo audio.')
            audio = AudioFileClip(f'{self.path}/{self.audio_file}')
            self.duration_method = self.duration_method_cb.get()
            n = len(os.listdir(f'{self.path}/{self.img_folder}/Editeds'))
            
            if self.duration_method == 'Definir duração total':
                self.total_duration = float(self.total_duration_entry.get())
                n = len(os.listdir(f'{self.path}/{self.img_folder}/Editeds'))
                durations = [self.total_duration/n]*n
                if audio.duration > self.total_duration:
                    audio = audio.subclip(0, self.total_duration)
                
            elif self.duration_method == 'Definir duração por imagem':
                self.img_duration = float(self.img_duration_entry.get())
                n = len(os.listdir(f'{self.path}/{self.img_folder}/Editeds'))
                durations = [self.img_duration]*n
                if audio.duration > self.total_duration:
                    audio = audio.subclip(0, self.total_duration)
                
            elif self.duration_method == 'Ajustar ao áudio':
                self.total_duration = audio.duration
                durations = [self.total_duration/n]*n
                
            self.processing_text.set(f'Gerando video.')
            video = ImageSequenceClip(f'{self.path}/{self.img_folder}/Editeds', durations=durations)
            audio = audio.audio_fadein(5).audio_fadeout(5)
            video.audio = audio
            self.processing_text.set(f'Renderizando video.')
            video.write_videofile(f'{self.path}/video.mp4', fps=20)
            self.processing_text.set(f'Procedimento concluído.')
        
    def search_audio(self):
        for file in os.listdir(self.path):
            if any(file.endswith(audio_format) for audio_format in self.audio_formats):
                self.audio_file = file
        if not self.audio_file:
            raise Exception('Audio file not found.')
        
    def search_images_folder(self):
        if any(any(file.endswith(img_format) for img_format in self.img_formats) for file in os.listdir(self.path)):
            self.img_folder = 'Imagens'
            os.mkdir(self.img_folder)
            for file in os.listdir(self.path):
                if any(file.endswith(img_format) for img_format in self.img_formats):
                    shutil.move(file, f'{self.path}/{self.img_folder}')                      
        else:
            for item in os.listdir(self.path):
                if os.path.isdir(f'{self.path}/{item}'):
                    if all(any(file.endswith(img_format) for img_format in self.img_formats) for file in os.listdir(f'{self.path}/{item}') if os.path.isfile(f'{self.path}/{item}/{file}')) and len(os.listdir(f'{self.path}/{item}'))>0:
                        self.img_folder = item
        if not self.img_folder:
            raise Exception( 'Image folder not found.')
                        
    def reshape(self):
        files = os.listdir(f'{self.path}/{self.img_folder}')
        new_folder = 'Editeds'

        if new_folder not in files:
            os.mkdir(f'{self.path}/{self.img_folder}/{new_folder}')

        for file in files:
            if any(file.endswith(img_format) for img_format in self.img_formats):
                name = ' '.join(file.split('.')[:-1])
                image = Image.open(f'{self.path}/{self.img_folder}/{file}', 'r')
                image_size = image.size
                screen_w = 1000
                screen_h = 600
                width = image_size[0]
                height = image_size[1]
                w_rat = width/screen_w
                h_rat = height/screen_h
                max_rat = max([w_rat, h_rat])
                if max_rat > 1:
                    width = int(width/max_rat)
                    height = int(height/max_rat)
                    image = image.resize((width, height), Image.ANTIALIAS)
                background = Image.new('RGBA', (screen_w, screen_h), (255, 255, 255, 255))
                offset = (int(round(((screen_w - width) / 2), 0)), int(round(((screen_h - height) / 2),0)))

                background.paste(image, offset)
                background.save(f'{self.path}/{self.img_folder}/{new_folder}/{name}.png')
        
vg = VideoGenerator()