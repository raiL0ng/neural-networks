import autograd.numpy as np
from autograd import grad
import json, sys

class BackPropagation:

    def __init__(self, W1, W2, n) -> None:
        self.W1 = np.array(W1)
        self.W2 = np.array(W2)
        self.n = n
        self.lmd = None
        self.messages = None

    def sigmoid(self, x : float) -> float:
        return 1.0 / (1.0 + np.exp(-x))

    def d_sigmoid(self, y : float) -> float:
        return y * (1.0 - y)

    def get_learning_rate_coeff(self, l : float) -> None:
        self.lmd = float(l)

    def mse(self, y_pred, y_true):
        return (1.0 / 2.0) * np.square(y_true - y_pred)

    def go_forward(self, input : list) -> (list, list):
        sum = np.dot(self.W1, input)
        output = np.array([self.sigmoid(x) for x in sum])
        sum = np.dot(self.W2, output)
        y = self.sigmoid(sum)
        return (y, output)

    def train(self, x_vec : list, y_true : list) -> None:
        m = len(x_vec)
        self.messages = []
        for i in range(1, self.n + 1):
            errors = []
            for k in range(m):
                y, out = self.go_forward(x_vec[k])
                e = self.mse(y, y_true[k])
                errors.append(list(e))
                delta = e * self.d_sigmoid(y)
                for t in range(len(self.W2)):
                    self.W2[t] = self.W2[t] - self.lmd * delta * out[t]
                for t in range(len(self.W1)):    
                    delta2 = self.W2 * delta * self.d_sigmoid(out[t])
                    self.W1[t, :] = self.W1[t, :] - x_vec[k] * delta2[t] * self.lmd
            self.messages.append(f"При i = {i} значения функции ошибок: {errors}\n")

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
    in1, in2, in3, out = None, None, None, None
    for el in argv:
        if "matrix=" in el:
            in1 = el[el.find("=") + 1:]
        elif "param=" in el:
            in2 = el[el.find("=") + 1:]
        elif "train=" in el:
            in3 = el[el.find("=") + 1:]
        elif "out=" in el:
            out = el[el.find("=") + 1:]
        
    if (in1 is None) or (in2 is None) or (in3 is None):
        print("Для корректной работы программы необходимо"
              " добавить в качестве аргументов названия файлов"
              " формата JSON для следующих параметров:\n"
              "matrix= -- файл, где лежат матрицы весов\n"
              "param= -- файл с параметром n (количество итераций)\n"
              "train= -- файл с входными и выходными параметрами\n")
        exit(0)
    return in1, in2, in3, out


def write_inf(mes : list, filename):
    mes = "".join(mes)
    try:
        f = open(filename, 'w')
        f.write(mes)
        f.close()
    except:
        print(f'Ошибка записи данных в файл {filename}')
        exit(0)
    
def main():
    # elements = []
    mtrx, par, train, out = args_parser(sys.argv)
    if out is None:
        print("Отсутствует название файла для вывода.\n"
              "Файл для вывода был выбран по умолчанию (output.txt)")
        out = "output.txt"
    mtrx = read_json_file(mtrx)
    par = read_json_file(par)
    train = read_json_file(train)
    if len(mtrx) != 2 or len(par) != 1:
        return
    print(f"\nМатрица весов W1 (первый слой): {mtrx['W1']}")
    print(f"\nМатрица весов W2 (второй слой): {mtrx['W2']}")
    print(f"\nКоличество итераций : {par['n']}")
    lmd = input("Введите значение коэффициента скорости обучения: ")
    bp = BackPropagation(mtrx['W1'], mtrx['W2'], par['n'])
    bp.get_learning_rate_coeff(lmd)
    xs = np.array(train["in"])
    ys = np.array(train["in"])
    bp.train(xs, ys)
    # elements.append((k, bp.messages))
    write_inf(bp.messages, out)    
if __name__ == '__main__':
    main()