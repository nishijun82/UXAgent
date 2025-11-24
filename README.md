# UXAgent: LLMを用いたウェブデザインのユーザビリティテストをシミュレートするシステム

<p align="center">
    <a href="https://arxiv.org/abs/2504.09407">
        <img src="https://img.shields.io/badge/arXiv-2504.09407-B31B1B.svg?style=plastic&logo=arxiv" alt="arXiv">
    </a>
    <a href="https://opensource.org/licenses/MIT">
        <img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=plastic" alt="License: MIT">
    </a>
</p>

<p align="center">
Yuxuan Lu, Bingsheng Yao, Hansu Gu, Jing Huang, Jessie Wang, Laurence Li, Haiyang Zhang, Qi He, Toby Jia-Jun Li, Dakuo Wang
</p>

<p align="center">
    <img src="/figures/teaser.png" width="100%">
</p>

## 概要

**UXAgent**は、Large Language Models（LLM）をエージェントとして使用し、ウェブ環境でユーザビリティテストを実施するフレームワークです。これらのエージェントは人間のような行動をシミュレートし、UXリサーチャーが以下を実現できるようにします：

- 早期のユーザビリティ評価を実施
- 実行可能なデザインインサイトを収集
- 人間の参加者に即座に依存することなく反復作業を行う

このシステムは、迅速な意思決定と詳細な分析のために二重システム推論を活用し、**Universal Web Connector**により、あらゆるウェブページとの互換性を確保しています。リアルタイムのフィードバックを提供することで、UXAgentはデザインプロセスを効率化し、テスト効率を向上させます。

https://github.com/user-attachments/assets/8f4b352b-1c36-4b16-9d83-b39046357c40

<p align="center">
    <a href="https://uxagent.hailab.io/"> 
        <img src="https://img.shields.io/badge/Live_Demo-37a779?style=for-the-badge">
    </a>
    <a href="https://huggingface.co/datasets/NEU-HAI/UXAgent"> 
        <img src="https://img.shields.io/badge/Data-37a779?style=for-the-badge">
    </a>
</p>

---

## インストール

1. **リポジトリをクローン:**
   ```bash
   git clone git@github.com:neuhai/UXAgent.git
   ```

2. **uvをインストール**（[このガイド](https://docs.astral.sh/uv/getting-started/installation/)に従ってください）

3. **環境をセットアップ:**
   ```bash
   uv sync
   ```

4. **Playwright用のChromiumをインストール:**
   ```bash
   uv run playwright install chromium
   ```

5. **APIキーを設定:**
   ```bash
   # export AWS_ACCESS_KEY_ID=xxx123
   # export AWS_SECRET_ACCESS_KEY=xxx123
   # export OPENAI_API_KEY=sk-123
   export ANTHROPIC_API_KEY=sk-ant-123
   ```

6. **オプション: "headful"モードを有効化:**
   
   デフォルトでは、Chromeはヘッドレスモード（GUIなし）で実行されます。ブラウザを表示するには、以下を設定してください：
   ```bash
   export HEADLESS=false
   ```

---

## クイックスタート

### コマンドラインから単一のエージェントを実行

```bash
uv run -m src.simulated_web_agent.main --intent "Buy a Jacket from Amazon" --start-url "https://www.amazon.com" --max-steps 20 --wait-for-login
```

その他のオプションについては、ヘルプメッセージを参照してください：

```bash
uv run -m src.simulated_web_agent.main --help
```

### コマンドラインから複数のエージェントを実行（バッチモード）

```bash
uv run -m src.simulated_web_agent.main.run
```

`runConfig.yaml`は、バッチ実行中に**複数のシミュレートされたエージェント**がどのように起動されるか、およびエージェントが実行する行動やアンケートを定義します。`runConfig.yaml`のフィールドの使用方法については、以下の表を参照してください。

| フィールド | 説明 |
|---------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **total_personas**  | バッチ実行中に生成する仮想エージェント（ペルソナ）の総数。各ペルソナは1人のシミュレートされたユーザーを表します。 |
| **concurrency**     | 並行して実行するエージェントの数（例：`10`で最大10の同時ブラウザセッション）。 |
| **demographics**    | サンプリングカテゴリ（年齢、性別、買い物頻度など）とその相対的な重みを定義します。各ペルソナはこれらの重み付けされたオプションからランダムにサンプリングされます。 |
| **general_intent**  | すべてのエージェントの全体的なショッピングまたはウェブブラウジングの目標を説明する、短く平易な英語の指示。 |
| **example_persona** | 多様なペルソナを生成するために使用されるテンプレートペルソナプロファイル（背景、財務状況、習慣など）。生成されたすべてのペルソナは、例と同じ形式に従います。 |
| **start_url**       | 各エージェントがシミュレートされたセッションを開始するベースURL。 |
| **max_steps**       | エージェントが停止する前に実行できるアクション（クリック、ナビゲーション、フォーム入力など）の最大数。 |
| **questionnaire**   | 各エージェントに表示される実行後のユーザビリティアンケート。メタデータ（`id`、`title`）と質問のリスト（タイプ、プロンプト、オプション付き）で定義されます。 |

以下は、始めるための`runConfig.yaml`の例です：

```yaml
# ペルソナの数と並行性
total_personas: 20
concurrency: 10

# 人口統計的サンプリング（重み付けランダム）
demographics:
  - name: "年齢"
    choices:
      - { name: "18-55", weight: 1 }
  - name: "性別"
    choices:
      - { name: "男性", weight: 1 }
      - { name: "女性", weight: 1 }
      - { name: "ノンバイナリー", weight: 1 }
  - name: "オンラインショッピング頻度"
    choices:
      - { name: "年に数回", weight: 1 }
      - { name: "月に数回", weight: 1 }
      - { name: "週に数回", weight: 1 }

# すべてのエージェントの一般的なショッピング意図
general_intent: 予算100から200の範囲内で、肉代替品カテゴリーから最高評価の製品を購入してください。購入を完了する必要はなく、チェックアウトページまで進んでください。

# 生成参照用のペルソナテンプレート例
example_persona: |
  背景:
    男性、35-44歳、テクノロジー専門職、ニュージャージー在住。
  財務状況:
    安定した収入、支出には慎重。
  買い物習慣:
    月に2回オンラインで買い物、Amazon Primeを好む、ブランドに忠実だが柔軟。
  職業生活:
    テクノロジー業界でフルタイム勤務、家族との時間と趣味とのバランスの取れたライフスタイル。

# ブラウザエージェントの開始地点
start_url: http://52.91.223.130:7770/

# 許可されるエージェントアクションの最大数
max_steps: 50

# 実行後のアンケート定義
questionnaire:
  questionnaire_id: web_shopping_usability_v1
  title: システムユーザビリティ調査
  questions:
    - id: q1
      type: multiple_choice
      prompt: "このシステムを頻繁に使用したいと思います。(1 = 強く反対, 5 = 強く同意)"
      options: ["1", "2", "3", "4", "5"]
    - id: q2
      type: multiple_choice
      prompt: "このシステムは不必要に複雑だと思いました。(1 = 強く反対, 5 = 強く同意)"
      options: ["1", "2", "3", "4", "5"]
    - id: q3
      type: multiple_choice
      prompt: "このシステムは使いやすかったです。(1 = 強く反対, 5 = 強く同意)"
      options: ["1", "2", "3", "4", "5"]
    - id: q4
      type: multiple_choice
      prompt: "このシステムを使用するには技術者のサポートが必要だと思いました。(1 = 強く反対, 5 = 強く同意)"
      options: ["1", "2", "3", "4", "5"]
    - id: q5
      type: multiple_choice
      prompt: "このシステムの様々な機能はよく統合されていました。(1 = 強く反対, 5 = 強く同意)"
      options: ["1", "2", "3", "4", "5"]
```

### 複数エージェントモード用のクイック実験セットアップUIの使用

`runConfig.yaml`を通じてバッチ実行を設定するだけでなく、**Webベースのクイック実験セットアップUI**を使用して、複数のエージェントを視覚的に起動および管理することもできます。このインターフェースを使用すると、YAMLファイルを手動で編集することなく、ブラウザから直接、総ペルソナ数、並行性、意図などのパラメータを調整できます。

1. **flask**と**Node.js / npm**をインストール
2. プロジェクトのルートから：
   ```bash
   uv run -m src.simulated_web_agent.main.app
   ```
3. インターフェースを起動：
   ```bash
   cd experiment_ui
   npm install
   npm run dev
   ```
4. インターフェース内の実験設定ウィザードを通じて、マルチエージェント実行を設定できます（参加者の人口統計の設定、タスクの修正、アンケートの編集など）。UIで「Confirm and Run」をクリックして、カスタム設定されたマルチエージェント実行を開始します。

## 結果とデータ成果物

UXAgentでシミュレーションを実行すると、ログ、セッショントレース、スクリーンショット、集計メトリクスを含む構造化された出力フォルダ`runs/<timestamp>`が生成されます。

---

## ライセンス

このプロジェクトは[MITライセンス](https://opensource.org/licenses/MIT)の下でライセンスされています。

## 引用

```bibtex
@article{lu2025uxagent,
  title={UXAgent: A System for Simulating Usability Testing of Web Design with LLM Agents},
  author={Lu, Yuxuan and Yao, Bingsheng and Gu, Hansu and Huang, Jing and Wang, Jessie and Li, Yang and Gesi, Jiri and He, Qi and Li, Toby Jia-Jun and Wang, Dakuo},
  journal={arXiv preprint arXiv:2504.09407},
  year={2025}
}
```