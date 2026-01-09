import json
import logging
import os
import random
import time
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
    def __init__(self, auth_token: str, ct0: str, twid: str, bearer_token: str, proxies: dict = None):
        self.session = requests.Session()
        # self.session.proxies(proxies)
        self.bearer_token = bearer_token
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.bearer_token}",
                "x-twitter-auth-type": "OAuth2Session",
                "x-twitter-active-user": "yes",
                "x-twitter-client-language": "en",
                "x-csrf-token": ct0,
            }
        )
        self.session.cookies.update(
            {
                "auth_token": auth_token,
                "ct0": ct0,
                "twid": twid,
            }
        )

    def _random_delay(self):
        time.sleep(random.uniform(1, 3))

    def get_user_by_screen_name(self, username: str):
        query_id = "-oaLodhGbbnzJBACb1kk2Q"
        variables = {"screen_name": username, "withSafetyModeUserFields": True}
        features = {
            "hidden_profile_subscriptions_enabled": True,
            "profile_label_improvements_pcf_label_in_post_enabled": True,
            "responsive_web_profile_redirect_enabled": False,
            "rweb_tipjar_consumption_enabled": True,
            "verified_phone_label_enabled": False,
            "subscriptions_verification_info_is_identity_verified_enabled": True,
            "subscriptions_verification_info_verified_since_enabled": True,
            "highlights_tweets_tab_ui_enabled": True,
            "responsive_web_twitter_article_notes_tab_enabled": True,
            "subscriptions_feature_can_gift_premium": True,
            "creator_subscriptions_tweet_preview_api_enabled": True,
            "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
            "responsive_web_graphql_timeline_navigation_enabled": True,
        }
        fieldtoggles = {"withPayments": False, "withAuxiliaryUserLabels": False}
        params = {
            "variables": json.dumps(variables),
            "features": json.dumps(features),
            "fieldToggles": json.dumps(fieldtoggles),
        }
        url = f"https://x.com/i/api/graphql/{query_id}/UserByScreenName?{urlencode(params)}"

        self._random_delay()
        response = self.session.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            logging.info(f"Error: {response.status_code}")
            logging.info(response.text)
            return None

    def get_user_tweets(self, user_id: str, count: int = 10):
        query_id = "-V26I6Pb5xDZ3C7BWwCQ_Q"
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
            "responsive_web_grok_analyze_post_followups_enabled": True,
            "responsive_web_jetfuel_frame": True,
            "responsive_web_grok_share_attachment_enabled": True,
            "articles_preview_enabled": True,
            "responsive_web_edit_tweet_api_enabled": True,
            "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
            "view_counts_everywhere_api_enabled": True,
            "longform_notetweets_consumption_enabled": True,
            "responsive_web_twitter_article_tweet_consumption_enabled": True,
            "tweet_awards_web_tipping_enabled": False,
            "responsive_web_grok_show_grok_translated_post": False,
            "responsive_web_grok_analysis_button_from_backend": True,
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
        }
        fieldToggles = {"withArticlePlainText": False}
        params = {
            "variables": json.dumps(variables),
            "features": json.dumps(features),
            "fieldToggles": json.dumps(fieldToggles),
        }
        url = f"https://x.com/i/api/graphql/{query_id}/UserTweets?{urlencode(params)}"

        self._random_delay()

        response = self.session.get(url=url, headers={"Accept-Encoding": "identity"})
        if response.status_code == 200:
            return response.json()
        else:
            logging.info(f"Error: {response.status_code}")
            logging.info(response.text)
            return None

    def parse_tweets(self, data: dict) -> list[dict]:
        tweets = []
        try:
            instructions = data["data"]["user"]["result"]["timeline"]["timeline"]["instructions"]
            for instruction in instructions:
                if instruction.get("type") == "TimelineAddEntries":
                    for entry in instruction.get("entries", [])[:11]:
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
                                    "created_at": legacy.get("created_at"),
                                    "retweet_count": legacy.get("retweet_count"),
                                    "favorite_count": legacy.get("favorite_count"),
                                    "reply_count": legacy.get("reply_count"),
                                    "quote_count": legacy.get("quote_count"),
                                    "views": tweet_result.get("views", {}).get(
                                        "count", 0
                                    ),
                                }
                                tweets.append(tweet_info)

        except Exception as e:
            logging.error(f"Error parsing tweets: {e}")

        return tweets


if __name__ == "__main__":
    #proxies = {
    # "http": "http://your-proxy-ip:port",
    # "https": "http://your-proxy-ip:port",
    # }

    scraper = TwitterScraper(
        auth_token=os.getenv("AUTH_TOKEN"),
        ct0=os.getenv("CT0"),
        twid=os.getenv("TWID"),
        bearer_token=os.getenv("BEARER_TOKEN"),
    )

    logging.info("Fetching user information...")
    user_data = scraper.get_user_by_screen_name("testerlabor")
    if user_data:
        user_id = user_data["data"]["user"]["result"]["rest_id"]
        user_name = user_data["data"]["user"]["result"]["core"]["name"]
        followers_count = user_data["data"]["user"]["result"]["legacy"][
            "followers_count"
        ]
        friends_count = user_data["data"]["user"]["result"]["legacy"]["friends_count"]
        logging.info(
            f"\nUser ID: {user_id}\n"
            f"User Name: {user_name}\n"
            f"Followers Count: {followers_count}\n"
            f"Friends Count: {friends_count}"
        )

        logging.info("Fetching tweets...")
        tweets_data = scraper.get_user_tweets(user_id, count=10)
        tweets = scraper.parse_tweets(tweets_data)
        if tweets_data:
            with open("tweets.txt", "w", encoding="utf-8") as f:
                for i, tweet in enumerate(tweets, 1):
                    f.write(str(tweet["text"]).replace("\n", "") + "\n")
    logging.info("Tweets saved to tweets.txt")
