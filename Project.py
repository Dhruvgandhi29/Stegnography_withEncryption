import cv2
import os
from cryptography.fernet import Fernet

# Initializing Fernet for encryption and decryption


def initialize_fernet():
    enc_key = Fernet.generate_key()
    cipher = Fernet(enc_key)
    return cipher, enc_key

# Encrypting plaintext message


def encrypt_text(cipher, msg):
    encrypted_message = cipher.encrypt(bytes(msg, 'utf-8'))
    return encrypted_message

# Decrypting encrypted message


def decrypt_text(cipher, enc_msg):
    decrypted_message = cipher.decrypt(enc_msg).decode('utf-8')
    return decrypted_message

# Embedding encrypted message in image using block-wise approach


def embed_text_in_image(image, encMessage, block_size):
    n_max = image.shape[0]
    m_max = image.shape[1]
    tln = len(encMessage)
    m = 0
    n = 0
    z = 0
    # Calculating the number of blocks in the image
    block_count = (n_max // block_size) * (m_max // block_size)
    for i in range(tln):
        # Mapping each block to a position in the image
        block_number = i % block_count
        block_row = block_number // (m_max // block_size)
        block_col = block_number % (m_max // block_size)
        n = block_row * block_size
        m = block_col * block_size
        z = (z + 1) % 3
        image[n, m, z] = encMessage[i]
    return image

# Extracting embedded message from image using block-wise approach


def extract_text_from_image(image, n_max, m_max, encMessage, block_size):
    tln = len(encMessage)
    block_count = (n_max // block_size) * (m_max // block_size)
    z = 0
    decrypt_msg = ""
    for i in range(tln):
        # Mapping each block to a position in the image
        block_row = i // (m_max // block_size)
        block_col = i % (m_max // block_size)
        n = block_row * block_size
        m = block_col * block_size
        z = (z + 1) % 3
        decrypt_msg += chr(image[n, m, z])
    return decrypt_msg

# Main function to execute the program


def main():
    # Initialize Fernet
    cipher, enc_key = initialize_fernet()

    # Load the image
    image_path = "./test.jpg"
    image = cv2.imread(image_path)
    n_max = image.shape[0]
    m_max = image.shape[1]
    print(n_max, m_max)

    # User input
    msg = input("Enter your secret message:")
    password = input("Enter a password:")

    # Encryption
    encMessage = encrypt_text(cipher, msg)
    print("The encryption key:", enc_key)
    print("Message after encryption:", encMessage)

    # Embedding
    block_size = int(
        input("Enter block size[prefereably between 8-20 for small images]:"))
    embedded_image = embed_text_in_image(image.copy(), encMessage, block_size)

    # Save the image
    cv2.imwrite("Encrypted.jpg", embedded_image)
    os.startfile("Encrypted.jpg")
    print("Data Hiding in image completed successfully")

    # Decryption
    ch = int(input("\n\nEnter 1 to extract data from Image:"))
    if ch == 1:
        password1 = input("Re-enter the password to extract text:")
        if password == password1:
            decrypted_message = extract_text_from_image(
                embedded_image, n_max, m_max, encMessage, block_size)
            unembed = decrypt_text(cipher, decrypted_message)
            print("Decrypted Message is: ", decrypted_message)
            print("Embedded text was:", unembed)
        else:
            print("Password doesn't match")
    else:
        print("Thank you. Exiting")


# Execute the main function if the script is run
if __name__ == "__main__":
    main()
