import numpy as np
import matplotlib.pyplot as plt
r = 0.5  # Perturbation vector (should be between about 10-50 for 400 dimensions)
e = np.array([1, -1])   # Roudning error
m = []  # Message array (Used for storing the ASCII values of the message)
character = []  # Character array (For outputting the character version of message and decrypted message)
with open(##FILE DESTINATION##, 'r') as file:
    contents = file.read().strip()   # Read the contents of the file and remove any leading/trailing whitespace
message = list(contents)    # Convert the contents of the file to a list of characters
asciiMessage = [ord(char) for char in message]  # Convert message to ASCII values
m = np.array(asciiMessage)  # Create a numpy array directly from the ASCII values
goodBasis = np.array([[3, 1], [1, 2]])  # Private basis (W)
badBasis = np.array([[9234, 3002], [10393, 623423]])  # Public basis (U)
def generateLatticePoints(basis):
    bounds = (-10, 10)  # Bounds for the lattice points
    # Generate a grid of integer points
    x, y = np.meshgrid(
        np.arange(bounds[0], bounds[1] + 1),
        np.arange(bounds[0], bounds[1] + 1)
    )
    
    integer_points = np.column_stack((x.flatten(), y.flatten()))    # Stack the x and y values into a 2D array
    
    # Ensure basis is a 2x2 matrix and perform matrix multiplication
    lattice_points = np.dot(integer_points, basis)
    
    distances = np.linalg.norm(lattice_points, axis=1)
    sorted_indices = np.argsort(distances)
    
    return lattice_points[sorted_indices]
privateLatticePoints = generateLatticePoints(goodBasis)
publicLatticePoints = generateLatticePoints(badBasis)
def encodeMessage(asciiValues, latticePoints):
    maxValue = max(asciiValues)
    # Map ASCII values to lattice points
    return np.array([
        latticePoints[min(len(latticePoints)-1, int((ascii / maxValue) * (len(latticePoints) - 1)))]
        for ascii in asciiValues
    ])
def encrypt(basis, message, e):
    cipherText = np.dot(basis, message) + e # Encryption formula
    print("Ciphertext:", cipherText)
    return cipherText
def decrypt(basis, message, e):
    basis_inv = np.linalg.inv(basis)    # Inverse of the basis matrix
    decryptedText = np.dot(basis_inv, message) - e  # Decryption formula
    decryptedText[0] = np.ceil(decryptedText[0])    # Round the first value up
    decryptedText[1] = np.floor(decryptedText[1])   # Round the second value down
    print("Decrypted Message:", decryptedText)
    return decryptedText
print("Message: ", m)
for value in m:
    character.append(chr(int(value)))  # Convert each decrypted integer to a character and append it
character = ''.join(character)  # Join the list of characters into a single string
print("Message: ", character)
character = []  # Reset the character list
encodedMessage = encodeMessage(asciiMessage, publicLatticePoints)   # Encodes message into lattice points
print("Encoded Message Lattice Points:", encodedMessage)
ciphertext = encrypt(goodBasis, m, e)    # Encrypt using public basis, message, and perturbation vector
decryptedtext = decrypt(goodBasis, ciphertext, e)    # Decrypt using public basis, ciphertext, and perturbation vector
for value in decryptedtext:
    character.append(chr(int(value)))  # Convert each decrypted integer to a character and append it
character = ''.join(character)  # Join the list of characters into a single string
print("Decrypted Message: ", character)
