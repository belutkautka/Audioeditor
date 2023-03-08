#!/bin/bash
import ffmpeg
import subprocess
from pathlib import Path
import History


class Audio:
    def __init__(self, check=True, path=""):
        self.count = 0
        if check == True:
            self.path = self._check()
        else:
            self.path = Path(path)
        self.name = self.path.name
        self.current = self.path
        self.history = History.History(self.name)
        self.dictionary = {
            0: lambda: self.history.ex(),  # lambda нужна, так как
            1: lambda: self.trim(),  # иначе эти методы
            2: lambda: self.concut(),  # начинают исполняться
            3: lambda: self.change_speed(),  # при иницилизации
            4: lambda: self.norm(),
            5: lambda: self.equalizer(),
            6: lambda: self.history.save(),
            7: lambda: self.history.goBack(self)
        }
        if check == True:
            self.menu()

    def _check(self):
        print('Напишите название аудиофaйла ( форматы : .mp3, .wav )')
        if self.count == 0:
            print("Если хотите выйти, нажмите enter")
        while True:
            name = input()
            if name == "":
                if self.count == 0:
                    exit()
                return Path("")
            my_file = Path(name)
            if not self.is_file(my_file):
                print("Фаил " + name + " не найден")
                print("Попробуйте еще раз")
                continue
            if not self.is_audio(my_file):
                print('Не поддерживается данное расширение,'
                      ' проверьте правильность названия файла ' + name)
                print("Попробуйте еще раз")
                continue
            return my_file

    def is_file(self, my_file):
        if my_file.is_file():
            return True
        return False

    def is_audio(self, my_file):
        if my_file.suffix == '.mp3' or my_file.suffix == ".wav":
            return True
        return False

    def trim(self):
        self.count += 1
        stream = ffmpeg.input(str(self.current))
        len = self.lenght(str(self.current))
        print('Укажите начало аудиофрагмента (в секундах) или нажмите enter,'
              ' чтобы выйти из данной функции')
        st, en = 0, 0
        while True:
            try:
                st = input()
                if st == "":
                    return
                st = int(st)
            except:
                print("Неправильный ввод попробуйте еще раз")
                continue
            if st < 0 or st > len:
                print("Начало вне аудиофрагмента, попробуйте еще раз")
                continue
            break
        print('Укажите конец аудиофрагмента (в секундах) или нажмите enter,'
              ' чтобы обрезалось до конца')
        while True:
            try:
                en = input()
                if en == "":
                    en = len
                    break
                en = int(en)
            except:
                print("Неправильный ввод попробуйте еще раз")
                continue
            if en < 0 or en > len:
                print("Конец вне аудиофрагмента, попробуйте еще раз")
                continue
            break
        self.trim_body(st, en, stream)

    def trim_body(self, st, en, stream):
        path = Path(self.history.dir, f"{self.count}{self.name}")
        stream = stream.filter_('atrim', start=st, end=en) \
            .filter_('asetpts', 'PTS-STARTPTS')
        stream = ffmpeg.output(stream, str(path), loglevel="quiet")
        ffmpeg.run(stream)
        self.current = path
        self.history.add(path)

    def concut(self):
        self.count += 1
        print('Напишите названия аудиофайлов'
              ', которыe надо склеить и потом enter')
        streams = []
        streams.append(ffmpeg.input(str(self.current)))
        while True:
            name = self._check()
            if name.name == "":
                break
            streams.append(ffmpeg.input(str(name)))
        self.concut_body(streams)

    def concut_body(self, streams):
        stream = ffmpeg.concat(*streams, v=0, a=1)
        path = Path(self.history.dir, f"{self.count}{self.name}")
        stream = ffmpeg.output(stream, str(path), loglevel="quiet")
        ffmpeg.run(stream)
        self.current = path
        self.history.add(path)

    def change_speed(self):
        self.count += 1
        print('Укажите во сколько раз надо ускорить'
              ' аудиодорожку (диапазон от 0.5 до 2.0) или нажмите enter,'
              ' чтобы выйти из данной функции')
        while True:
            speed = input()
            try:
                if speed == "":
                    return
                number = float(speed)
                if not (0.5 <= number <= 2.0):
                    print("Неправильный диапозон")
                    continue
            except:
                print("Неправильный формат ввода, попробуйте еще раз")
                continue
            break
        self.change_speed_body(speed)

    def change_speed_body(self, speed):
        path = Path(self.history.dir, f"{self.count}{self.name}")
        process = subprocess.Popen(['ffmpeg', "-loglevel", "-8",
                                    "-i", str(self.current), "-af",
                                    "atempo=" + speed, str(path)])
        process.wait()
        self.current = path
        self.history.add(path)

    def norm(self):
        self.count += 1
        path = Path(self.history.dir, f"{self.count}{self.name}")
        process = subprocess.Popen(['ffmpeg', "-loglevel", "-8", "-i",
                                    str(self.current), "-af", "dynaudnorm", str(path)])
        process.wait()
        self.current = path
        self.history.add(path)

    def equalizer(self):
        self.count += 1
        frequency = self.try_int("Введите центральную частоту или нажмите enter,"
                                 " чтобы выйти из данной функции")
        if frequency == "":
            return
        width = self.try_int("Введите нужную полосу пропускания или нажмите enter,"
                             " чтобы выйти из данной функции")
        if width == "":
            return

        g = self.try_int("Введите коэффициентом усиления(положтельное число)/"
                         "ослабления(отрицательное число)"
                         " или нажмите enter, чтобы выйти из данной функции")
        if g == "":
            return
        self.equalizer_body(frequency, width, g)

    def equalizer_body(self, frequency, width, g):
        path = Path(self.history.dir, f"{self.count}{self.name}")
        process = subprocess.Popen(['ffmpeg', "-loglevel", "-8",
                                    "-i", str(self.current), "-af",
                                    f"equalizer=f={frequency}:width_type=h"
                                    f":width={width}:g={g}", str(path)])
        process.wait()
        self.current = path
        self.history.add(path)

    def try_int(self, str):
        while True:
            print(str)
            value = input()
            try:
                if value == "":
                    return ""
                value = int(value)
                break
            except:
                print("Неправильный формат ввода, попробуйте еще раз")
        return value

    def lenght(self, name):
        return float(ffmpeg.probe(name)['format']['duration'])

    def menu(self):
        while True:
            print('Возможные функции:',
                  '0 - перестать работать с аудиозаписью',
                  '1 - обрзать аудио',
                  '2 - склеить несколько аудио',
                  '3 - ускорить или замедлить аудио',
                  '4 - нормализовать аудио (усреднить звук аудио)',
                  '5 - эквалайзер',
                  '6 - сохранить',
                  '7 - назад'
                  , sep='\n')
            command = input()
            try:
                command = int(command)
            except ValueError:
                print("Неправильный ввод команды, попробуйте еще раз")
                continue
            else:
                if not command in self.dictionary.keys():
                    print("Неправильный ввод команды, попробуйте еще раз")
                    continue
                self.dictionary[command]()
                print("!!!Готово!!!\n")
                self.menu()
                break
