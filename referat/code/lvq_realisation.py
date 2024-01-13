import numpy as np

class LVQNetworkCompetitive:
    
    def __init__(self, input_size, output_size):
        self.input_size = input_size
        self.output_size = output_size
        self.ws = np.random.rand(output_size, input_size)

    def find_winner(self, input_vector):
        distances = np.linalg.norm(self.ws - input_vector, axis=1)
        winner_index = np.argmin(distances)
        return winner_index

    def update_weights(self, input_vector, learning_rate, winner_index, target):
            for i in range(self.input_size):
                self.ws[winner_index, i] += learning_rate * \
                                            (target - self.ws[winner_index, i]) * \
                                            input_vector[i]

    def compute_error(self, input_data, targets):
        total_error = 0.0
        for input_vector, target in zip(input_data, targets):
            winner_index = self.find_winner(input_vector)
            total_error += np.sum((input_vector - self.ws[winner_index]) ** 2) / 2

        return total_error

    def train(self, input_data, targets, epochs, initial_learning_rate):
        learning_rate = initial_learning_rate

        for epoch in range(epochs):
            for input_vector, target in zip(input_data, targets):
                winner_index = self.find_winner(input_vector)
                self.update_weights(input_vector, learning_rate, winner_index, target)

            training_error = self.compute_error(input_data, targets)
            print(f"Эпоха {epoch + 1}/{epochs}, Ошибка обучения: {training_error}")
            learning_rate *= np.exp(-epoch / 1000)

    def predict(self, input_vector):
        winner_index = self.find_winner(input_vector)
        return winner_index