    import os
    import re
    import shutil

    # --- 設定 ---
    # プロジェクトのルートからの相対パスを定義
    DECK_MD_PATH = 'docs/DECK.md'
    CARDS_DIR_PATH = 'docs/cards'
    TEMPLATE_PATH = 'templates/SCREEN_CARD_TEMPLATE.md'
    # --- 設定ここまで ---

    def parse_deck_file(deck_path):
        """DECK.mdを解析し、カードの情報を抽出する"""
        cards_info = []
        try:
            with open(deck_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            print(f"エラー: {deck_path} が見つかりません。")
            return []

        # カード一覧のセクションから情報を抽出する正規表現
        # 例: * `CARD-001`: ログイン画面
        card_regex = re.compile(r"\*\s*`([A-Z]+-\d+)`:\s*(.*)")

        for match in card_regex.finditer(content):
            card_id = match.group(1).strip()
            card_name = match.group(2).strip()

            # ディレクトリ名を カードID のみとする
            dir_name = card_id

            cards_info.append({
                'id': card_id,
                'name': card_name,
                'dir_name': dir_name
            })
        return cards_info

    def create_card_scaffold(card_info, template_content):
        """カードのフォルダとindex.mdを作成する"""
        card_dir = os.path.join(CARDS_DIR_PATH, card_info['dir_name'])
        index_path = os.path.join(card_dir, 'index.md')

        # フォルダが既に存在するかチェック
        if os.path.exists(card_dir):
            print(f"スキップ: フォルダ '{card_dir}' は既に存在します。")
            return

        try:
            # フォルダを作成
            os.makedirs(card_dir)
            print(f"作成: フォルダ '{card_dir}'")

            # テンプレートの内容をカード情報で置換
            content = template_content.replace('(例: CARD-000)', card_info['id'])
            content = content.replace('(画面名)', card_info['name'])
            content = content.replace('(WIP / In Review / Approved)', 'WIP') # 初期ステータスをWIPに

            # index.mdを書き込む
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"作成: ファイル '{index_path}'")

        except OSError as e:
            print(f"エラー: {card_dir} の作成に失敗しました - {e}")


    def main():
        """メイン処理"""
        print("DECK.mdからカードの雛形生成を開始します...")

        cards = parse_deck_file(DECK_MD_PATH)
        if not cards:
            print("DECK.mdからカード情報が見つかりませんでした。正規表現に一致する行があるか確認してください。")
            print("例: * `CARD-001`: ログイン画面")
            return

        try:
            with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
                template_content = f.read()
        except FileNotFoundError:
            print(f"エラー: テンプレートファイル {TEMPLATE_PATH} が見つかりません。")
            return

        for card in cards:
            create_card_scaffold(card, template_content)

        print("\n処理が完了しました。")

    if __name__ == "__main__":
        main()

