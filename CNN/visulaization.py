"""
Visualize how an image transforms as it passes through each layer
of the LeNet-5 style model.

Core idea:
    A trained (or even untrained) Keras model is just a graph of
    layers. `model.layers[i].output` is a symbolic tensor -- you can
    build a NEW Model that reuses the same weights but exposes those
    intermediate tensors as outputs. One forward pass then gives you
    every layer's activation, not just the final softmax.
"""

import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.layers import Conv2D, AveragePooling2D, Flatten, Dense


def build_lenet():
    model = Sequential()
    model.add(Conv2D(6, kernel_size=(5, 5), padding='valid',
                      activation='tanh', input_shape=(32, 32, 1)))
    model.add(AveragePooling2D(pool_size=(2, 2), strides=2, padding='valid'))
    model.add(Conv2D(16, kernel_size=(5, 5), padding='valid', activation='tanh'))
    model.add(AveragePooling2D(pool_size=(2, 2), strides=2, padding='valid'))
    model.add(Flatten())
    model.add(Dense(120, activation='tanh'))
    model.add(Dense(84, activation='tanh'))
    model.add(Dense(10, activation='softmax'))
    return model


def get_activation_model(model):
    """A model with the same weights, but every layer's output exposed."""
    layer_outputs = [layer.output for layer in model.layers]
    return Model(inputs=model.inputs, outputs=layer_outputs)


def load_image(path=None, size=(32, 32)):
    """
    Loads a grayscale image and preprocesses it to (1, 32, 32, 1),
    normalized to [0, 1]. If no path is given, generates a synthetic
    digit-like blob so you can test the pipeline without a file.
    """
    if path is not None:
        from tensorflow.keras.preprocessing.image import load_img, img_to_array
        img = load_img(path, color_mode='grayscale', target_size=size)
        arr = img_to_array(img) / 255.0
    else:
        arr = np.zeros((*size, 1), dtype='float32')
        arr[8:24, 8:24, 0] = 1.0  # a plain white square as a stand-in

    return np.expand_dims(arr, axis=0)  # add batch dim -> (1,32,32,1)


def plot_feature_maps(layer_name, activation, max_maps=8):
    """Plots one layer's activation. Handles both conv-like (4D) and dense (2D) outputs."""
    if activation.ndim == 4:
        n_maps = min(activation.shape[-1], max_maps)
        fig, axes = plt.subplots(1, n_maps, figsize=(2 * n_maps, 2))
        if n_maps == 1:
            axes = [axes]
        for i in range(n_maps):
            axes[i].imshow(activation[0, :, :, i], cmap='viridis')
            axes[i].axis('off')
        fig.suptitle(f"{layer_name}  shape={activation.shape[1:]}")
    else:
        # Flatten / Dense output: show as a single heatmap row
        fig, ax = plt.subplots(figsize=(8, 1.2))
        ax.imshow(activation.reshape(1, -1), cmap='viridis', aspect='auto')
        ax.set_yticks([])
        ax.set_title(f"{layer_name}  shape={activation.shape[1:]}")

    plt.tight_layout()
    plt.show()


def main(image_path=None):
    model = build_lenet()
    model.summary()

    activation_model = get_activation_model(model)
    img_batch = load_image(image_path)

    activations = activation_model.predict(img_batch)

    # show the original input first
    plt.imshow(img_batch[0, :, :, 0], cmap='gray')
    plt.title("Input image (32x32)")
    plt.axis('off')
    plt.show()

    for layer, activation in zip(model.layers, activations):
        plot_feature_maps(layer.name, activation)


if __name__ == "__main__":
    # pass a real file path once you have one, e.g. main("digit.png")
    main() 