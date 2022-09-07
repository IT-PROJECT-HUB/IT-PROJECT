import numpy as np

donut_size = 30
theta_spacing = 0.07
phi_spacing = 0.02
illumination = np.fromiter(".,-~:;=!*#$@", dtype="<U1")

A = 1
B = 1
R1 = 1
R2 = 2
K2 = 5

K1 = donut_size * K2 * 3 / (8 * (R1+R2))


def render_frame(a: float, b: float) -> np.ndarray:
    cos_a = np.cos(a)
    sin_a = np.sin(a)
    cos_b = np.cos(b)
    sin_b = np.sin(b)

    output = np.full((donut_size, donut_size), " ")
    buffer = np.zeros((donut_size, donut_size))

    cos_phi = np.cos(phi := np.arange(0, 2 * np.pi, phi_spacing))
    sin_phi = np.sin(phi)
    cos_theta = np.cos(theta := np.arange(0, 2 * np.pi, theta_spacing))
    sin_theta = np.sin(theta)

    circle_x = R2 + R1 * cos_theta
    circle_y = R1 * sin_theta

    x = (np.outer(cos_b * cos_phi + sin_a * sin_b * sin_phi, circle_x) - circle_y * cos_a * sin_b).T
    y = (np.outer(sin_b * cos_phi - sin_a * cos_b * sin_phi, circle_x) + circle_y * cos_a * cos_b).T
    z = ((K2 + cos_a * np.outer(sin_phi, circle_x)) + circle_y * sin_a).T

    ooz = np.reciprocal(z)

    xp = (donut_size / 2 + K1 * ooz * x).astype(int)
    yp = (donut_size / 2 - K1 * ooz * y).astype(int)

    L1 = (((np.outer(cos_phi, cos_theta) * sin_b) - cos_a *np.outer(sin_phi, cos_theta)) - sin_a * sin_theta)
    L2 = cos_b * (cos_a * sin_theta - np.outer(sin_phi, cos_theta * sin_a))
    L = np.around(((L1 + L2) * 8 )).astype(int).T
    mask_L = L >= 0
    chars = illumination[L]

    for i in range(90):
        mask = mask_L[i] & (ooz[i] > buffer[xp[i], yp[i]])
        buffer[xp[i], yp[i]] = np.where(mask, ooz[i], buffer[xp[i], yp[i]])
        output[xp[i], yp[i]] = np.where(mask, chars[i], output[xp[i], yp[i]])

    return output


def pprint(array: np.ndarray) -> None:
    print(*[" ".join(row) for row in array], sep="\n")


if __name__ == '__main__':
    while True:
        for _ in range(donut_size * donut_size):
            A += theta_spacing
            B += phi_spacing
            print("\x1b[H")
            pprint(render_frame(A, B))
