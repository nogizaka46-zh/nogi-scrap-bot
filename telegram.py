import telebot
import json
from time import sleep
from dataclasses import dataclass, field


@dataclass
class NogiBot():
    chat_id: str = "-860326913"
    api_token: str = "5654645197:AAHpnP4NW9-QwqMm8gIUExvq7swbgL2afvU"
    bot: telebot.TeleBot = field(init=False)

    def __post_init__(self):
        self.bot = telebot.TeleBot(self.api_token)

    def post_message(self, payload) -> None:
        try:
            markdown = f"""
#{ payload["author"] } 「{ payload["title"] }」

{ payload["date"] }

{ payload["link"] }
            """
            self.bot.send_message(
                self.chat_id,
                markdown,
                parse_mode="Markdown",
                disable_web_page_preview=True
            )
        except telebot.apihelper.ApiException as e:
            error = json.loads(e.result.text)
            print(error)
            # if error['error_code'] == 429:
            #     delay = error['parameters']['retry_after']
            #     print(delay)
            #     sleep(delay + 5)
            #     self.bot.send_message(
            #         self.chat_id,
            #         f"{text} {e}",
            #         disable_web_page_preview=True)
            #     send_text(
            #         chat_id,
            #         text,
            #         markup=markup,
            #         disable_web_page_preview=disable_web_page_preview)
            # elif error['error_code'] == 400 and 'group send failed' in error['description']:
            #     sleep(5)
            #     send_text(
            #         chat_id,
            #         f"{text} {e}",
            #         disable_web_page_preview=True)
            #     send_text(
            #         chatid,
            #         text,
            #         markup=markup,
            #         disable_web_page_preview=disable_web_page_preview)
