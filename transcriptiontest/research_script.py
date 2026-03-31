import os
import requests
from datetime import datetime, timedelta

# --- 設定 ---
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
# SlackのWebhook URL（GitHubのSecretsに登録した名前と一致させてください）
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")

SEARCH_KEYWORDS = ["japanese speech-to-text", "whisper japanese", "日本語 音声認識"]
MIN_STARS = 5  # フィルタリングする最小スター数

def send_slack_notification(message):
    """
    Slackにメッセージを送信します。
    """
    if not SLACK_WEBHOOK_URL:
        print("Error: SLACK_WEBHOOK_URL が設定されていません。")
        return

    payload = {"text": message}
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=payload)
        response.raise_for_status()
        print("Slackへの通知が完了しました。")
    except requests.exceptions.RequestException as e:
        print(f"Slack送信エラー: {e}")

def search_github_repos(keyword):
    # 過去24時間以内に更新されたリポジトリを検索
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
    query = f"{keyword} pushed:>{yesterday} sort:updated-desc"
    url = f"https://api.github.com/search/repositories?q={query}"
    
    headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json().get('items', [])
    else:
        print(f"Error: {response.status_code}")
        return []

def main():
    today_str = datetime.now().strftime('%Y-%m-%d')
    print(f"--- {today_str} のリサーチ結果 ---")
    
    found_any = False
    seen_repos = set()
    slack_msg_parts = [f"*【{today_str}】日本語STTツール新着リサーチ*"]
    
    for kw in SEARCH_KEYWORDS:
        repos = search_github_repos(kw)
        for repo in repos:
            repo_full_name = repo['full_name']
            if repo['stargazers_count'] >= MIN_STARS:
                if repo_full_name in seen_repos:
                    continue
                seen_repos.add(repo_full_name)
                found_any = True
                
                # 情報の整理
                repo_url = repo['html_url']
                description = repo.get('description') or "説明なし"
                stars = repo['stargazers_count']
                
                # コンソール出力
                print(f"【名前】: {repo_full_name}")
                
                # Slackメッセージ用のテキスト構築
                slack_msg_parts.append(
                    f"• *<{repo_url}|{repo_full_name}>* (⭐ {stars})\n"
                    f"_{description}_"
                )
    
    if found_any:
        # メッセージを結合して送信
        full_message = "\n\n".join(slack_msg_parts)
        send_slack_notification(full_message)
    else:
        print("本日の新規アップデートはありませんでした。")

if __name__ == "__main__":
    main()
