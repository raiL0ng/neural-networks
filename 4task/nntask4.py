import autograd.numpy as np
from autograd import grad
import json, sys

class FeedForward:


    def __init__(self, ws) -> None:
        self.ws = ws
        self.n = len(ws)


    def sigmoid(self, x : float) -> float:
            return 1.0 / (1.0 + np.exp(-x))


    def go_forward(self, x : list) -> (list, list):
        sum = np.dot(self.ws[0], x)
        y = np.array([self.sigmoid(x) for x in sum])
        for i in range(1, self.n):
            sum = np.dot(self.ws[i], y)
            y = np.array([self.sigmoid(x) for x in sum])
        return y


def read_json_file(name) -> dict:
    try:
        f = open(name)
        data = json.load(f)
        f.close()
    except:
        print(f"Файла `{name}` не существует. "
              "Проверьте корректность имени файла.")
        exit(0)
    return data


def args_parser(argv : list) -> None:
    in1, in2, out = None, None, None
    for el in argv:
        if "matrix=" in el:
            in1 = el[el.find("=") + 1:]
        elif "vector=" in el:
            in2 = el[el.find("=") + 1:]
        elif "out=" in el:
            out = el[el.find("=") + 1:]
        
    if (in1 is None) or (in2 is None):
        print("Для корректной работы программы необходимо"
              " добавить в качестве аргументов названия файлов"
              " формата JSON для следующих параметров:\n"
              "matrix= -- файл, где лежат матрицы весов\n"
              "vector= -- файл с входными параметрами\n")
        exit(0)
    return in1, in2, out


def write_to_file(data, filename) -> bool:
        try:
            with open(filename, 'w') as f:
                json.dump(data, f)
        except:
            print(f'Ошибка записи данных в файл `{filename}`')
            exit(0)
        else:
            print(f'Данные были успешно записаны в файл `{filename}`')


def main():
    mtrx, vec, out = args_parser(sys.argv)
    if out is None:
        print("Отсутствует название файла для вывода.\n"
              "Файл для вывода был выбран по умолчанию (output.txt)")
        out = "output.txt"
    WS = read_json_file(mtrx)
    xs = read_json_file(vec)
    ws = []
    for w in WS['W']:
        ws.append(np.array(w))
    ys = []
    c = FeedForward(ws)
    for x in xs['x']:
        ys.append(list(c.go_forward(np.array(x))))
    write_to_file({'y' : ys}, out)

if __name__ == '__main__':
    main()