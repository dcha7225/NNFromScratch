import numpy as np


def load_data_small():
    """ 
    Load small training and validation dataset

    Returns a tuple of length 4 with the following objects:
    X_train: An N_train-x-M ndarray containing the training data (N_train examples, M features each)
    y_train: An N_train-x-1 ndarray contraining the labels
    X_val: An N_val-x-M ndarray containing the training data (N_val examples, M features each)
    y_val: An N_val-x-1 ndarray contraining the labels
    """
    train_all = np.loadtxt('data/smallTrain.csv', dtype=int, delimiter=',')
    valid_all = np.loadtxt('data/smallValidation.csv',
                           dtype=int, delimiter=',')

    X_train = train_all[:, 1:]
    y_train = train_all[:, 0]
    X_val = valid_all[:, 1:]
    y_val = valid_all[:, 0]

    return (X_train, y_train, X_val, y_val)


def load_data_medium():
    """ 
    Load medium training and validation dataset

    Returns a tuple of length 4 with the following objects:
    X_train: An N_train-x-M ndarray containing the training data (N_train examples, M features each)
    y_train: An N_train-x-1 ndarray contraining the labels
    X_val: An N_val-x-M ndarray containing the training data (N_val examples, M features each)
    y_val: An N_val-x-1 ndarray contraining the labels
    """
    train_all = np.loadtxt('data/mediumTrain.csv', dtype=int, delimiter=',')
    valid_all = np.loadtxt('data/mediumValidation.csv',
                           dtype=int, delimiter=',')

    X_train = train_all[:, 1:]
    y_train = train_all[:, 0]
    X_val = valid_all[:, 1:]
    y_val = valid_all[:, 0]

    return (X_train, y_train, X_val, y_val)


def load_data_large():
    """ 
    Load large training and validation dataset

    Returns a tuple of length 4 with the following objects:
    X_train: An N_train-x-M ndarray containing the training data (N_train examples, M features each)
    y_train: An N_train-x-1 ndarray contraining the labels
    X_val: An N_val-x-M ndarray containing the training data (N_val examples, M features each)
    y_val: An N_val-x-1 ndarray contraining the labels
    """
    train_all = np.loadtxt('data/largeTrain.csv', dtype=int, delimiter=',')
    valid_all = np.loadtxt('data/largeValidation.csv',
                           dtype=int, delimiter=',')

    X_train = train_all[:, 1:]
    y_train = train_all[:, 0]
    X_val = valid_all[:, 1:]
    y_val = valid_all[:, 0]

    return (X_train, y_train, X_val, y_val)


def linearForward(input, p):
    """
    Arguments:
        - input: input vector (N, in_features + 1) 
            WITH bias feature added as 1st col
        - p: parameter matrix (out_features, in_features + 1)
            WITH bias parameter added as 1st col (i.e. alpha / beta in the writeup)

    Returns:
        - output vector (N, out_features)
    """
    return np.matmul(input, np.transpose(p))


def sigmoidForward(a):
    """
    Arguments:
        - a: input vector (N, dim)

    Returns:
        - output vector (N, dim)
    """
    result = 1 / (1 + np.exp(-a))
    return result


def softmaxForward(b):
    """
    Arguments:
        - b: input vector (N, dim)

    Returns:
        - output vector (N, dim)
    """
    exp_b = np.exp(b)
    result = exp_b / np.sum(exp_b, axis=1, keepdims=True)
    return result


def crossEntropyForward(hot_y, y_hat):
    """
    Arguments:
        - hot_y: 1-hot encoding for true labels (N, K), where K is the # of classes
        - y_hat: (N, K) vector of probabilistic distribution for predicted label

    Returns:
        - cross entropy loss (scalar)
    """

    j = np.sum(hot_y * np.log(y_hat), axis=1)
    avg = (-(np.sum(j)))/(j.shape[0])
    return avg


def NNForward(x, y, alpha, beta):
    """
    Arguments:
        - x: input vector (N, M+1)
            WITH bias feature added as 1st col
        - y: ground truth labels of size (N,) or () when N=1
        - alpha: alpha parameter matrix (D, M+1)
            WITH bias parameter added as 1st col
        - beta: beta parameter matrix (K, D+1)
            WITH bias parameter added as 1st col



    Returns (refer to writeup for details):
        - x: the input vector
        - a: 1st linear output (N, D)
        - z: sigmoid output WITH bias feature added as 1st col (N, D+1)
        - b: 2nd linear output (N, K)
        - y_hat: softmax output (N, K)
        - J: cross entropy loss (scalar)

    """

    a = linearForward(x, alpha)
    z = sigmoidForward(a)
    z_with_bias = np.hstack((np.ones((z.shape[0], 1)), z))

    b = linearForward(z_with_bias, beta)
    y_hat = softmaxForward(b)

    y = np.eye(10)[y]

    J = crossEntropyForward(y, y_hat)

    return x, a, z_with_bias, b, y_hat, J


def softmaxBackward(hot_y, y_hat):
    """
    Arguments:
        - hot_y: 1-hot encoding for true labels (N, K) where K is the # of classes
        - y_hat: (N, K) vector of probabilistic distribution for predicted label
    """
    a = y_hat-hot_y
    return a


def linearBackward(prev, p, grad_curr):
    """
    Arguments:
        - prev: previous layer WITH bias feature
        - p: parameter matrix (alpha/beta) WITH bias parameter
        - grad_curr: gradients for current layer

    Returns:
        - grad_param: gradients for parameter matrix (i.e. alpha / beta)
            This should have the same shape as the parameter matrix.
        - grad_prevl: gradients for previous layer

    """

    grad_param = np.matmul(np.transpose(grad_curr), prev)
    grad_prevl = np.matmul(grad_curr, p[:, 1:])
    return grad_param, grad_prevl


def sigmoidBackward(curr, grad_curr):
    """
    Arguments:
        - curr: current layer WITH bias feature
        - grad_curr: gradients for current layer

    Returns: 
        - grad_prevl: gradients for previous layer
    """

    curr_noBias = curr[:, 1:]
    grad_prevl = grad_curr*curr_noBias*(1-curr_noBias)
    return grad_prevl


def NNBackward(x, y, alpha, beta, z, y_hat):
    """
    Arguments:
        - x: input vector (N, M)
        - y: ground truth labels of size (N,) or () when N=1
        - alpha: alpha parameter matrix (D, M+1)
            WITH bias parameter added as 1st col
        - beta: beta parameter matrix (K, D+1)
            WITH bias parameter added as 1st col
        - z: z as per writeup
        - y_hat: (N, K) vector of probabilistic distribution for predicted label

    Returns:
        - g_alpha: gradients for alpha
        - g_beta: gradients for beta
        - g_b: gradients for layer b (softmaxBackward)
        - g_z: gradients for layer z (linearBackward)
        - g_a: gradients for layer a (sigmoidBackward)
    """
    y = np.eye(10)[y]

    g_b = softmaxBackward(y, y_hat)

    g_beta, g_z = linearBackward(z, beta, g_b)
    g_a = sigmoidBackward(z, g_z)
    g_alpha, g_x = linearBackward(x, alpha, g_a)

    return g_alpha, g_beta, g_b, g_z, g_a


def SGD(tr_x, tr_y, valid_x, valid_y, hidden_units, num_epoch, init_flag, learning_rate):
    """
    Arguments:
        - tr_x: training data input (N_train, M)
        - tr_y: training labels (N_train, 1)
        - valid_x: validation data input (N_valid, M)
        - valid_y: validation labels (N_valid, 1)
        - hidden_units: Number of hidden units
        - num_epoch: Number of epochs
        - init_flag:
            - True: Initialize weights to random values in Uniform[-0.1, 0.1], bias to 0
            - False: Initialize weights and bias to 0
        - learning_rate: Learning rate

    Returns:
        - alpha weights
        - beta weights
        - train_entropy (length num_epochs): mean cross-entropy loss for training data for each epoch
        - valid_entropy (length num_epochs): mean cross-entropy loss for validation data for each epoch
    """
    M = tr_x.shape[1]
    N = tr_x.shape[0]

    train_entropy = np.zeros(num_epoch)
    valid_entropy = np.zeros(num_epoch)

    tr_x = np.hstack((np.ones((tr_x.shape[0], 1)), tr_x))
    valid_x = np.hstack((np.ones((valid_x.shape[0], 1)), valid_x))

    if init_flag:
        alpha = np.random.uniform(low=-0.1, high=0.1, size=(hidden_units, M))
        beta = np.random.uniform(low=-0.1, high=0.1, size=(10, hidden_units))
        alpha = np.hstack((np.zeros((alpha.shape[0], 1)), alpha))
        beta = np.hstack((np.zeros((beta.shape[0], 1)), beta))
    else:
        alpha = np.zeros((hidden_units, M+1))
        beta = np.zeros((10, hidden_units+1))

    for e in range(num_epoch):
        for i in range(N):
            x = tr_x[i].reshape(1, -1)
            y = np.array([tr_y[i]])

            x, a, z, b, y_hat, J = NNForward(x, y, alpha, beta)

            g_alpha, g_beta, _, _, _ = NNBackward(x, y, alpha, beta, z, y_hat)

            alpha = alpha - learning_rate*g_alpha
            beta = beta - learning_rate*g_beta

        _, _, _, _, _, JTrain = NNForward(tr_x, tr_y, alpha, beta)
        _, _, _, _, _, JValid = NNForward(valid_x, valid_y, alpha, beta)

        train_entropy[e] = JTrain
        valid_entropy[e] = JValid
    return alpha, beta, train_entropy, valid_entropy


def prediction(tr_x, tr_y, valid_x, valid_y, tr_alpha, tr_beta):
    """
    Arguments:
        - tr_x: training data input (N_train, M)
        - tr_y: training labels (N_train, 1)
        - valid_x: validation data input (N_valid, M)
        - valid_y: validation labels (N-valid, 1)
        - tr_alpha: alpha weights WITH bias
        - tr_beta: beta weights WITH bias

    Returns:
        - train_error: training error rate (float)
        - valid_error: validation error rate (float)
        - y_hat_train: predicted labels for training data
        - y_hat_valid: predicted labels for validation data
    """

    tr_x = np.hstack((np.ones((tr_x.shape[0], 1)), tr_x))
    valid_x = np.hstack((np.ones((valid_x.shape[0], 1)), valid_x))

    _, _, _, _, y_hat_train, _ = NNForward(tr_x, tr_y, tr_alpha, tr_beta)

    _, _, _, _, y_hat_valid, _ = NNForward(valid_x, valid_y, tr_alpha, tr_beta)

    trainPred = np.argmax(y_hat_train, axis=1)
    validPred = np.argmax(y_hat_valid, axis=1)

    train_error = np.sum(trainPred != tr_y)/tr_y.shape[0]
    valid_error = np.sum(validPred != valid_y)/valid_y.shape[0]

    return train_error, valid_error, trainPred, validPred


# FEEL FREE TO WRITE ANY HELPER FUNCTIONS

def train_and_valid(X_train, y_train, X_val, y_val, num_epoch, num_hidden, init_rand, learning_rate):
    """ 
    Main function to train and validate your neural network implementation.

    Arguments:
        - X_train: training input in (N_train, M) array. Each value is binary, in {0,1}.
        - y_train: training labels in (N_train, 1) array. Each value is in {0,1,...,K-1},
            where K is the number of classes.
        - X_val: validation input in (N_val, M) array. Each value is binary, in {0,1}.
        - y_val: validation labels in (N_val, 1) array. Each value is in {0,1,...,K-1},
            where K is the number of classes.
        - num_epoch: Positive integer representing the number of epochs to train (i.e. number of
            loops through the training data).
        - num_hidden: Positive integer representing the number of hidden units.
        - init_flag: Boolean value of True/False
            - True: Initialize weights to random values in Uniform[-0.1, 0.1], bias to 0
            - False: Initialize weights and bias to 0
        - learning_rate: Float value specifying the learning rate for SGD.

    Returns:
        - loss_per_epoch_train (length num_epochs): A list of float values containing the mean cross entropy on training data after each SGD epoch
        - loss_per_epoch_val (length num_epochs): A list of float values containing the mean cross entropy on validation data after each SGD epoch
        - err_train: Float value containing the training error after training (equivalent to 1.0 - accuracy rate)
        - err_val: Float value containing the validation error after training (equivalent to 1.0 - accuracy rate)
        - y_hat_train: A list of integers representing the predicted labels for training data
        - y_hat_val: A list of integers representing the predicted labels for validation data
    """

    alpha, beta, loss_per_epoch_train, loss_per_epoch_val = SGD(
        X_train, y_train, X_val, y_val, num_hidden, num_epoch, init_rand, learning_rate)

    err_train, err_val, y_hat_train, y_hat_val = prediction(
        X_train, y_train, X_val, y_val, alpha, beta)

    return (loss_per_epoch_train, loss_per_epoch_val,
            err_train, err_val, y_hat_train, y_hat_val)
