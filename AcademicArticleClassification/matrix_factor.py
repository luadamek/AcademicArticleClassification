import numpy as np

class MatrixFactor:

    def __init__(self, X, masking, latent_factors = 0):
        self.data = X
        self.masking = masking
        self.latent_factors = latent_factors
        minimum = np.amin(self.data)
        maximum = np.amax(self.data)
        self.U = np.random.uniform(minimum, maximum, size=(self.data.shape[0], latent_factors))
        self.Z = np.random.uniform(minimum, maximum, size=(latent_factors, self.data.shape[1]))

    def update_parameters(self):
        original_u = np.copy(self.U)
        original_z = np.copy(self.Z)
        current_loss = self.calc_loss()

        for i in range(0, self.Z.shape[1]):
            M_b = np.einsum("i,ia,ik", self.masking[:,i], self.U, self.U)
            M_inv= np.linalg.inv(M_b)
            d1 = np.dot(M_inv, self.U.transpose())
            result = np.dot(d1 , (self.masking * self.data)[:,i])
            self.Z[:,i] = result

        new_loss = self.calc_loss()
        if new_loss > current_loss:
            self.Z, self.U = original_z, original_u

        original_u = np.copy(self.U)
        original_z = np.copy(self.Z)
        current_loss = self.calc_loss()

        for i in range(0, self.U.shape[0]):
            M_a = np.einsum("i,ai,ki", self.masking[i,:], self.Z, self.Z)
            M_inv = np.linalg.inv(M_a)
            d1 = np.dot( (self.masking * self.data)[i,:], self.Z.transpose())
            result = np.dot(d1, M_inv)
            self.U[i, :] = result

        new_loss = self.calc_loss()
        if new_loss > current_loss:
            self.Z, self.U = original_z, original_u

    def get_predictions(self):
        return np.dot(self.U, self.Z) #recommendations for all users

    def calc_loss(self):
        pred = self.get_predictions()
        return np.sum(np.sum(self.masking * (self.data - pred)**2))
