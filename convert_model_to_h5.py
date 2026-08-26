#!/usr/bin/env python3
"""Convert a Keras SavedModel or .keras file to an HDF5 (.h5) Keras file.

Usage:
    python convert_model_to_h5.py --input path/to/model.keras --output model.h5

If the input is a TensorFlow SavedModel directory or a `.keras` file, this script
will load it with `tf.keras.models.load_model` and save as `.h5`.
"""
import argparse
import os
import sys

try:
    import tensorflow as tf
except Exception as e:
    print("TensorFlow is required. Install with: pip install tensorflow")
    raise


def convert(input_path: str, output_path: str):
    if not os.path.exists(input_path):
        print(f"Input not found: {input_path}")
        sys.exit(2)

    print(f"Loading model from: {input_path}")
    model = tf.keras.models.load_model(input_path, compile=False)

    out_dir = os.path.dirname(output_path)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    print(f"Saving model to: {output_path}")
    # For HDF5 format, provide a filename that ends with .h5
    model.save(output_path)
    print("Done.")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", "-i", required=True, help="SavedModel directory or .keras file")
    p.add_argument("--output", "-o", required=True, help="Output .h5 filename (e.g. model.h5)")
    args = p.parse_args()

    if args.output.lower().endswith(('.h5', '.hdf5')):
        convert(args.input, args.output)
    else:
        print("Output filename should end with .h5 or .hdf5")
        sys.exit(2)


if __name__ == '__main__':
    main()
