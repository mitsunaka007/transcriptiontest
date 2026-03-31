import requests
from datetime import datetime, timedelta

# --- 設定 ---
GITHUB_TOKEN = "あなたのGitHubトークン"  # 未入力でも動作しますが制限があります
SEARCH_KEYWORDS = ["japanese speech-to-text", "whisper japanese", "日本語 音声認識"]
MIN_STARS = 5  # フィルタリングする最小スター数

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
    print(f"--- {datetime.now().strftime('%Y-%m-%d')} のリサーチ結果 ---")
    found_any = False
    
    for kw in SEARCH_KEYWORDS:
        repos = search_github_repos(kw)
        for repo in repos:
            if repo['stargazers_count'] >= MIN_STARS:
                found_any = True
                print(f"【名前】: {repo['full_name']}")
                print(f"【URL】: {repo['html_url']}")
                print(f"【説明】: {repo['description']}")
                print(f"【Star】: {repo['stargazers_count']}")
                print("-" * 30)
                
    if not found_any:
        print("本日の新規アップデートはありませんでした。")

if __name__ == "__main__":
    main()