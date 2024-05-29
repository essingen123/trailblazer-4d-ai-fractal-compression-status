# One-liner to generate a beautiful fractal image
import matplotlib.pyplot as plt
import numpy as np

# Create a complex grid
x, y = np.meshgrid(np.linspace(-2, 2, 1000), np.linspace(-2, 2, 1000))
c = x + 1j * y

# Mandelbrot set computation
z = np.zeros_like(c)
for _ in range(100):
    z = z**2 + c

# Plot the result
plt.figure(figsize=(8, 8))
plt.imshow(np.abs(z), cmap='twilight_shifted', extent=(-2, 2, -2, 2))
plt.axis('off')
plt.title("Mandelbrot Set")
plt.show()
