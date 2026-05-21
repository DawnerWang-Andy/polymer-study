"""
分子结构可视化脚本（RDKit）。
用法: python mol_visualize.py <input.smi> [--output mol.png]
"""

import argparse

from rdkit import Chem
from rdkit.Chem import Draw


def draw_molecule(smiles: str, output: str) -> None:
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"无法解析 SMILES: {smiles}")
    img = Draw.MolToImage(mol, size=(600, 400))
    img.save(output)
    print(f"分子图保存至 {output}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Draw molecule from SMILES")
    parser.add_argument("input", help="SMILES file (one SMILES per line)")
    parser.add_argument("--output", default="molecule.png", help="Output image path")
    parser.add_argument("--line", type=int, default=1, help="Which line to read (1-indexed)")
    args = parser.parse_args()

    with open(args.input) as f:
        lines = [l.strip() for l in f if l.strip()]
    if not lines:
        raise SystemExit("Empty SMILES file")
    idx = min(args.line - 1, len(lines) - 1)
    draw_molecule(lines[idx], args.output)


if __name__ == "__main__":
    main()
