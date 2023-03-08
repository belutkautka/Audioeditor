#!/bin/bash
from pathlib import Path
from collections import deque
import shutil
import Audio


class History:
    def __init__(self, name):
        self.dir = Path(Path.cwd(), "systemFiles", "History_" + name)
        if self.dir.is_dir():
            shutil.rmtree(self.dir)
        Path.mkdir(self.dir)
        self.queue = deque()

    def add(self, name):
        self.queue.append(Path(name))
        if len(self.queue) > 5:
            trash = self.queue.popleft()
            trash.unlink()

    def goBack(self, audio):
        if len(self.queue) == 0:
            print('Невозможно откатиться дальше по истории изменений')
        trash = self.queue.pop()
        audio.current = self.queue.pop()
        self.add(str(audio.current))
        trash.unlink()

    def save(self):
        if len(self.queue) == 0:
            print('Не было изменений')
            return
        print("В какую директорию сохранить файл?")
        print("Если хотите продолжить без сохранения, нажмите enter")
        while True:
            path = input()
            if path == "":
                self.ex()
            my_file = Path(path)
            if not my_file.is_dir():
                print("Директория не найдена, попробуйте еще раз")
                continue
            a = self.queue.pop()
            self.add(str(a))
            while True:
                print("Под каким имеем сохранить аудиофайл")
                name = input()
                b = str(my_file) + "\\" + name + a.suffix
                if Path(b).is_file():
                    print("Фаил с таким названием уже существует,"
                          " попробуйте еще раз")
                    continue
                break
            shutil.copy(str(a), str(b))
            break

    def ex(self):
        while (len(self.queue) > 0):
            trash = self.queue.popleft()
            trash.unlink()
        self.dir.rmdir()
        Audio.Audio()

    def ex_t(self):
        while (len(self.queue) > 0):
            trash = self.queue.popleft()
            trash.unlink()
        self.dir.rmdir()
