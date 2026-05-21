"""
实验报告生成器：从模板 + 数据生成 Markdown 报告。
用法: python report_generator.py <template.md> <data.csv> [--output report.md]
"""

import argparse
from datetime import datetime


def render(template: str, data: dict[str, str]) -> str:
    for key, val in data.items():
        template = template.replace(f"{{{{{key}}}}}", val)
    return template


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate experiment report from template")
    parser.add_argument("template", help="Markdown template path")
    parser.add_argument("data", help="CSV data file")
    parser.add_argument("--output", default="report.md", help="Output path")
    args = parser.parse_args()

    with open(args.template) as f:
        template = f.read()

    data = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "data_file": args.data,
    }

    result = render(template, data)
    with open(args.output, "w") as f:
        f.write(result)
    print(f"报告已生成: {args.output}")


if __name__ == "__main__":
    main()
