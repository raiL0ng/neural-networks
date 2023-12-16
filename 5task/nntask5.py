import autograd.numpy as np
from autograd import grad
import json

class BackPropagation:

    def __init__(self, W1, W2) -> None:
        self.W1 = W1
        self.W2 = W2
        self.lmd = None
        self.messages = None

    def sigmoid(self, x : float) -> float:
        return 1.0 / (1.0 + np.exp(-x))

    def d_sigmoid(self, y : float) -> float:
        return y * (1.0 - y)

    def get_learning_rate(self, l : float) -> None:
        self.lmd = l

    def mse(self, y_pred, y_true):
        return (1.0 / 2.0) * np.square(y_true - y_pred)

    def go_forward(self, input : list) -> (list, list):
        sum = np.dot(self.W1, input)
        output = np.array([self.sigmoid(x) for x in sum])
        sum = np.dot(self.W2, output)
        y = self.sigmoid(sum)
        return (y, output)

    def train(self, x_vec : list, y_true : list, n : int) -> None:
        m = len(x_vec)
        self.messages = []
        for i in range(1, n + 1):
            errors = []
            for k in range(m):
                y, out = self.go_forward(x_vec[k])
                e = self.mse(y, y_true[k])
                errors.append(e)
                delta = e * self.d_sigmoid(y)
                for t in range(len(self.W2)):
                    self.W2[t] = self.W2[t] - self.lmd * delta * out[t]
                for t in range(len(self.W1)):    
                    delta2 = self.W2 * delta * self.d_sigmoid(out[t])
                    self.W1[t, :] = self.W1[t, :] - x_vec[k] * delta2[t] * self.lmd
            self.messages.append(f"При i = {i} значения функции ошибок: {errors}")

def read_json_file(self, name) -> dict:
    try:
        f = open(name)
        data = json.load(f)
        f.close()
    except:
        print(f"Файла `{self._in}` не существует. "
              "Проверьте корректность имени файла.")
        exit(0)
    return data


def args_parser(argv : list) -> None:
    global graphs
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
              "param= -- файл с параметром n -- количество итераций"
              "train= -- файл с входными и выходными параметрами")
        return False
    return True

def main():
    pass


def test():
    w1 = [[0.1], [0.2], [0.3], [0.4], [0.5], [0.6], [0.7], [0.8], [0.9], [0.0]]
    w2 = [[0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]]
    w2 = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
    x__ = [[0.1],[0.2],[0.3],[0.4],[0.5],[0.6],[0.7],[0.8],[0.9],[1.0]]
    # x = [[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]]
    y__ = [[0.9], [0.8], [0.7], [0.6], [0.5], [0.4], [0.3], [0.2], [0.1], [0.0]]
    # x = [[0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0]]
    # x = np.array(x)
    # w1 = np.array(w1)
    # print(len(w1), len(w1[0]), len(x))
    # print(np.dot(w1, x))

    c = BackPropagation(np.array(w1),np.array(w2))
    c.get_learning_rate(0.2)
    y_, out = c.go_forward(np.array(x__[0]))
    e = c.mse(y_, np.array(y__[0]))
    print(e, y_, out)
    c.train(np.array(x__), np.array(y__), 10)
    # print(c.W1[0, :], c.W1[0])

if __name__ == '__main__':
    main()