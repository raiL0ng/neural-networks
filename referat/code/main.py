from lvq_realisation import LVQNetworkCompetitive
import numpy as np
import json

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

def main():
    data_training = read_json_file("train_parameters.json")
    input_data = np.array(data_training["in"])
    targets = np.array(data_training["targets"])
    n = data_training["epochs"]
    learning_rate = data_training["learning_rate"]
    input_size = input_data.shape[1]
    output_size = 2 # по умолчанию два кластера на выходе
    lvq_net = LVQNetworkCompetitive(input_size, output_size)
    lvq_net.train(input_data, targets, n, learning_rate)
    while True:
        print('\n1. Проверить новые параметры.'
              '\n2. Выход.')
        bl = input("Выберите опцию: ")
        if bl == '1':
            new_data = read_json_file("new_parameters.json")["new_data"]
            for num, new_vector in enumerate(new_data):
                pred_cluster = lvq_net.predict(np.array(new_vector))
                print(f"Прогнозируемый кластер #{num}: {pred_cluster}")
        elif bl == '2':
            break

if __name__ == '__main__':
    main()

