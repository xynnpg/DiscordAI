import requests
import json
import base64
from typing import Optional, Dict, Any, List, Union
import time

class OpenRouterClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://discord-bot-ai.com",
            "X-Title": "Discord AI Bot",
            "X-Description": "Discord AI Bot with multimodal support"
        }

        # Model-specific configurations
        self.model_configs = {
            "google/gemini-2.5-flash-image-preview:free": {
                "supports_images": True,
                "max_tokens": 8192,
                "temperature_range": [0.0, 2.0]
            },
            "google/gemini-flash-1.5:free": {
                "supports_images": True,
                "max_tokens": 8192,
                "temperature_range": [0.0, 2.0]
            },
            "openai/gpt-4o": {
                "supports_images": True,
                "max_tokens": 4096,
                "temperature_range": [0.0, 2.0]
            }
        }

    def generate_response(self, model: str, message: Union[str, List[Dict]], system_prompt: str = "You are a helpful AI assistant.", conversation_history: Optional[List[Dict[str, str]]] = None, image_data: Optional[bytes] = None) -> Optional[str]:
        """
        Generate a response using the specified model with optional conversation history and image support

        Args:
            model: The model identifier
            message: Text message or list of content objects for multimodal
            system_prompt: System instruction for the AI
            conversation_history: Previous conversation messages
            image_data: Optional image bytes for multimodal models
        """
        try:
            # Get model configuration
            model_config = self.model_configs.get(model, {})
            max_tokens = model_config.get("max_tokens", 1000)
            supports_images = model_config.get("supports_images", False)

            # Build messages array with system prompt
            messages = [{"role": "system", "content": system_prompt}]

            # Add conversation history if provided
            if conversation_history:
                messages.extend(conversation_history)

            # Handle multimodal content
            user_message = {"role": "user"}

            if isinstance(message, list):
                # Already formatted multimodal content
                user_message["content"] = message
            elif image_data and supports_images:
                # Create multimodal message with image
                image_b64 = base64.b64encode(image_data).decode('utf-8')
                user_message["content"] = [
                    {"type": "text", "text": message},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_b64}"
                        }
                    }
                ]
            else:
                # Simple text message
                user_message["content"] = message

            messages.append(user_message)

            # Build payload with model-specific optimizations
            payload = {
                "model": model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": 0.7,
                "top_p": 0.9,
                "stream": False
            }

            # Add model-specific parameters
            if "gemini" in model.lower():
                payload.update({
                    "temperature": 0.8,
                    "top_k": 40,
                    "top_p": 0.95
                })
            elif "gpt" in model.lower():
                payload.update({
                    "presence_penalty": 0.1,
                    "frequency_penalty": 0.1
                })

            # Make request with retry logic
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = requests.post(
                        f"{self.base_url}/chat/completions",
                        headers=self.headers,
                        json=payload,
                        timeout=60
                    )

                    if response.status_code == 200:
                        data = response.json()
                        if data.get('choices') and len(data['choices']) > 0:
                            content = data['choices'][0]['message']['content']
                            if content and content.strip():
                                return content.strip()
                        return None
                    elif response.status_code == 429:  # Rate limit
                        if attempt < max_retries - 1:
                            wait_time = 2 ** attempt
                            print(f"Rate limited, waiting {wait_time}s before retry...")
                            time.sleep(wait_time)
                            continue
                        else:
                            print(f"Rate limit error: {response.text}")
                            return None
                    elif response.status_code == 401:
                        print(f"Authentication error: Invalid API key")
                        return None
                    elif response.status_code == 400:
                        error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
                        error_msg = error_data.get('error', {}).get('message', response.text)
                        print(f"Bad request error: {error_msg}")
                        return None
                    else:
                        print(f"HTTP {response.status_code}: {response.text}")
                        return None

                except requests.exceptions.Timeout:
                    if attempt < max_retries - 1:
                        print(f"Request timeout, retrying... (attempt {attempt + 1})")
                        continue
                    else:
                        print(f"Request timeout after {max_retries} attempts")
                        return None

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
                timeout=15
            )

            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error fetching models: {response.status_code}")
                return None

        except Exception as e:
            print(f"Error getting models: {e}")
            return None

    def test_model_availability(self, model: str) -> bool:
        """Test if a model is available and responding"""
        try:
            test_response = self.generate_response(
                model=model,
                message="Hello! Please respond with 'OK' to confirm you're working.",
                system_prompt="You are a test assistant. Respond briefly."
            )
            return test_response is not None and len(test_response.strip()) > 0
        except Exception as e:
            print(f"Model test failed for {model}: {e}")
            return False

    def get_model_info(self, model: str) -> Dict[str, Any]:
        """Get information about a specific model"""
        config = self.model_configs.get(model, {})
        return {
            "supports_images": config.get("supports_images", False),
            "max_tokens": config.get("max_tokens", 1000),
            "temperature_range": config.get("temperature_range", [0.0, 2.0]),
            "is_multimodal": config.get("supports_images", False)
        }
