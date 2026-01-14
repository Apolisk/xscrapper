import argparse
import json
import logging
import random
import re
import time
from typing import Optional
from urllib.parse import urlencode

import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("run.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

class TwitterScraper:
    def __init__(self, proxies: dict = None):
        self.session = requests.Session()
        if proxies:
            self.session.proxies.update(proxies)
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
                "x-client-transaction-id": "K5/Dr0yJcemq+ttw1DUKspl7o+Bny3boWRBVqsJqtK0u6XZjzQidXY3/TFJMuQ+s8XvpPS6QYyxXFTJNWLPss1I7vbTmKA",
                "x-twitter-active-user": "yes",
                "x-twitter-client-language": "ru",
                "content-type": "application/json",
            }
        )

        self.bearer_token = self._get_bearer_token()
        self.session.headers.update({"authorization": f"Bearer {self.bearer_token}"})

        self.guest_token = self._get_guest_token()
        self.session.headers.update({"x-guest-token": self.guest_token})

    def _get_bearer_token(self) -> str:
        url = "https://abs.twimg.com/responsive-web/client-web/main.e46e1035.js"
        try:
            response = self.session.get(url)
            bearer_token = re.search(r"s=\"([\w\%]{104})\"", response.text)[1]
            return bearer_token
        except Exception as e:
            logger.error(f"Error while reciving bearer token: {e}")
        return None

    def _get_guest_token(self) -> str:
        url = "https://api.x.com/1.1/guest/activate.json"
        try:
            response = self.session.post(url)
            if response.status_code == 200:
                token = response.json().get("guest_token")
                return token
            else:
                logger.error(response.text)
        except Exception as e:
            logger.error(f"Error while reciving guest token: {e}")
        return None

    def _random_delay(self):
        time.sleep(random.uniform(2, 4))

    def get_user_by_screen_name(self, username: Optional[str] = "elonmusk"): # or username: str = "elonmusk"
        query_id = "-oaLodhGbbnzJBACb1kk2Q"

        variables = {"screen_name": username, "withSafetyModeUserFields": True}

        features = {
            "profile_label_improvements_pcf_label_in_post_enabled": True,
            "responsive_web_profile_redirect_enabled": False,
            "rweb_tipjar_consumption_enabled": True,
            "verified_phone_label_enabled": False,
            "subscriptions_verification_info_is_identity_verified_enabled": True,
            "subscriptions_verification_info_verified_since_enabled": True,
            "hidden_profile_subscriptions_enabled": True,
            "highlights_tweets_tab_ui_enabled": True,
            "subscriptions_feature_can_gift_premium": True,
            "responsive_web_twitter_article_notes_tab_enabled": True,
            "creator_subscriptions_tweet_preview_api_enabled": True,
            "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
            "responsive_web_graphql_timeline_navigation_enabled": True,
        }

        fieldToggles = {"withPayments": False, "withAuxiliaryUserLabels": True}

        params = {
            "variables": json.dumps(variables),
            "features": json.dumps(features),
            "fieldToggles": json.dumps(fieldToggles),
        }

        url = (
            f"https://api.x.com/graphql/{query_id}/UserByScreenName?{urlencode(params)}"
        )

        self._random_delay()

        try:
            self._random_delay()
            response = self.session.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Error: {response.status_code}")
                logger.error(response.text)
                return None
        except Exception as e:
            logger.error(f"Request error: {e}")
            return None

    def get_user_tweets(self, user_id: str, count: Optional[int] = 10): # or count: int = 10
        query_id = "YtN4Mzhm80AHZL5danComw"
        variables = {
            "userId": user_id,
            "count": count,
            "includePromotedContent": True,
            "withQuickPromoteEligibilityTweetFields": True,
            "withVoice": True,
        }

        features = {
            "rweb_video_screen_enabled": False,
            "profile_label_improvements_pcf_label_in_post_enabled": True,
            "responsive_web_profile_redirect_enabled": False,
            "rweb_tipjar_consumption_enabled": True,
            "verified_phone_label_enabled": False,
            "creator_subscriptions_tweet_preview_api_enabled": True,
            "responsive_web_graphql_timeline_navigation_enabled": True,
            "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
            "premium_content_api_read_enabled": False,
            "communities_web_enable_tweet_community_results_fetch": True,
            "c9s_tweet_anatomy_moderator_badge_enabled": True,
            "responsive_web_grok_analyze_button_fetch_trends_enabled": False,
            "responsive_web_grok_analyze_post_followups_enabled": False,
            "responsive_web_jetfuel_frame": True,
            "responsive_web_grok_share_attachment_enabled": True,
            "responsive_web_grok_annotations_enabled": False,
            "articles_preview_enabled": True,
            "responsive_web_edit_tweet_api_enabled": True,
            "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
            "view_counts_everywhere_api_enabled": True,
            "longform_notetweets_consumption_enabled": True,
            "responsive_web_twitter_article_tweet_consumption_enabled": True,
            "tweet_awards_web_tipping_enabled": False,
            "responsive_web_grok_show_grok_translated_post": False,
            "responsive_web_grok_analysis_button_from_backend": True,
            "post_ctas_fetch_enabled": True,
            "creator_subscriptions_quote_tweet_preview_enabled": False,
            "freedom_of_speech_not_reach_fetch_enabled": True,
            "standardized_nudges_misinfo": True,
            "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
            "longform_notetweets_rich_text_read_enabled": True,
            "longform_notetweets_inline_media_enabled": True,
            "responsive_web_grok_image_annotation_enabled": True,
            "responsive_web_grok_imagine_annotation_enabled": True,
            "responsive_web_grok_community_note_auto_translation_is_enabled": False,
            "responsive_web_enhance_cards_enabled": False,
            "responsive_web_twitter_article_notes_tab_enabled": True,
            "subscriptions_verification_info_verified_since_enabled": True,
            "subscriptions_verification_info_is_identity_verified_enabled": True,
            "hidden_profile_subscriptions_enabled": True,
            "highlights_tweets_tab_ui_enabled": True,
            "subscriptions_feature_can_gift_premium": True,
        }

        fieldToggles = {"withArticlePlainText": False}

        params = {
            "variables": json.dumps(variables),
            "features": json.dumps(features),
            "fieldToggles": json.dumps(fieldToggles),
        }

        url = f"https://api.x.com/graphql/{query_id}/UserTweets?{urlencode(params)}"

        self._random_delay()

        try:
            response = self.session.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Error: {response.status_code}")
                logger.error(response.text)
                return None
        except Exception as e:
            logger.error(f"Request error: {e}")
            return None

    def parse_tweets(self, data: dict, count: int) -> list[dict]:
        tweets = []
        try:
            instructions = data["data"]["user"]["result"]["timeline"]["timeline"]["instructions"]
            for instruction in instructions:
                if instruction.get("type") == "TimelineAddEntries":
                    for entry in instruction.get("entries", [])[:count]:
                        if "tweet-" in entry.get("entryId", ""):
                            item_content = entry.get("content", {}).get(
                                "itemContent", {}
                            )
                            tweet_results = item_content.get("tweet_results", {})
                            tweet_result = tweet_results.get("result", {})

                            legacy = tweet_result.get("legacy")
                            if legacy:
                                tweet_info = {
                                    "id": legacy.get("id_str"),
                                    "text": legacy.get("full_text"),
                                }
                                tweets.append(tweet_info)

        except Exception as e:
            logging.error(f"Error parsing tweets: {e}")

        return tweets


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Twitter scraper")
    parser.add_argument(
        "--username", type=str, default="elonmusk", help="Twitter username (without @)"
    )
    parser.add_argument(
        "--count", type=int, default=10, help="Number of tweets to fetch (default: 10)"
    )

    parser.add_argument(
        "--proxy", default=None, help="Proxy URL, example: http://ip:port"
    )

    args = parser.parse_args()
    proxies = None
    if args.proxy:
        proxies = {
            "http": args.proxy,
        }

    scraper = TwitterScraper(proxies=proxies)

    logging.info("Fetching profile information...")
    user_data = scraper.get_user_by_screen_name(username=args.username)
    if user_data:
        user_id = user_data["data"]["user"]["result"]["rest_id"]
        user_name = user_data["data"]["user"]["result"]["core"]["name"]
        logging.info(f"\nUser ID: {user_id}\n" f"User Name: {user_name}\n")

        logging.info("Fetching tweets...")
        tweets_data = scraper.get_user_tweets(user_id, count=args.count)
        tweets = scraper.parse_tweets(tweets_data, count=args.count)
        if tweets_data:
            with open("tweets.txt", "w", encoding="utf-8") as f:
                for i, tweet in enumerate(tweets, 1):
                    f.write(str(tweet["text"]).replace("\n", "") + "\n")
    logging.info("Tweets saved to tweets.txt")
