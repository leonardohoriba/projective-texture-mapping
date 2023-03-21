# 5o ano - COMP 2023
# Alu Leonardo Horiba - 19411
# 1o Ten Marin - 19027
# Cap Caique Nery - 

# Coordenadas da imagem para inserir a textura
# a11 = (251,693)
# a12 = (553,681)
# a21 = (264,887)
# a22 = (532,877)

from PIL import Image
import numpy as np


def insertTexture(
    texture_path: str,
    image_path: str,
    image_target: list,
    output_path: str = "storage/output.jpg",
) -> None:
    """
    texture_path (str): Path of texture image.
    image_path (str): Path of image.
    image_target (list): List of target coordinates.
    output_path (str): Path of output image.
    """

    # Open images
    texture = Image.open(texture_path)
    img = Image.open(image_path)

    (x_t, y_t) = texture.size
    (x_i, y_i) = img.size

    # Texture points
    texture_coordinates = [(0, 0, 1), (x_t, 0, 1), (0, y_t, 1), (x_t, y_t, 1)]

    # Image points (get_coordinates.py code to generate the points)
    image_coordinates = image_target

    # Construindo a matriz A usada no sistema:
    # A.t = B ----> t tem como coordenadas as entradas da transformacao
    A = np.array([[0 for x in range(12)] for y in range(12)])
    B = np.array([0 for x in range(12)])

    for i in range(0, 3):
        B[i] = image_coordinates[0][i]

    for i in range(0, 4):
        for j in range(0, 3):
            A[3 * i][j] = A[3 * i + 1][j + 3] = A[3 * i + 2][
                j + 6
            ] = texture_coordinates[i][j]
        if i > 0:
            A[3 * i][8 + i] = -image_coordinates[i][0]
            A[3 * i + 1][8 + i] = -image_coordinates[i][1]
            A[3 * i + 2][8 + i] = -image_coordinates[i][2]

    # Resolvendo o sistema para achar T
    # A.t = B ----> t = inv(A).B
    t = np.linalg.inv(A).dot(B)
    T = np.array([[t[3 * j + i] for i in range(3)] for j in range(3)])

    # Calculo a Inversa
    Tinv = np.linalg.inv(T)

    # Percorrer a figura de destino e cola o pixel no lugar correspondente
    for a in range(x_i):
        for b in range(y_i):
            v = (a, b, 1)

            # Calculo do produto Tinv.v
            i = Tinv[0][0] * v[0] + Tinv[0][1] * v[1] + Tinv[0][2] * v[2]
            j = Tinv[1][0] * v[0] + Tinv[1][1] * v[1] + Tinv[1][2] * v[2]
            k = Tinv[2][0] * v[0] + Tinv[2][1] * v[1] + Tinv[2][2] * v[2]

            # Normalizacao da ultima coordenada para 1
            i = int(i / k)
            j = int(j / k)

            if i >= 0 and j >= 0 and i < x_t and j < y_t:
                img.putpixel([a, b], texture.getpixel((int(i), int(j))))

    # Show the output
    img.save(output_path)
    img.show()


if __name__ == "__main__":
    TEXTURE_PATH = "storage/german_cano.jpg"
    IMAGE_PATH = "storage/caique.JPG"
    IMAGE_TARGET = [(251, 693, 1), (553, 681, 1), (264, 887, 1), (532, 877, 1)]

    insertTexture(
        texture_path=TEXTURE_PATH, image_path=IMAGE_PATH, image_target=IMAGE_TARGET
    )
