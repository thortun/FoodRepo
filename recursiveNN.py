import numpy as np

import time

class RNN(object):
    """Recursive Neural Network."""
    def __init__(self, hidden_size, seq_length, learning_rate, data):
        """Initializes
        hyperparam = [hidden_size, seq_length, learning_rate]
        If we have set load_from_file to True, we will do that
        by loading the parameters from the directory rnn_name
        """
        self.init_data(data) # Initialize the data
        self.hidden_size, self.seq_length, self.learning_rate = hidden_size, seq_length, learning_rate
        self.Wxh = np.random.randn(self.hidden_size, self.vocab_size)*0.01  # Input to hidden
        self.Whh = np.random.randn(self.hidden_size, self.hidden_size)*0.01 # Hidde to hidden
        self.Why = np.random.randn(self.vocab_size, self.hidden_size)*0.01  # Hidden to outpu
        self.bh = np.zeros((self.hidden_size, 1))                           # Hidden bias
        self.by = np.zeros((self.vocab_size, 1))                            # Output bias
        self.iter = 0                                                       # Number of training iterations
        self.global_iter = 0                                                # Initialize global iter
        self.smooth_loss = -np.log(1.0/self.vocab_size)*self.seq_length # loss at iteration 0
        self.mWxh, self.mWhh, self.mWhy = np.zeros_like(self.Wxh), np.zeros_like(self.Whh), np.zeros_like(self.Why)

    def init_data(self, data):
        """Defines what data to train on."""
        self.data = data # Sets the data
        chars = list(set(self.data))
        self.data_size, self.vocab_size = len(self.data), len(chars) # Set some params
        self.char_to_ix = {ch : i for i, ch in enumerate(chars)}
        self.ix_to_char = {i : ch for i, ch in enumerate(chars)}

    def train(self, num_iter = -1):
        """One training iteration for the RNN."""
        print "Started trainin! Data size %s | Unique chars %s" % (self.data_size, self.vocab_size)
        p = 0 # Start at the start of the data
        mbh, mby = np.zeros_like(self.bh), np.zeros_like(self.by) # memory variables for Adagrad

        try:
            for _ in xrange(0, num_iter): # Train forever
                # prepare inputs (we're sweeping from left to right in steps seq_length long)
                if p + self.seq_length+1 >= len(self.data) or self.iter == 0: 
                    hprev = np.zeros((self.hidden_size, 1)) # reset RNN memory
                    p = 0 # go from start of data
                inputs = [self.char_to_ix[ch] for ch in self.data[p:p + self.seq_length]]
                targets = [self.char_to_ix[ch] for ch in self.data[p + 1:p + self.seq_length + 1]]

                # forward seq_length characters through the net and fetch gradient
                loss, dWxh, dWhh, dWhy, dbh, dby, hprev = self.lossFun(inputs, targets, hprev)
                self.smooth_loss = self.smooth_loss * 0.999 + loss * 0.001

                # perform parameter update with Adagrad
                for param, dparam, mem in zip([self.Wxh, self.Whh, self.Why, self.bh, self.by], 
                                              [dWxh, dWhh, dWhy, dbh, dby], 
                                              [self.mWxh, self.mWhh, self.mWhy, mbh, mby]):
                    mem += dparam * dparam
                    param += -self.learning_rate * dparam / np.sqrt(mem + 1e-8) # adagra

                p += self.seq_length # move data pointer
                self.iter += 1 # iteration counter
                self.global_iter += 1

                if self.iter % 1000 == 0:
                    sample_ix = self.sample(hprev, inputs[0], 2000)
                    txt = ''.join(self.ix_to_char[ix] for ix in sample_ix)
                    fileID = open('recipe.txt', 'w')
                    fileID.write('----\n %s \n----' % (txt, ))
                if self.iter % 1000 == 0: print 'iter %d, loss: %f' % (self.global_iter, self.smooth_loss) # print progress

        except KeyboardInterrupt: # If we interrupt, save it!
            self.save('rnn1')     # Save the current state
            exit(0)               # Exit the training

    def lossFun(self, inputs, targets, hprev):
        """
        inputs,targets are both list of integers.
        hprev is Hx1 array of initial hidden state
        returns the loss, gradients on model parameters, and last hidden state
        """
        xs, hs, ys, ps = {}, {}, {}, {}
        hs[-1] = np.copy(hprev)
        loss = 0
        # forward pass
        for t in xrange(len(inputs)):
            xs[t] = np.zeros((self.vocab_size,1)) # encode in 1-of-k representation
            xs[t][inputs[t]] = 1
            hs[t] = np.tanh(np.dot(self.Wxh, xs[t]) + np.dot(self.Whh, hs[t-1]) + self.bh) # hidden state
            ys[t] = np.dot(self.Why, hs[t]) + self.by # unnormalized log probabilities for next chars
            ps[t] = np.exp(ys[t]) / np.sum(np.exp(ys[t])) # probabilities for next chars
            loss += -np.log(ps[t][targets[t],0]) # softmax (cross-entropy loss)
        # backward pass: compute gradients going backwards
        dWxh, dWhh, dWhy = np.zeros_like(self.Wxh), np.zeros_like(self.Whh), np.zeros_like(self.Why)
        dbh, dby = np.zeros_like(self.bh), np.zeros_like(self.by)
        dhnext = np.zeros_like(hs[0])
        for t in reversed(xrange(len(inputs))):
            dy = np.copy(ps[t])
            dy[targets[t]] -= 1 # backprop into y. see http://cs231n.github.io/neural-networks-case-study/#grad if confused here
            dWhy += np.dot(dy, hs[t].T)
            dby += dy
            dh = np.dot(self.Why.T, dy) + dhnext # backprop into h
            dhraw = (1 - hs[t] * hs[t]) * dh # backprop through tanh nonlinearity
            dbh += dhraw
            dWxh += np.dot(dhraw, xs[t].T)
            dWhh += np.dot(dhraw, hs[t-1].T)
            dhnext = np.dot(self.Whh.T, dhraw)
        for dparam in [dWxh, dWhh, dWhy, dbh, dby]:
            np.clip(dparam, -5, 5, out=dparam) # clip to mitigate exploding gradients
        return loss, dWxh, dWhh, dWhy, dbh, dby, hs[len(inputs)-1]

    def sample_to_string(self, sample_ix):
        """Takes a sample and makes it a string"""
        txt = ''.join(self.ix_to_char[ix] for ix in sample_ix)
        return txt

    def sample(self, h, seed_ix, n):
        """ 
        sample a sequence of integers from the model 
        h is memory state, seed_ix is seed letter for first time step
        """
        x = np.zeros((self.vocab_size, 1))
        x[seed_ix] = 1
        ixes = []
        for t in xrange(n):
            h = np.tanh(np.dot(self.Wxh, x) + np.dot(self.Whh, h) + self.bh)
            y = np.dot(self.Why, h) + self.by
            p = np.exp(y) / np.sum(np.exp(y))
            ix = np.random.choice(range(self.vocab_size), p = p.ravel())
            x = np.zeros((self.vocab_size, 1))
            x[ix] = 1
            ixes.append(ix)
        return ixes

    def save(self, dirname):
        """Saves the RNN for later traning.
        saves all files in the directory 'dirname' with
        'standardized' names.
        """
        np.save(dirname + '/Wxh', self.Wxh)  # Save input to hidden
        np.save(dirname + '/Whh', self.Whh)  # Save hidden to hidden
        np.save(dirname + '/Why', self.Why)  # Save hidden to ouput
        np.save(dirname + '/bh', self.bh)    # Save hidden bias
        np.save(dirname + '/by', self.by)    # Save output bias
        with open(dirname + '/iter.txt', 'wb') as fileID:
            fileID.write(str(self.global_iter)) # Write the global counter to file
            fileID.close()                   # Close the file down
        with open(dirname + '/smooth_loss.txt', 'wb') as fileID:
            fileID.write(str(self.smooth_loss))
            fileID.close()

    def load(self, dirname):
        """Loads the RNN from a file."""
        self.Wxh = np.load(dirname + '/Wxh.npy')  # Save input to hidden
        self.Whh = np.load(dirname + '/Whh.npy')  # Save hidden to hidden
        self.Why = np.load(dirname + '/Why.npy')  # Save hidden to ouput
        self.bh = np.load(dirname + '/bh.npy')    # Save hidden bias
        self.by = np.load(dirname + '/by.npy')    # Save output bias
        with open(dirname + '/iter.txt', 'rb') as fileID:
            self.global_iter = int(fileID.read()) # Read the global iteration index
        with open(dirname + '/smooth_loss.txt', 'rb') as fileID:
            self.smooth_loss = float(fileID.read())

data = open('recipeData.txt', 'r').read()

rnn = RNN(256, 100, 1e-1, data)
rnn.train(10**8)
