"""
通用数据绘图脚本。
用法: python data_plot.py <input.csv> [--x col] [--y col] [--output fig.png]
"""

import argparse

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def plot(df: pd.DataFrame, x: str, y: str, output: str) -> None:
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(df[x], df[y], "o-", markersize=4)
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    fig.tight_layout()
    fig.savefig(output, dpi=150)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="Quick data plot from CSV")
    parser.add_argument("input", help="CSV file path")
    parser.add_argument("--x", default="x", help="X column name")
    parser.add_argument("--y", default="y", help="Y column name")
    parser.add_argument("--output", default="plot.png", help="Output figure path")
    args = parser.parse_args()

    df = load_data(args.input)
    plot(df, args.x, args.y, args.output)
    print(f"Plot saved to {args.output}")


if __name__ == "__main__":
    main()
