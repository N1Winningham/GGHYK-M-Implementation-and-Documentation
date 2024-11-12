import numpy as np
import os

r = 0.5  # Perturbation vector (should be between about 10-50 for 400 dimensions)
e = np.array([1, -1])   # Roudning error
character = []  # Character array (For outputting the character version of message and decrypted message)

# Function to read message from file
def readFile(filePathname):
    with open(filePathname, 'r') as file:
        while True:
            chunk = file.read(2)  # Read 2 characters at a time
            if not chunk:
                break
            asciiValues = [ord(char) for char in chunk]  # Convert characters to ASCII values
            if len(asciiValues) < 2:
                asciiValues.append(0)  # Pad with null if chunk is less than 2 characters
            yield np.array(asciiValues)

# Function to generate lattice points
def generateLatticePoints(basis):
    bounds = (-10, 10)  # Bounds for the lattice points
    x, y = np.meshgrid(
        np.arange(bounds[0], bounds[1] + 1),
        np.arange(bounds[0], bounds[1] + 1)
    )
    integerPoints = np.column_stack((x.flatten(), y.flatten()))  # Stack the x and y values into a 2D array
    latticePoints = np.dot(integerPoints, basis)  # Matrix multiplication
    distances = np.linalg.norm(latticePoints, axis=1)
    sortedIndices = np.argsort(distances)
    return latticePoints[sortedIndices]

def encodeMessage(asciiValues, latticePoints):
    maxValue = max(asciiValues)
    # Map ASCII values to lattice points
    return np.array([
        latticePoints[min(len(latticePoints)-1, int((ascii / maxValue) * (len(latticePoints) - 1)))]
        for ascii in asciiValues
    ])

# Encryption function
def encrypt(basis, message, e):
    cipherText = np.dot(basis, message) + e # Encryption formula
    # print("Ciphertext:", cipherText)
    return cipherText

# Decryption function
def decrypt(basis, message, e):
    basis_inv = np.linalg.inv(basis)    # Inverse of the basis matrix
    decryptedText = np.dot(basis_inv, message) - e  # Decryption formula
    decryptedText[0] = np.ceil(decryptedText[0])    # Round the first value up
    decryptedText[1] = np.floor(decryptedText[1])   # Round the second value down
 #   print("Decrypted Message:", decryptedText)
    return decryptedText

# Function to write the result to a file on the Desktop
def writeFile(outputPathname, data_chunks):
    desktopPathname = os.path.expanduser("~/Desktop")  # Path to the Desktop
    outputFile = os.path.join(desktopPathname, outputPathname)    # Combine Desktop path with the output file name
    
    with open(outputFile, 'w') as file:
        for chunk in data_chunks:
            file.write(''.join(chr(int(value)) for value in chunk if value != 0))  # Exclude padding
    print(f"Data saved to {outputFile}")




# Exectuing Code
print("Select an option:")
print("1 - Encrypt")
print("2 - Decrypt")
choice = input("Enter 1 or 2: ")

filePathname = input("Enter the file path: ")
asciiMessage = readFile(filePathname)  # Read the contents of the file

rows = int(input("Enter the number of rows for the basis matrix: "))
columns = int(input("Enter the number of columns for the basis matrix: "))
goodBasis = []
for i in range(rows):
    row = list(map(int, input(f"Enter row {i+1} (space-separated values): ").split()))
    if len(row) != columns:
        print(f"Error: Row {i+1} must have {columns} elements.")
    goodBasis.append(row)
goodBasis = np.array(goodBasis)

# Assigns the values to the opperations
outputChunks = []
if choice == "1":
    for ascii_chunk in readFile(filePathname):
        encrypted_chunk = encrypt(goodBasis, ascii_chunk, e)
        outputChunks.append(encrypted_chunk)
    writeFile(f"encrypted_{os.path.basename(filePathname)}", outputChunks)

elif choice == "2":
    for ascii_chunk in readFile(filePathname):
        decrypted_chunk = decrypt(goodBasis, ascii_chunk, e)
        outputChunks.append(decrypted_chunk)
    writeFile(f"decrypted_{os.path.basename(filePathname)}", outputChunks)

else:
    print("Invalid option, please enter 1 or 2.")


























# import numpy as np
# import os

# r = 0.5  # Perturbation vector (should be between about 10-50 for 400 dimensions)
# e = np.array([1, -1])  # Rounding error
# character = []  # Character array (for outputting the character version of message and decrypted message)

# # Function to read message from file in chunks of 2 characters
# def readFile(filePathname):
#     with open(filePathname, 'r') as file:
#         while True:
#             chunk = file.read(2)  # Read 2 characters at a time
#             if not chunk:
#                 break
#             ascii_values = [ord(char) for char in chunk]  # Convert characters to ASCII values
#             if len(ascii_values) < 2:
#                 ascii_values.append(0)  # Pad with 0 if chunk is less than 2 characters
#             yield np.array(ascii_values)

# # Function to generate lattice points
# def generateLatticePoints(basis):
#     bounds = (-10, 10)
#     x, y = np.meshgrid(np.arange(bounds[0], bounds[1] + 1), np.arange(bounds[0], bounds[1] + 1))
#     integerPoints = np.column_stack((x.flatten(), y.flatten()))
#     latticePoints = np.dot(integerPoints, basis)
#     distances = np.linalg.norm(latticePoints, axis=1)
#     sortedIndices = np.argsort(distances)
#     return latticePoints[sortedIndices]

# # Encryption function for a 2-element chunk
# def encrypt(basis, message_chunk, e):
#     cipherText = np.dot(basis, message_chunk) + e
#     return cipherText

# # Decryption function for a 2-element chunk
# def decrypt(basis, cipher_chunk, e):
#     basis_inv = np.linalg.inv(basis)
#     decryptedText = np.dot(basis_inv, cipher_chunk) - e
#     decryptedText[0] = np.ceil(decryptedText[0])  # Round the first value up
#     decryptedText[1] = np.floor(decryptedText[1])  # Round the second value down
#     return decryptedText

# # Function to write the result to a file on the Desktop
# def writeFile(outputPathname, data_chunks):
#     desktopPathname = os.path.expanduser("~/Desktop")
#     outputFile = os.path.join(desktopPathname, outputPathname)
    
#     with open(outputFile, 'w') as file:
#         for chunk in data_chunks:
#             file.write(''.join(chr(int(value)) for value in chunk if value != 0))  # Exclude padding
#     print(f"Data saved to {outputFile}")

# # Executing Code
# print("Select an option:")
# print("1 - Encrypt")
# print("2 - Decrypt")
# choice = input("Enter 1 or 2: ")

# file_path = input("Enter the file path: ")

# rows = int(input("Enter the number of rows for the basis matrix: "))
# columns = int(input("Enter the number of columns for the basis matrix: "))
# goodBasis = []
# for i in range(rows):
#     row = list(map(int, input(f"Enter row {i+1} (space-separated values): ").split()))
#     if len(row) != columns:
#         print(f"Error: Row {i+1} must have {columns} elements.")
#     goodBasis.append(row)
# goodBasis = np.array(goodBasis)

# # Process file by chunks and perform encryption or decryption
# output_chunks = []
# if choice == "1":
#     for ascii_chunk in readFile(file_path):
#         encrypted_chunk = encrypt(goodBasis, ascii_chunk, e)
#         output_chunks.append(encrypted_chunk)
#     writeFile(f"encrypted_{os.path.basename(file_path)}", output_chunks)

# elif choice == "2":
#     for ascii_chunk in readFile(file_path):
#         decrypted_chunk = decrypt(goodBasis, ascii_chunk, e)
#         output_chunks.append(decrypted_chunk)
#     writeFile(f"decrypted_{os.path.basename(file_path)}", output_chunks)

# else:
#     print("Invalid option, please enter 1 or 2.")
