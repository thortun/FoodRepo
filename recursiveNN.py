import numpy as np

class RNN(object):
    """Recursive Neural Network."""
    def __init__(self, hidden_size, seq_length, learning_rate, data):
        """Initializes
        hyperparam = [hidden_size, seq_length, learning_rate]
        """
        self.init_data(data) # Initialize the data
        self.hidden_size, self.seq_length, self.learning_rate = hidden_size, seq_length, learning_rate
        self.Wxh = np.random.randn(self.hidden_size, self.vocab_size)*0.01  # Input to hidden
        self.Whh = np.random.randn(self.hidden_size, self.hidden_size)*0.01 # Hidde to hidden
        self.Why = np.random.randn(self.vocab_size, self.hidden_size)*0.01  # Hidden to outpu
        self.bh = np.zeros((self.hidden_size, 1))                           # Hidden bias
        self.by = np.zeros((self.vocab_size, 1))                            # Output bias

    def init_data(self, data):
        """Defines what data to train on."""
        self.data = data # Sets the data
        chars = list(set(self.data))
        self.data_size, self.vocab_size = len(self.data), list(set(data)) # Set some params
        self.char_to_ix = {ch : i for i, ch in enumerate(chars)}
        self.ix_to_char = {i : ch for i, ch in enumerate(chars)}

data = open('input.txt', 'r').read()
rnn = RNN(64, 50, 1e-1, data)
