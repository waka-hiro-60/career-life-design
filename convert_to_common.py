#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
convert_to_common.py
career-life-design の全HTMLをcommon.js/css対応に一括変換する

使い方：
  1. このファイルを career-life-design\ に置く
  2. PowerShellで実行：
     cd "G:\マイドライブ\Docs\career-life\career-life-design"
     python convert_to_common.py
"""

import os
import re

SITE_ROOT = os.path.dirname(os.path.abspath(__file__))

# ── 変換スキップするファイル ──────────────────────────────────
SKIP_FILES = [
    # qa/index.htmlはすでに対応済み
    os.path.join(SITE_ROOT, "QA", "index.html"),
    os.path.join(SITE_ROOT, "qa", "index.html"),
]

# ── ヘッダーのパターン（複数パターンに対応）──────────────────
HEADER_PATTERNS = [
    # パターン1：fixed緑ヘッダー（books/journal/contact/about）
    re.compile(
        r'<!-- ヘッダー -->\s*<header class="site-header">.*?</header>',
        re.DOTALL
    ),
    # パターン2：div.header-navパターン（一部ページ）
    re.compile(
        r'<header class="site-header">.*?</header>',
        re.DOTALL
    ),
]

# ── フッターのパターン ────────────────────────────────────────
FOOTER_PATTERNS = [
    re.compile(
        r'<!-- フッター -->\s*<footer class="site-footer">.*?</footer>',
        re.DOTALL
    ),
    re.compile(
        r'<footer class="site-footer">.*?</footer>',
        re.DOTALL
    ),
]

# ── ヘッダーCSS のパターン（削除対象）────────────────────────
HEADER_CSS_PATTERN = re.compile(
    r'/\*\s*──\s*ヘッダー\s*──\s*\*/.*?(?=/\*\s*──(?!\s*ヘッダー))',
    re.DOTALL
)

FOOTER_CSS_PATTERN = re.compile(
    r'/\*\s*──\s*フッター\s*──\s*\*/.*?(?=</style>)',
    re.DOTALL
)

def convert_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    changed = False

    # すでにcommon.js対応済みならスキップ
    if 'common.js' in content:
        print(f"  ⏭️  スキップ（対応済み）: {os.path.relpath(filepath, SITE_ROOT)}")
        return False

    # ── ヘッダーHTML → プレースホルダー ──
    for pattern in HEADER_PATTERNS:
        new_content = pattern.sub('<div id="site-header"></div>', content, count=1)
        if new_content != content:
            content = new_content
            changed = True
            break

    # ── フッターHTML → プレースホルダー ──
    for pattern in FOOTER_PATTERNS:
        new_content = pattern.sub('<div id="site-footer"></div>', content, count=1)
        if new_content != content:
            content = new_content
            changed = True
            break

    # ── common.cssをfont読み込みの前に追加 ──
    if '/assets/css/common.css' not in content:
        content = content.replace(
            '<link rel="preconnect" href="https://fonts.googleapis.com">',
            '<link rel="stylesheet" href="/assets/css/common.css">\n<link rel="preconnect" href="https://fonts.googleapis.com">'
        )
        changed = True

    # ── common.jsを</body>の前に追加 ──
    if '/assets/js/common.js' not in content:
        content = content.replace(
            '</body>',
            '<script src="/assets/js/common.js"></script>\n</body>'
        )
        changed = True

    # ── margin-top:60px をパンくず・メインに追加（fixed header対応）──
    # page-heroやbreadcrumbにmargin-topがなければ追加
    if 'margin-top:60px' not in content and 'margin-top: 60px' not in content:
        # page-heroがある場合
        content = content.replace(
            '<div class="page-hero">',
            '<div class="page-hero" style="margin-top:60px;">'
        )
        # breadcrumbがある場合（page-heroがないページ）
        content = content.replace(
            '<nav class="breadcrumb">',
            '<nav class="breadcrumb" style="margin-top:60px;">'
        )
        changed = True

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ 変換完了: {os.path.relpath(filepath, SITE_ROOT)}")
        return True
    else:
        print(f"  ⚠️  変換パターン不一致: {os.path.relpath(filepath, SITE_ROOT)}")
        return False


def main():
    print("=" * 60)
    print("common.js/css 一括変換スクリプト")
    print(f"対象ディレクトリ: {SITE_ROOT}")
    print("=" * 60)

    html_files = []
    for root, dirs, files in os.walk(SITE_ROOT):
        # .git フォルダは除外
        dirs[:] = [d for d in dirs if d != '.git']
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))

    html_files.sort()
    print(f"\n対象ファイル数: {len(html_files)}\n")

    success = 0
    skipped = 0
    failed = 0

    for filepath in html_files:
        # スキップ対象チェック
        if any(os.path.normcase(filepath) == os.path.normcase(s) for s in SKIP_FILES):
            print(f"  ⏭️  スキップ（除外リスト）: {os.path.relpath(filepath, SITE_ROOT)}")
            skipped += 1
            continue

        result = convert_file(filepath)
        if result:
            success += 1
        else:
            failed += 1

    print(f"\n{'=' * 60}")
    print(f"完了: {success}件変換 / {skipped}件スキップ / {failed}件パターン不一致")
    print(f"{'=' * 60}")
    print("\n次のステップ：")
    print('  git add .')
    print('  git commit -m "Add: 全ページcommon.js/css対応"')
    print('  git push origin main')

if __name__ == '__main__':
    main()
