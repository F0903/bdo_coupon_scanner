from typing import Iterable
import snscrape.modules.twitter as t
from itertools import takewhile
from .checker import CODE_REGEX, CodeChecker
from .coupon_code import CouponCode


class TwitterChecker(CodeChecker):
    MAX_TWEETS = 20

    def get_checker_name(self) -> str:
        return "official twitter"

    def check_tweet(self, tweet: t.Tweet) -> CouponCode | None:
        text = tweet.content
        result = CODE_REGEX.search(text)
        if result == None:
            return None
        link = tweet.url
        code = result.group()
        date = tweet.date.date()
        return CouponCode(code, date, link)

    def get_codes(self) -> Iterable[CouponCode]:
        profile = t.TwitterUserScraper("NewsBlackDesert")
        codes = set()
        for i, item in takewhile(
            lambda x: x[0] < self.MAX_TWEETS, enumerate(profile.get_items())
        ):
            if isinstance(item, t.Tweet):
                result = self.check_tweet(item)
                if result != None:
                    codes.add(result)
        return codes
