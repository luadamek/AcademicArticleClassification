import numpy as np

class MatrixFactor:

    def __init__(self, X, masking, latent_factors = 0):
        self.data = X
        self.masking = masking
        self.latent_factors = latent_factors
        minimum = np.minimum(self.data)
        maximum = np.maximum(self.data)
        self.U = np.random.uniform(minimum, maximum, size=(x.shape[0], latent_factors))
        self.Z = np.random.uniform(minimum, maximum, size=(latent_factors, x.shape[1]))

    def update_parameters(self):
        for i in range(0, self.Z.shape[1]):
            M_b = np.einsum("i,ia,ik", self.masking[:,i], self.U, self.U)
            M_inv= np.lingalg.inverse(M_b)
            self.Z[:,i] = np.dot(np.dot(M_inv, self.U.transpose), (self.masking * self.data))

        for i in range(0, self.U.shape[0]):
            M_a = np.einsum("i,ai,ki", self.making[i,:], self.Z, self.Z)
            M_inv = np.linalg.inverse(M_a)
            self.U[i, :] = np.dot(np.dot( (self.masking * self.data), self.Z.transpose), M_inv)

    def get_predictions(self):
        return np.dot(self.U, self.Z) #recommendations for all users

    def calc_loss(self):
        pred = self.get_predictions()
        axes = [i for i in range(0, len(self.data.shape))]
        return np.sum(self.masking * (self.data - pred)**2, axis=axes)
