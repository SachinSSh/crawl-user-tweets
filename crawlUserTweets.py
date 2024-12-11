import requests
import time
import csv
import os
from typing import List, Dict, Optional

class TwitterCrawler:
    def __init__(self, bearer_token: str):
        """
        Initialize the Twitter crawler with a bearer token.
        
        :param bearer_token: OAuth 2.0 Bearer Token from X Developer Portal
        """
        self.bearer_token = bearer_token
        self.base_url = "https://api.twitter.com/2"
        self.headers = {
            "Authorization": f"Bearer {self.bearer_token}",
            "Content-Type": "application/json"
        }

    def get_user_id(self, username: str) -> Optional[str]:
        """
        Retrieve the user ID for a given username.
        
        :param username: Twitter/X username
        :return: User ID or None if not found
        """
        url = f"{self.base_url}/users/by/username/{username}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()['data']['id']
        except requests.RequestException as e:
            print(f"Error fetching user ID: {e}")
            return None

    def get_user_tweets(self, user_id: str, max_tweets: int = 1000) -> List[Dict]:
        """
        Retrieve tweets for a specific user.
        
        :param user_id: User ID to retrieve tweets for
        :param max_tweets: Maximum number of tweets to retrieve
        :return: List of tweet dictionaries
        """
        url = f"{self.base_url}/users/{user_id}/tweets"
        
        params = {
            "max_results": min(100, max_tweets),  # X API max is 100 per request
            "tweet.fields": "created_at,text,author_id,id",
            "exclude": "retweets,replies"
        }
        
        all_tweets = []
        pagination_token = None
        
        try:
            while len(all_tweets) < max_tweets:
                if pagination_token:
                    params['pagination_token'] = pagination_token
                
                response = requests.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                
                data = response.json()
                tweets = data.get('data', [])
                all_tweets.extend(tweets)
                
                # Check for pagination
                pagination_token = data.get('meta', {}).get('next_token')
                
                if not pagination_token:
                    break
                
                # Respect rate limits
                time.sleep(1)
        
        except requests.RequestException as e:
            print(f"Error fetching tweets: {e}")
        
        return all_tweets[:max_tweets]

    def save_tweets_to_csv(self, tweets: List[Dict], filename: str = 'tweets.csv'):
        """
        Save retrieved tweets to a CSV file.
        
        :param tweets: List of tweet dictionaries
        :param filename: Output CSV filename
        """
        if not tweets:
            print("No tweets to save.")
            return
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'text', 'created_at']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for tweet in tweets:
                writer.writerow({
                    'id': tweet['id'],
                    'text': tweet['text'],
                    'created_at': tweet.get('created_at', 'N/A')
                })
        
        print(f"Saved {len(tweets)} tweets to {filename}")

def main():
    # Replace with your actual bearer token from X Developer Portal
    BEARER_TOKEN = "YOUR_BEARER_TOKEN_HERE"
    
    crawler = TwitterCrawler(BEARER_TOKEN)
    
    # Example usage
    username = "ellfae"  # Replace with the desired username
    user_id = crawler.get_user_id(username)
    
    if user_id:
        tweets = crawler.get_user_tweets(user_id)
        crawler.save_tweets_to_csv(tweets)
    else:
        print("Could not retrieve user ID.")

if __name__ == "__main__":
    main()
