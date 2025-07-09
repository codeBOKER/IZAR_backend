import requests
import time
import logging
from django.conf import settings
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

def upload_image_to_imgur(image_file, max_retries=3):
    """Uploads an image file to Imgur with retry logic and error handling."""
    
    if not settings.IMGUR_CLIENT_ID:
        logger.error("IMGUR_CLIENT_ID not configured")
        return None
    
    # Reset file pointer to beginning
    image_file.seek(0)
    image_data = image_file.read()
    
    # Setup session with retry strategy
    session = requests.Session()
    retry_strategy = Retry(
        total=max_retries,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["POST"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    headers = {
        'Authorization': f'Client-ID {settings.IMGUR_CLIENT_ID}',
        'User-Agent': 'IZAR-Backend/1.0'
    }
    
    for attempt in range(max_retries + 1):
        try:
            files = {'image': image_data}
            response = session.post(
                'https://api.imgur.com/3/image', 
                headers=headers, 
                files=files,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and 'link' in data['data']:
                    logger.info(f"Successfully uploaded image to Imgur: {data['data']['link']}")
                    return data['data']['link']
                else:
                    logger.error(f"Unexpected Imgur response format: {data}")
                    
            elif response.status_code == 429:  # Rate limited
                wait_time = 2 ** attempt
                logger.warning(f"Rate limited by Imgur, waiting {wait_time}s before retry {attempt + 1}")
                if attempt < max_retries:
                    time.sleep(wait_time)
                    continue
                    
            else:
                logger.error(f"Imgur upload failed with status {response.status_code}: {response.text}")
                
        except requests.exceptions.Timeout:
            logger.warning(f"Imgur upload timeout on attempt {attempt + 1}")
            if attempt < max_retries:
                time.sleep(2 ** attempt)
                continue
                
        except requests.exceptions.ConnectionError as e:
            logger.warning(f"Connection error on attempt {attempt + 1}: {str(e)}")
            if attempt < max_retries:
                time.sleep(2 ** attempt)
                continue
                
        except Exception as e:
            logger.error(f"Unexpected error during Imgur upload: {str(e)}")
            break
    
    logger.error(f"Failed to upload image to Imgur after {max_retries + 1} attempts")
    return None

def handle_image_upload_failure(model_instance, field_name='image'):
    """Handle cases where image upload fails by setting a default or None."""
    logger.warning(f"Setting {field_name} to None for {model_instance.__class__.__name__} due to upload failure")
    setattr(model_instance, field_name, None)
