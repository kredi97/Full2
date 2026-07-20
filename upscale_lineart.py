#!/usr/bin/env python3
"""Upscale black-and-white line art without changing the drawing."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import cv2
import numpy as np
from PIL import Image


def load_grayscale(path: Path) -> np.ndarray:
    image = Image.open(path).convert("L")
    return np.array(image)


def clean_binary(gray: np.ndarray, threshold: int | None) -> np.ndarray:
    if threshold is None:
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    else:
        _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)

    # Remove isolated compression noise while keeping thin traces.
    kernel = np.ones((2, 2), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=1)
    return binary


def upscale_nearest(binary: np.ndarray, scale: int) -> Image.Image:
    height, width = binary.shape
    return Image.fromarray(binary, mode="L").resize(
        (width * scale, height * scale),
        resample=Image.Resampling.NEAREST,
    )


def upscale_potrace(binary: np.ndarray, scale: int) -> Image.Image:
    potrace = shutil.which("potrace")
    convert = shutil.which("convert")
    if not potrace or not convert:
        raise RuntimeError("potrace and ImageMagick convert are required for vector upscaling")

    height, width = binary.shape
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        pbm_path = tmp_path / "input.pbm"
        svg_path = tmp_path / "output.svg"
        png_path = tmp_path / "output.png"

        Image.fromarray((binary > 127).astype(np.uint8) * 255).convert("1").save(pbm_path)

        subprocess.run(
            [potrace, "-b", "svg", "-o", str(svg_path), str(pbm_path)],
            check=True,
            capture_output=True,
            text=True,
        )

        target_width = width * scale
        target_height = height * scale
        density = max(72 * scale, 300)

        subprocess.run(
            [
                convert,
                "-background",
                "white",
                "-density",
                str(density),
                str(svg_path),
                "-resize",
                f"{target_width}x{target_height}!",
                str(png_path),
            ],
            check=True,
            capture_output=True,
            text=True,
        )

        return Image.open(png_path).convert("L")


def upscale_image(
    input_path: Path,
    output_path: Path,
    scale: int = 8,
    method: str = "potrace",
    threshold: int | None = None,
) -> tuple[int, int, int, int]:
    gray = load_grayscale(input_path)
    binary = clean_binary(gray, threshold)

    if method == "nearest":
        result = upscale_nearest(binary, scale)
    elif method == "potrace":
        result = upscale_potrace(binary, scale)
    else:
        raise ValueError(f"Unknown method: {method}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    result.save(output_path, format="PNG", optimize=True)

    source_h, source_w = gray.shape
    out_w, out_h = result.size
    return source_w, source_h, out_w, out_h


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Increase resolution of line-art images while preserving the original drawing."
    )
    parser.add_argument("input", type=Path, help="Source image path")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("output_upscaled.png"),
        help="Destination PNG path",
    )
    parser.add_argument(
        "-s",
        "--scale",
        type=int,
        default=8,
        help="Upscale factor (default: 8)",
    )
    parser.add_argument(
        "-m",
        "--method",
        choices=("potrace", "nearest"),
        default="potrace",
        help="potrace keeps sharp traces; nearest preserves raw pixels",
    )
    parser.add_argument(
        "-t",
        "--threshold",
        type=int,
        default=None,
        help="Manual binarization threshold (0-255). Default: Otsu",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.input.exists():
        print(f"Input file not found: {args.input}", file=sys.stderr)
        return 1
    if args.scale < 1:
        print("Scale must be >= 1", file=sys.stderr)
        return 1

    src_w, src_h, out_w, out_h = upscale_image(
        args.input,
        args.output,
        scale=args.scale,
        method=args.method,
        threshold=args.threshold,
    )
    print(f"Saved: {args.output}")
    print(f"Size: {src_w}x{src_h} -> {out_w}x{out_h} ({args.method}, x{args.scale})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
