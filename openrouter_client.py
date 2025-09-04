import requests
import json
from typing import Optional, Dict, Any, List

class OpenRouterClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://discord-bot-ai.com",
            "X-Title": "Discord AI Bot"
        }

    def generate_response(self, model: str, message: str, system_prompt: str = "You are a helpful AI assistant.", conversation_history: Optional[List[Dict[str, str]]] = None) -> Optional[str]:
        """Generate a response using the specified model with optional conversation history"""
        try:
            # Build messages array with system prompt and conversation history
            messages = [{"role": "system", "content": system_prompt}]

            # Add conversation history if provided
            if conversation_history:
                messages.extend(conversation_history)

            # Add the current user message
            messages.append({"role": "user", "content": message})

            payload = {
                "model": model,
                "messages": messages,
                "max_tokens": 1000,
                "temperature": 0.7
            }

            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                return data['choices'][0]['message']['content']
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            print(f"Error generating response: {e}")
            return None

    def get_models(self) -> Optional[Dict[str, Any]]:
        """Get available models from OpenRouter"""
        try:
            response = requests.get(
                f"{self.base_url}/models",
                headers=self.headers,
                timeout=10
            )

            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error fetching models: {response.status_code}")
                return None

        except Exception as e:
            print(f"Error getting models: {e}")
            return None
