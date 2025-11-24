import asyncio
import logging
from pathlib import Path

import click
from dotenv import load_dotenv
from hydra import compose, initialize, initialize_config_dir
from omegaconf import DictConfig

from ..agent import gpt
from ..executor.env import WebAgentEnv  # Playwright env
from .experiment import _run_for_persona_and_intent
from .model import AgentPolicy  # noqa


def _load_cfg():
    here = Path(__file__).resolve().parent
    conf_dir = here.parents[2] / "conf"
    with initialize_config_dir(version_base=None, config_dir=str(conf_dir)):
        cfg = compose(config_name="base")
    return cfg


@click.command()
@click.option(
    "--record/--no-record",
    default=False,
    show_default=True,
    help="セッションの記録を有効または無効にします。",
)
@click.option(
    "--headless/--headed",
    default=False,
    show_default=True,
    help="ブラウザをヘッドレスモードまたはヘッドモードで実行します。",
)
@click.option(
    "--persona",
    default="ペルソナ: Clara\n背景:\nClaraは名門大学でコンピュータサイエンスの博士課程に在籍する学生です。人工知能と機械学習に焦点を当てた研究に深く携わっており、社会に貢献できる技術の進歩に寄与することを目指しています。\n\n人口統計学的情報:\n\n年齢: 28歳\n性別: 女性\n学歴: コンピュータサイエンスの博士課程在籍中\n職業: 博士課程学生\n収入: $50,000\n\n経済状況:\nClaraは博士課程学生としての奨学金で生活しており、支出には慎重です。研究関連の費用のためにお金を貯め、学問的追求に投資することを好みます。\n\n買い物習慣:\nClaraは買い物が嫌いで、商品を閲覧することに多くの時間を費やすことを避けます。彼女は簡潔で効率的なショッピング体験を好み、利便性のためにオンラインでよく買い物をします。買い物をする時は、スタイルやトレンディさよりも実用性と手頃な価格を求めます。\nそのため、Claraは迅速かつ効率的に買い物をしたいと考えています。\n\n職業生活:\nClaraは学術活動にほとんどの時間を費やし、会議に出席し、研究室で作業し、論文を執筆しています。研究への献身が彼女の主な優先事項であり、学術的責任を中心に時間を管理しています。\n\n個人的なスタイル:\nClaraは快適で機能的な衣服を好み、デスクや研究室で長時間着用するのに適したアイテムをよく選びます。彼女はMサイズの衣服を着用し、自分の個性を反映する色を好みます—主に赤色で、これが気分を高揚させ、エネルギーを与えてくれると感じています。",
    show_default=False,
    help="ペルソナの説明文字列。",
)
@click.option(
    "--intent",
    default="AmazonのRufus機能を使用してゲーミングマウスを購入する",
    show_default=False,
    help="エージェントのユーザー意図。",
)
@click.option(
    "--start-url",
    default="http://www.amazon.com",
    show_default=True,
    help="セッションの開始URL。",
)
@click.option(
    "--max-steps",
    default=20,
    show_default=True,
    type=int,
    help="エージェントの最大ステップ数。",
)
@click.option(
    "--wait-for-login/--no-wait-for-login",
    default=False,
    show_default=True,
    help="セッションを開始する前にログインの完了を待機します。",
)
@click.option(
    "--use-user-data-dir/--no-use-user-data-dir",
    default=False,
    show_default=True,
    help="ブラウザのユーザーデータディレクトリ。",
)
def main(
    record: bool,
    headless: bool,
    persona: str,
    intent: str,
    start_url: str,
    max_steps: int,
    wait_for_login: bool,
    use_user_data_dir: bool,
) -> None:
    """
    ClickベースのCLIオプションを使用してシミュレートされたWebエージェントを実行します。
    """
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("LiteLLM").setLevel(logging.WARNING)
    logging.getLogger("LiteLLM Router").setLevel(logging.WARNING)
    cfg = _load_cfg()
    cfg.environment.recording.enabled = record
    cfg.environment.browser.launch_options.headless = headless
    gpt.provider = cfg.llm_provider
    # config.browser.user_data_dir
    if not use_user_data_dir:
        cfg.environment.browser.user_data_dir = None

    asyncio.run(
        _run_for_persona_and_intent(
            cfg=cfg,
            persona_info={
                "persona": persona,
                "intent": intent,
            },
            start_url=start_url,
            max_steps=max_steps,
            wait_for_login=wait_for_login,
        )
    )


if __name__ == "__main__":
    main()