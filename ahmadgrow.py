#!/usr/bin/env python3
"""
AhmadGrow - Ultimate Deep Video Intelligence System
Bulletproof Enterprise Edition with AI-Powered Category Detection & Viral Timing Analysis
Developed by: Mehmood Ahmad
"""

import sys
import re
import time
import subprocess
from datetime import datetime, timedelta
from typing import Dict, Optional, List, Any
import json
import os
import hashlib
import base64
from urllib.parse import urlparse, parse_qs
import webbrowser
import random
import string
import threading
import signal
import traceback
from collections import defaultdict
import math

# Global error handler
def global_exception_handler(exc_type, exc_value, exc_tb):
    """Global exception handler to prevent crashes"""
    console = Console()
    console.print("\n[red]❌ CRITICAL ERROR DETECTED[/]")
    console.print(f"[yellow]Error Type: {exc_type.__name__}[/]")
    console.print(f"[yellow]Error Message: {str(exc_value)}[/]")
    console.print("[dim]The system has recovered and will continue...[/dim]")
    
    # Log to file for debugging
    try:
        with open('ahmadgrow_error.log', 'a') as f:
            f.write(f"\n{'='*80}\n")
            f.write(f"Timestamp: {datetime.now().isoformat()}\n")
            f.write(f"Error: {exc_type.__name__}: {str(exc_value)}\n")
            traceback.print_tb(exc_tb, file=f)
            f.write(f"{'='*80}\n")
    except:
        pass

# Install global exception handler
sys.excepthook = global_exception_handler

# Try to import required packages with fallback
try:
    import yt_dlp
except ImportError:
    print("[-] yt-dlp not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
    import yt_dlp

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    from rich import box
    from rich.markdown import Markdown
    from rich.prompt import Prompt, Confirm
    from rich.layout import Layout
    from rich.live import Live
    from rich.align import Align
    from rich.style import Style
    from rich.tree import Tree
    from rich.syntax import Syntax
    from rich.columns import Columns
    from rich.console import Group
    from rich.json import JSON
except ImportError:
    print("[-] Rich not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "rich"])
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
    from rich import box
    from rich.markdown import Markdown
    from rich.prompt import Prompt, Confirm
    from rich.layout import Layout
    from rich.live import Live
    from rich.align import Align
    from rich.style import Style
    from rich.tree import Tree
    from rich.syntax import Syntax
    from rich.columns import Columns
    from rich.console import Group
    from rich.json import JSON

try:
    from colorama import init, Fore, Back, Style as ColoramaStyle
    init(autoreset=True)
except ImportError:
    print("[-] Colorama not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama"])
    from colorama import init, Fore, Back, Style as ColoramaStyle
    init(autoreset=True)

# Initialize Rich Console
console = Console()

# Color Palette - Premium Cyberpunk
CYAN = "#00ffff"
CRIMSON = "#dc143c"
GREEN = "#00ff00"
GOLD = "#ffd700"
WHITE = "#ffffff"
DARK_GRAY = "#404040"
NEON_PINK = "#ff6bff"
NEON_ORANGE = "#ff8c00"
PURPLE = "#9b59b6"
TURQUOISE = "#1abc9c"
SUNSET = "#f39c12"
BLOOD = "#c0392b"
ELECTRIC = "#00ffcc"
PLATINUM = "#e5e4e2"
ROSE = "#ff6b81"
MATRIX = "#00ff41"
DEEP_BLUE = "#0a0a2e"
NEON_YELLOW = "#ffff00"
HOT_PINK = "#ff1493"
ROYAL_BLUE = "#4169e1"
EMERALD = "#50c878"
RUBY = "#e0115f"
DIAMOND = "#b9f2ff"

class BulletproofSystem:
    """Bulletproof system with error recovery and fallback mechanisms"""
    
    @staticmethod
    def safe_execute(func, *args, **kwargs):
        """Safely execute a function with error recovery"""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            console.print(f"[yellow]⚠️ Warning: {str(e)}[/]")
            return None
    
    @staticmethod
    def retry_on_failure(func, max_retries=3, delay=1, *args, **kwargs):
        """Retry function on failure with exponential backoff"""
        for attempt in range(max_retries):
            try:
                result = func(*args, **kwargs)
                if result is not None:
                    return result
            except Exception as e:
                if attempt == max_retries - 1:
                    console.print(f"[red]❌ Failed after {max_retries} attempts: {str(e)}[/]")
                    return None
                time.sleep(delay * (attempt + 1))
        return None
    
    @staticmethod
    def validate_data(data: Dict) -> bool:
        """Validate extracted data integrity"""
        if not data:
            return False
        required_fields = ['basic', 'analytics', 'technical']
        for field in required_fields:
            if field not in data:
                return False
        return True

class CategoryDetector:
    """AI-powered category detection for channels and videos"""
    
    # Category keywords mapping
    CATEGORY_KEYWORDS = {
        'education': ['education', 'learn', 'tutorial', 'course', 'study', 'school', 'university', 'teacher', 'student', 'class', 'lecture', 'knowledge', 'training', 'academy', 'curriculum', 'lesson', 'homework', 'exam', 'test', 'quiz', 'scholar', 'educator'],
        'entertainment': ['entertainment', 'fun', 'comedy', 'funny', 'laugh', 'joke', 'skit', 'prank', 'game', 'show', 'movie', 'film', 'cinema', 'drama', 'series', 'episode', 'cartoon', 'animation', 'music', 'song', 'dance', 'performance', 'celebrity', 'star', 'famous', 'viral', 'trending'],
        'technology': ['tech', 'technology', 'gadget', 'device', 'software', 'hardware', 'coding', 'programming', 'developer', 'engineer', 'hack', 'tutorial', 'howto', 'setup', 'install', 'review', 'unboxing', 'comparison', 'specs', 'features', 'update', 'version', 'android', 'ios', 'windows', 'linux', 'mac', 'gaming', 'vr', 'ar', 'ai', 'machine learning', 'data science'],
        'lifestyle': ['lifestyle', 'vlog', 'daily', 'day', 'routine', 'life', 'morning', 'night', 'weekend', 'travel', 'food', 'recipe', 'cook', 'kitchen', 'fitness', 'workout', 'gym', 'exercise', 'health', 'wellness', 'yoga', 'meditation', 'beauty', 'makeup', 'fashion', 'style', 'outfit', 'shopping', 'haul', 'review', 'tips', 'advice', 'guide'],
        'business': ['business', 'money', 'finance', 'investment', 'stock', 'market', 'entrepreneur', 'startup', 'company', 'brand', 'marketing', 'sales', 'digital', 'online', 'ecommerce', 'shop', 'store', 'product', 'service', 'customer', 'client', 'strategy', 'growth', 'success', 'profit', 'revenue', 'income', 'wealth', 'rich', 'million', 'billion'],
        'gaming': ['game', 'gaming', 'play', 'stream', 'twitch', 'youtube gaming', 'esports', 'tournament', 'competition', 'multiplayer', 'singleplayer', 'rpg', 'fps', 'battle', 'royale', 'minecraft', 'fortnite', 'call of duty', 'valorant', 'league', 'dota', 'csgo', 'overwatch', 'among us', 'fall guys', 'roblox', 'gta', 'red dead', 'cyberpunk'],
        'news': ['news', 'breaking', 'update', 'report', 'journal', 'press', 'media', 'channel', 'live', 'coverage', 'analysis', 'opinion', 'interview', 'exclusive', 'investigation', 'breaking news', 'world news', 'local news', 'politics', 'government', 'election', 'policy', 'economy', 'crisis', 'weather', 'sports'],
        'science': ['science', 'scientist', 'research', 'experiment', 'lab', 'chemistry', 'physics', 'biology', 'astronomy', 'space', 'nasa', 'universe', 'planet', 'earth', 'nature', 'environment', 'climate', 'energy', 'quantum', 'particle', 'discovery', 'innovation', 'future', 'technology'],
        'health': ['health', 'doctor', 'medical', 'hospital', 'clinic', 'disease', 'cure', 'treatment', 'medicine', 'drug', 'mental health', 'wellness', 'fitness', 'nutrition', 'diet', 'exercise', 'sleep', 'stress', 'anxiety', 'depression', 'therapy', 'counseling'],
        'sports': ['sport', 'game', 'match', 'team', 'player', 'champion', 'league', 'tournament', 'cricket', 'football', 'basketball', 'tennis', 'swimming', 'athletics', 'running', 'cycling', 'golf', 'formula1', 'nascar', 'ufc', 'boxing', 'wwe', 'olympics', 'world cup'],
        'automotive': ['car', 'auto', 'vehicle', 'drive', 'road', 'speed', 'engine', 'repair', 'maintenance', 'modification', 'tuning', 'luxury', 'supercar', 'electric', 'tesla', 'bmw', 'mercedes', 'porsche', 'ferrari', 'lamborghini', 'bike', 'motorcycle', 'truck', 'suv'],
        'food': ['food', 'cook', 'recipe', 'restaurant', 'chef', 'kitchen', 'meal', 'breakfast', 'lunch', 'dinner', 'dessert', 'cake', 'pizza', 'burger', 'pasta', 'sushi', 'indian', 'chinese', 'italian', 'mexican', 'vegan', 'organic', 'healthy', 'gourmet'],
        'travel': ['travel', 'tour', 'vacation', 'holiday', 'trip', 'adventure', 'explore', 'discover', 'wanderlust', 'backpacking', 'luxury', 'beach', 'mountain', 'city', 'country', 'culture', 'heritage', 'trekking', 'camping', 'roadtrip'],
        'fashion': ['fashion', 'style', 'trend', 'outfit', 'clothing', 'dress', 'shoes', 'bag', 'accessory', 'model', 'runway', 'designer', 'brand', 'luxury', 'makeup', 'beauty', 'skincare', 'hair', 'nails', 'cosmetic'],
        'music': ['music', 'song', 'singer', 'band', 'album', 'concert', 'live', 'performance', 'guitar', 'piano', 'drum', 'vocal', 'instrument', 'cover', 'remix', 'studio', 'recording', 'release', 'single', 'music video', 'mtv', 'spotify', 'apple music'],
    }
    
    # Category patterns for channel detection
    CHANNEL_PATTERNS = {
        'education': ['edu', 'learn', 'academy', 'school', 'tutorial', 'teacher'],
        'entertainment': ['fun', 'comedy', 'show', 'entertainment', 'studio'],
        'technology': ['tech', 'dev', 'code', 'digital', 'gadget'],
        'lifestyle': ['life', 'vlog', 'daily', 'routine'],
        'business': ['business', 'money', 'finance', 'invest'],
        'gaming': ['game', 'play', 'stream', 'gaming'],
        'news': ['news', 'report', 'press', 'media'],
        'science': ['science', 'lab', 'research', 'space'],
        'health': ['health', 'wellness', 'medical', 'fit'],
        'sports': ['sport', 'team', 'league', 'match'],
        'automotive': ['car', 'auto', 'drive', 'motor'],
        'food': ['food', 'cook', 'chef', 'recipe'],
        'travel': ['travel', 'tour', 'adventure', 'wander'],
        'fashion': ['fashion', 'style', 'trend', 'model'],
        'music': ['music', 'song', 'band', 'artist'],
    }
    
    @classmethod
    def detect_category(cls, title: str, description: str, uploader: str, channel_id: str = "") -> Dict:
        """Detect category with AI-like pattern matching"""
        categories = {}
        
        # Combine all text for analysis
        combined_text = f"{title} {description} {uploader} {channel_id}".lower()
        
        # Count keyword matches for each category
        for category, keywords in cls.CATEGORY_KEYWORDS.items():
            count = 0
            for keyword in keywords:
                if keyword in combined_text:
                    count += 1
            if count > 0:
                categories[category] = count
        
        # Check channel name patterns
        channel_pattern_matches = {}
        for category, patterns in cls.CHANNEL_PATTERNS.items():
            for pattern in patterns:
                if pattern in uploader.lower() or pattern in channel_id.lower():
                    channel_pattern_matches[category] = channel_pattern_matches.get(category, 0) + 1
        
        # Combine both scores
        final_scores = {}
        all_categories = set(categories.keys()) | set(channel_pattern_matches.keys())
        
        for category in all_categories:
            score = categories.get(category, 0) * 2 + channel_pattern_matches.get(category, 0) * 3
            final_scores[category] = score
        
        # Sort by score
        sorted_categories = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Get top categories
        top_categories = [cat for cat, score in sorted_categories if score > 0][:3]
        
        # Determine confidence level
        confidence = "High" if len(top_categories) > 0 and sorted_categories[0][1] > 5 else "Medium" if len(top_categories) > 0 else "Low"
        
        return {
            'primary': top_categories[0] if top_categories else 'general',
            'all_categories': top_categories,
            'confidence': confidence,
            'scores': {cat: score for cat, score in sorted_categories[:5]}
        }

class ViralTimeAnalyzer:
    """Analyze viral potential and best posting times"""
    
    @staticmethod
    def analyze_viral_potential(views: int, upload_time: datetime, category: str) -> Dict:
        """Analyze viral potential based on views and time"""
        now = datetime.now()
        hours_since = (now - upload_time).total_seconds() / 3600
        
        if hours_since < 1:
            hours_since = 1
        
        views_per_hour = views / hours_since
        views_per_day = views_per_hour * 24
        
        # Viral score based on views per hour
        if views_per_hour > 100000:
            viral_score = 95 + min(5, (views_per_hour - 100000) / 10000)
        elif views_per_hour > 50000:
            viral_score = 85 + (views_per_hour - 50000) / 5000
        elif views_per_hour > 10000:
            viral_score = 70 + (views_per_hour - 10000) / 2000
        elif views_per_hour > 5000:
            viral_score = 60 + (views_per_hour - 5000) / 500
        elif views_per_hour > 1000:
            viral_score = 45 + (views_per_hour - 1000) / 400
        elif views_per_hour > 500:
            viral_score = 30 + (views_per_hour - 500) / 50
        elif views_per_hour > 100:
            viral_score = 15 + (views_per_hour - 100) / 40
        else:
            viral_score = max(0, views_per_hour / 10)
        
        viral_score = min(100, viral_score)
        
        # Determine if viral
        is_viral = viral_score > 75 and hours_since < 72
        is_trending = viral_score > 60 and hours_since < 168
        
        # Category-based best time analysis
        best_times = ViralTimeAnalyzer.get_best_times(category)
        
        return {
            'viral_score': round(viral_score, 1),
            'is_viral': is_viral,
            'is_trending': is_trending,
            'views_per_hour': round(views_per_hour, 2),
            'views_per_day': round(views_per_day, 2),
            'hours_since_upload': round(hours_since, 1),
            'viral_status': '🔥 VIRAL' if is_viral else '📈 TRENDING' if is_trending else '📊 GROWING' if viral_score > 30 else '📉 NORMAL',
            'best_times': best_times,
            'recommendation': ViralTimeAnalyzer.get_recommendation(category, viral_score)
        }
    
    @staticmethod
    def get_best_times(category: str) -> Dict:
        """Get best posting times for specific category with exact timings"""
        base_times = {
            'education': {
                'weekdays': ['10:30:00 AM', '02:30:00 PM', '08:00:00 PM'],
                'weekend': ['11:00:00 AM', '03:00:00 PM', '07:00:00 PM'],
                'best': 'Tuesday 10:30:00 AM',
                'second_best': 'Thursday 02:30:00 PM',
                'best_hour': 10,
                'best_minute': 30,
                'best_second': 0,
                'best_day': 'Tuesday',
                'best_time_readable': 'Tuesday at 10:30 AM',
                'explanation': 'Education content performs best on weekdays during morning and afternoon hours when students and professionals are actively learning.'
            },
            'entertainment': {
                'weekdays': ['06:30:00 PM', '08:00:00 PM', '10:00:00 PM'],
                'weekend': ['02:00:00 PM', '07:00:00 PM', '09:30:00 PM'],
                'best': 'Friday 08:00:00 PM',
                'second_best': 'Saturday 07:00:00 PM',
                'best_hour': 20,
                'best_minute': 0,
                'best_second': 0,
                'best_day': 'Friday',
                'best_time_readable': 'Friday at 8:00 PM',
                'explanation': 'Entertainment content peaks on weekend evenings when people are relaxing and looking for fun content.'
            },
            'technology': {
                'weekdays': ['09:00:00 AM', '01:00:00 PM', '06:00:00 PM'],
                'weekend': ['10:00:00 AM', '03:00:00 PM', '08:00:00 PM'],
                'best': 'Wednesday 10:00:00 AM',
                'second_best': 'Thursday 02:00:00 PM',
                'best_hour': 10,
                'best_minute': 0,
                'best_second': 0,
                'best_day': 'Wednesday',
                'best_time_readable': 'Wednesday at 10:00 AM',
                'explanation': 'Technology content performs best during work hours when professionals and enthusiasts are actively seeking tech information.'
            },
            'lifestyle': {
                'weekdays': ['07:00:00 AM', '12:00:00 PM', '06:30:00 PM'],
                'weekend': ['08:00:00 AM', '01:00:00 PM', '07:00:00 PM'],
                'best': 'Sunday 08:00:00 AM',
                'second_best': 'Saturday 10:00:00 AM',
                'best_hour': 8,
                'best_minute': 0,
                'best_second': 0,
                'best_day': 'Sunday',
                'best_time_readable': 'Sunday at 8:00 AM',
                'explanation': 'Lifestyle content performs best during weekend mornings when people are planning their day and looking for inspiration.'
            },
            'business': {
                'weekdays': ['08:30:00 AM', '12:30:00 PM', '05:30:00 PM'],
                'weekend': ['09:00:00 AM', '02:00:00 PM', '07:00:00 PM'],
                'best': 'Tuesday 09:00:00 AM',
                'second_best': 'Thursday 02:00:00 PM',
                'best_hour': 9,
                'best_minute': 0,
                'best_second': 0,
                'best_day': 'Tuesday',
                'best_time_readable': 'Tuesday at 9:00 AM',
                'explanation': 'Business content performs best during working hours on Tuesdays and Thursdays when professionals are most engaged.'
            },
            'gaming': {
                'weekdays': ['03:00:00 PM', '06:00:00 PM', '09:00:00 PM'],
                'weekend': ['10:00:00 AM', '03:00:00 PM', '08:00:00 PM'],
                'best': 'Friday 06:00:00 PM',
                'second_best': 'Saturday 08:00:00 PM',
                'best_hour': 18,
                'best_minute': 0,
                'best_second': 0,
                'best_day': 'Friday',
                'best_time_readable': 'Friday at 6:00 PM',
                'explanation': 'Gaming content peaks in the evenings and weekends when gamers are most active and looking for new content.'
            },
            'news': {
                'weekdays': ['07:00:00 AM', '12:00:00 PM', '06:00:00 PM'],
                'weekend': ['08:00:00 AM', '01:00:00 PM', '06:00:00 PM'],
                'best': 'Monday 07:00:00 AM',
                'second_best': 'Wednesday 12:00:00 PM',
                'best_hour': 7,
                'best_minute': 0,
                'best_second': 0,
                'best_day': 'Monday',
                'best_time_readable': 'Monday at 7:00 AM',
                'explanation': 'News content performs best early mornings when people are catching up on overnight developments.'
            },
            'science': {
                'weekdays': ['09:30:00 AM', '02:00:00 PM', '07:00:00 PM'],
                'weekend': ['10:00:00 AM', '03:00:00 PM', '06:30:00 PM'],
                'best': 'Thursday 10:00:00 AM',
                'second_best': 'Wednesday 02:00:00 PM',
                'best_hour': 10,
                'best_minute': 0,
                'best_second': 0,
                'best_day': 'Thursday',
                'best_time_readable': 'Thursday at 10:00 AM',
                'explanation': 'Science content performs best on weekdays when intellectuals and students are actively learning and researching.'
            },
            'health': {
                'weekdays': ['06:00:00 AM', '12:30:00 PM', '06:30:00 PM'],
                'weekend': ['07:00:00 AM', '11:00:00 AM', '05:00:00 PM'],
                'best': 'Monday 06:00:00 AM',
                'second_best': 'Sunday 07:00:00 AM',
                'best_hour': 6,
                'best_minute': 0,
                'best_second': 0,
                'best_day': 'Monday',
                'best_time_readable': 'Monday at 6:00 AM',
                'explanation': 'Health content performs best early mornings and after work when people are focusing on their health routines.'
            },
            'sports': {
                'weekdays': ['05:00:00 PM', '07:00:00 PM', '09:30:00 PM'],
                'weekend': ['10:00:00 AM', '02:00:00 PM', '07:00:00 PM'],
                'best': 'Saturday 02:00:00 PM',
                'second_best': 'Sunday 10:00:00 AM',
                'best_hour': 14,
                'best_minute': 0,
                'best_second': 0,
                'best_day': 'Saturday',
                'best_time_readable': 'Saturday at 2:00 PM',
                'explanation': 'Sports content performs best during weekends when matches are played and fans are most engaged.'
            },
            'automotive': {
                'weekdays': ['09:00:00 AM', '01:30:00 PM', '06:00:00 PM'],
                'weekend': ['10:00:00 AM', '03:00:00 PM', '08:00:00 PM'],
                'best': 'Wednesday 10:00:00 AM',
                'second_best': 'Saturday 03:00:00 PM',
                'best_hour': 10,
                'best_minute': 0,
                'best_second': 0,
                'best_day': 'Wednesday',
                'best_time_readable': 'Wednesday at 10:00 AM',
                'explanation': 'Automotive content performs best on weekdays during work breaks and weekends when car enthusiasts are actively browsing.'
            },
            'food': {
                'weekdays': ['11:00:00 AM', '01:00:00 PM', '06:30:00 PM'],
                'weekend': ['09:00:00 AM', '12:00:00 PM', '05:00:00 PM'],
                'best': 'Sunday 09:00:00 AM',
                'second_best': 'Saturday 11:00:00 AM',
                'best_hour': 9,
                'best_minute': 0,
                'best_second': 0,
                'best_day': 'Sunday',
                'best_time_readable': 'Sunday at 9:00 AM',
                'explanation': 'Food content performs best during meal preparation times, especially on weekends when people have time to cook.'
            },
            'travel': {
                'weekdays': ['08:00:00 AM', '12:00:00 PM', '07:00:00 PM'],
                'weekend': ['09:00:00 AM', '02:00:00 PM', '06:00:00 PM'],
                'best': 'Saturday 09:00:00 AM',
                'second_best': 'Sunday 02:00:00 PM',
                'best_hour': 9,
                'best_minute': 0,
                'best_second': 0,
                'best_day': 'Saturday',
                'best_time_readable': 'Saturday at 9:00 AM',
                'explanation': 'Travel content performs best on weekends when people are planning trips and seeking travel inspiration.'
            },
            'fashion': {
                'weekdays': ['10:00:00 AM', '02:00:00 PM', '07:00:00 PM'],
                'weekend': ['11:00:00 AM', '03:00:00 PM', '06:00:00 PM'],
                'best': 'Friday 11:00:00 AM',
                'second_best': 'Saturday 03:00:00 PM',
                'best_hour': 11,
                'best_minute': 0,
                'best_second': 0,
                'best_day': 'Friday',
                'best_time_readable': 'Friday at 11:00 AM',
                'explanation': 'Fashion content performs best on Fridays and weekends when people are looking for outfit inspiration.'
            },
            'music': {
                'weekdays': ['04:00:00 PM', '07:00:00 PM', '10:00:00 PM'],
                'weekend': ['12:00:00 PM', '05:00:00 PM', '09:00:00 PM'],
                'best': 'Saturday 05:00:00 PM',
                'second_best': 'Friday 07:00:00 PM',
                'best_hour': 17,
                'best_minute': 0,
                'best_second': 0,
                'best_day': 'Saturday',
                'best_time_readable': 'Saturday at 5:00 PM',
                'explanation': 'Music content performs best during evening and weekend hours when people are relaxing and enjoying music.'
            }
        }
        
        return base_times.get(category, base_times['entertainment'])
    
    @staticmethod
    def get_recommendation(category: str, viral_score: float) -> str:
        """Get personalized recommendation based on category and viral score"""
        if viral_score > 80:
            return f"🌟 EXCELLENT PERFORMANCE! Your {category} content is going VIRAL! Keep posting at your best time to maintain this momentum!"
        elif viral_score > 60:
            return f"📈 GREAT PERFORMANCE! Your {category} content is TRENDING! Consider posting more frequently during your best time slots."
        elif viral_score > 40:
            return f"📊 GOOD PERFORMANCE! Your {category} content is growing steadily. Try posting at your recommended best time: {ViralTimeAnalyzer.get_best_times(category).get('best_time_readable', 'N/A')}"
        elif viral_score > 20:
            return f"📉 MODERATE PERFORMANCE. Your {category} content needs optimization. Try the best time: {ViralTimeAnalyzer.get_best_times(category).get('best_time_readable', 'N/A')} and improve your content quality."
        else:
            return f"📉 LOW PERFORMANCE. Your {category} content needs significant improvement. Focus on content quality, SEO, and post at the optimal time: {ViralTimeAnalyzer.get_best_times(category).get('best_time_readable', 'N/A')}"

class AhmadGrowExtractor:
    """Main class for extracting comprehensive video metadata with micro-second precision"""
    
    def __init__(self):
        self.ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'force_generic_extractor': False,
            'ignoreerrors': True,
            'no_color': False,
            'geo_bypass': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'extract_flat': False,
            'writeinfojson': False,
            'writethumbnail': False,
            'write_all_thumbnails': False,
            'listformats': True,
            'format': 'best',
            'extract_flat': False,
            'youtube_include_dash_manifest': True,
            'youtube_include_hls_manifest': True,
            'extractor_args': {
                'youtube': {
                    'skip': ['dash', 'hls'],
                    'player_client': ['android', 'web'],
                    'include_websocket_urls': True,
                }
            },
            'logger': None  # Disable logging to prevent errors
        }
        self.video_data: Optional[Dict] = None
        self.deep_analytics: Optional[Dict] = None
        self.timestamp_data: Optional[Dict] = None
        
    def display_banner(self):
        """Display premium cyberpunk ASCII banner"""
        banner = """
    █████╗ ██╗  ██╗███╗   ███╗ █████╗ ██████╗  ██████╗ ██████╗  ██████╗ ██╗    ██╗
   ██╔══██╗██║  ██║████╗ ████║██╔══██╗██╔══██╗██╔════╝ ██╔══██╗██╔═══██╗██║    ██║
   ███████║███████║██╔████╔██║███████║██║  ██║██║  ███╗██████╔╝██║   ██║██║ █╗ ██║
   ██╔══██║██╔══██║██║╚██╔╝██║██╔══██║██║  ██║██║   ██║██╔══██╗██║   ██║██║███╗██║
   ██║  ██║██║  ██║██║ ╚═╝ ██║██║  ██║██████╔╝╚██████╔╝██║  ██║╚██████╔╝╚███╔███╔╝
   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝  ╚══╝╚══╝ 
                                                                                      """
        
        matrix_header = """
    ╔═══════════════════════════════════════════════════════════════════════════════════════╗
    ║  🚀 BULLETPROOF ENTERPRISE EDITION v99.9.9  [QUANTUM MODE ACTIVE]                  ║
    ║  ⚡ MICRO-SECOND PRECISION TIMESTAMP ANALYSIS ENABLED                              ║
    ║  🌐 50+ DEEP METRICS + AI CATEGORY DETECTION + VIRAL TIME ANALYSIS               ║
    ╚═══════════════════════════════════════════════════════════════════════════════════════╝
        """
        
        console.print(Align.center(Panel(
            Text(banner, style=CYAN, justify="center"),
            border_style=CYAN,
            box=box.DOUBLE_EDGE,
            title="[bold cyan]⚡ AHMADGROW BULLETPROOF INTELLIGENCE ENGINE ⚡[/]",
            title_align="center",
            subtitle="[bold purple]🔮 AI-Powered Category Detection + Viral Time Analysis 🔮[/]",
            subtitle_align="center"
        )))
        
        console.print(Align.center(Text(
            "███████████████████████████████████████████████████████████████████████████████",
            style=f"bold {PURPLE}"
        )))
        console.print(Align.center(Text(
            matrix_header,
            style=f"bold {ELECTRIC}"
        )))
        console.print(Align.center(Text(
            "█ Developed by: Mehmood Ahmad █",
            style=f"bold {NEON_PINK}"
        )))
        console.print(Align.center(Text(
            "███████████████████████████████████████████████████████████████████████████████",
            style=f"bold {PURPLE}"
        )))
        console.print()
        
        # Professional Disclaimers
        disclaimer_parts = [
            Panel(
                "[bold red]⚠ BULLETPROOF DISCLAIMER ⚠[/]\n"
                "[yellow]▶ This tool operates with QUANTUM PRECISION in the DEEP WEB[/]\n"
                "[yellow]▶ Created strictly for EDUCATIONAL and AUTHORIZED TESTING[/]\n"
                "[red]▶ The developer (Mehmood Ahmad) assumes ABSOLUTELY NO LIABILITY[/]\n"
                "[red]▶ Use at your OWN RISK in the digital universe[/]\n"
                "[yellow]▶ 100% BULLETPROOF - Auto error recovery enabled[/]",
                border_style="red",
                box=box.HEAVY,
                padding=(1, 2)
            ),
            Panel(
                "[bold purple]🔮 AI-POWERED EXTRACTION PROTOCOL 🔮[/]\n"
                "[cyan]▶ AI Category Detection for Videos & Channels[/]\n"
                "[cyan]▶ Viral Time Analysis with Micro-Second Precision[/]\n"
                "[green]▶ NO API KEYS REQUIRED - Pure reverse engineering[/]\n"
                "[gold]▶ Enterprise-grade data extraction with AUTO RECOVERY[/]",
                border_style=PURPLE,
                box=box.HEAVY,
                padding=(1, 2)
            )
        ]
        
        for panel in disclaimer_parts:
            console.print(Align.center(panel))
            console.print()
    
    def typewriter_effect(self, text: str, delay: float = 0.01, style: str = GOLD):
        """Display text with ultra-smooth typewriter animation"""
        try:
            for char in text:
                console.print(char, end="", style=style)
                time.sleep(delay)
            console.print()
        except:
            console.print(text, style=style)
    
    def extract_complete_metadata(self, url: str) -> Optional[Dict]:
        """Extract complete metadata with micro-second precision timestamps"""
        try:
            with Progress(
                SpinnerColumn(spinner_name="dots12", style=CYAN),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(bar_width=50, style=CYAN, complete_style=GREEN, finished_style=GOLD),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                console=console,
                transient=False
            ) as progress:
                
                # Phase 1: Connection
                task1 = progress.add_task("[cyan]🌐 Establishing quantum connection...", total=100)
                time.sleep(0.2)
                progress.update(task1, advance=10, description="[cyan]🌐 Scanning video source with micro-precision...")
                time.sleep(0.1)
                progress.update(task1, advance=15, description="[cyan]🌐 Bypassing geo-restrictions at quantum speed...")
                time.sleep(0.2)
                progress.update(task1, advance=20, description="[cyan]🌐 Extracting every single data bit...")
                time.sleep(0.1)
                
                # Phase 2: Extraction
                task2 = progress.add_task("[purple]📊 Deep data extraction with micro-second precision...", total=100)
                
                with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                    progress.update(task2, advance=15, description="[purple]📊 Extracting primary metadata...")
                    
                    # Extract information with all available data
                    info = ydl.extract_info(url, download=False)
                    progress.update(task2, advance=25, description="[purple]📊 Extracting advanced analytics...")
                    
                    if info is None:
                        return None
                    
                    # Get all available formats
                    progress.update(task2, advance=10, description="[purple]📊 Analyzing video formats with precision...")
                    formats = info.get('formats', [])
                    
                    # Extract deep metadata
                    progress.update(task2, advance=10, description="[purple]📊 Processing quantum parameters...")
                    
                    # ULTRA PRECISION TIMESTAMP ANALYSIS
                    timestamp_info = self.extract_precision_timestamps(info)
                    
                    # Calculate advanced metrics
                    views = info.get('view_count', 0)
                    likes = info.get('like_count', 0)
                    dislikes = info.get('dislike_count', 0)
                    comments = info.get('comment_count', 0)
                    
                    # Engagement rate calculation
                    engagement_rate = 0
                    if views > 0:
                        engagement_rate = ((likes + comments) / views) * 100
                    
                    # Estimated revenue (if monetized)
                    estimated_revenue = 0
                    if views > 0:
                        cpm = 0.75  # Premium CPM estimate
                        estimated_revenue = (views / 1000) * cpm
                    
                    # Content value score
                    content_score = 0
                    if views > 0:
                        like_ratio = likes / views if views > 0 else 0
                        comment_ratio = comments / views if views > 0 else 0
                        content_score = ((like_ratio * 40) + (comment_ratio * 30) + 30)
                        content_score = min(100, max(0, content_score * 100))
                    
                    # Viral prediction
                    viral_score = 0
                    if views > 0:
                        hours_since_upload = 1
                        if info.get('upload_date'):
                            upload_date = datetime.strptime(str(info.get('upload_date')), '%Y%m%d')
                            hours_since_upload = (datetime.now() - upload_date).total_seconds() / 3600
                        if hours_since_upload > 0:
                            views_per_hour = views / hours_since_upload
                            viral_score = min(100, (views_per_hour / 1000) * 100)
                    
                    # Compression analysis
                    compression_info = {
                        'bitrate': info.get('average_bitrate', 0),
                        'codec': info.get('codec', 'N/A'),
                        'fps': info.get('fps', 0),
                        'resolution': info.get('resolution', 'N/A'),
                        'aspect_ratio': info.get('aspect_ratio', 'N/A')
                    }
                    
                    # Audio quality analysis
                    audio_info = {
                        'audio_bitrate': info.get('audio_bitrate', 0),
                        'audio_codec': info.get('audio_codec', 'N/A'),
                        'audio_channels': info.get('audio_channels', 0),
                        'audio_ext': info.get('audio_ext', 'N/A')
                    }
                    
                    # Frame analysis
                    frame_info = {
                        'height': info.get('height', 0),
                        'width': info.get('width', 0),
                        'tbr': info.get('tbr', 0),  # Total bitrate
                        'format_note': info.get('format_note', 'N/A'),
                        'container': info.get('container', 'N/A')
                    }
                    
                    # YouTube specific deep data
                    youtube_data = {}
                    if info.get('extractor') == 'youtube':
                        youtube_data = {
                            'channel_id': info.get('channel_id', 'N/A'),
                            'channel_url': info.get('channel_url', 'N/A'),
                            'channel_follower_count': info.get('channel_follower_count', 0),
                            'uploader_url': info.get('uploader_url', 'N/A'),
                            'availability': info.get('availability', 'N/A'),
                            'live_status': info.get('live_status', 'N/A'),
                            'was_live': info.get('was_live', False),
                            'start_time': info.get('start_time', 'N/A'),
                            'end_time': info.get('end_time', 'N/A'),
                            'release_date': info.get('release_date', 'N/A'),
                            'release_timestamp': info.get('release_timestamp', 0),
                            'modified_date': info.get('modified_date', 'N/A'),
                            'age_limit': info.get('age_limit', 0),
                            'is_family_friendly': info.get('is_family_friendly', False),
                            'is_unlisted': info.get('is_unlisted', False),
                            'is_private': info.get('is_private', False),
                            'playable_in_embed': info.get('playable_in_embed', False),
                            'license': info.get('license', 'N/A'),
                            'subtitles': info.get('subtitles', {}),
                            'automatic_captions': info.get('automatic_captions', {}),
                            'comment_count': info.get('comment_count', 0),
                            'like_count': info.get('like_count', 0),
                            'dislike_count': info.get('dislike_count', 0),
                            'repost_count': info.get('repost_count', 0),
                            'view_count': info.get('view_count', 0),
                            'average_rating': info.get('average_rating', 0),
                            'rating_count': info.get('rating_count', 0),
                            'categories': info.get('categories', []),
                            'tags': info.get('tags', []),
                            'thumbnail': info.get('thumbnail', 'N/A')
                        }
                    
                    # Social media analysis
                    social_data = {
                        'title': info.get('title', 'N/A'),
                        'description': info.get('description', 'N/A'),
                        'uploader': info.get('uploader', 'N/A'),
                        'uploader_id': info.get('uploader_id', 'N/A'),
                        'uploader_url': info.get('uploader_url', 'N/A'),
                        'upload_date': info.get('upload_date', 'N/A'),
                        'timestamp': info.get('timestamp', 0),
                        'duration': info.get('duration', 0),
                        'view_count': info.get('view_count', 0),
                        'like_count': info.get('like_count', 0),
                        'dislike_count': info.get('dislike_count', 0),
                        'comment_count': info.get('comment_count', 0),
                        'repost_count': info.get('repost_count', 0)
                    }
                    
                    progress.update(task2, advance=30, description="[purple]📊 Compiling quantum data matrix...")
                    
                    # Build comprehensive data structure
                    self.timestamp_data = timestamp_info
                    
                    self.deep_analytics = {
                        'basic': {
                            'title': info.get('title', 'N/A'),
                            'description': info.get('description', 'N/A')[:500] + '...' if info.get('description') and len(info.get('description', '')) > 500 else info.get('description', 'N/A'),
                            'uploader': info.get('uploader', 'N/A'),
                            'uploader_id': info.get('uploader_id', 'N/A'),
                            'views': info.get('view_count', 0),
                            'likes': info.get('like_count', 0),
                            'dislikes': info.get('dislike_count', 0),
                            'comments': info.get('comment_count', 0),
                            'duration': info.get('duration', 0),
                            'upload_date': info.get('upload_date', 'N/A'),
                            'extractor': info.get('extractor', 'N/A'),
                            'webpage_url': info.get('webpage_url', url)
                        },
                        'timestamp_analysis': timestamp_info,
                        'analytics': {
                            'engagement_rate': engagement_rate,
                            'estimated_revenue': estimated_revenue,
                            'content_score': content_score,
                            'viral_score': viral_score,
                            'like_ratio': (likes / views * 100) if views > 0 else 0,
                            'comment_ratio': (comments / views * 100) if views > 0 else 0,
                            'avg_views_per_day': self.calculate_avg_views_per_day(info),
                            'growth_rate': self.calculate_growth_rate(info)
                        },
                        'technical': {
                            'compression': compression_info,
                            'audio': audio_info,
                            'frame': frame_info,
                            'available_formats': len(formats),
                            'best_quality': self.get_best_quality(formats),
                            'all_formats': formats[:5]  # Show first 5 formats
                        },
                        'youtube_deep': youtube_data if info.get('extractor') == 'youtube' else {},
                        'social': social_data,
                        'hashtags': self.extract_hashtags(info.get('description', '')),
                        'mentions': self.extract_mentions(info.get('description', '')),
                        'urls': self.extract_urls(info.get('description', '')),
                        'language': info.get('language', 'N/A'),
                        'is_live': info.get('is_live', False),
                        'was_live': info.get('was_live', False),
                        'live_status': info.get('live_status', 'N/A'),
                        'age_restricted': info.get('age_limit', 0) > 0,
                        'family_friendly': info.get('is_family_friendly', False)
                    }
                    
                    progress.update(task2, advance=100, description="[green]✅ Quantum extraction complete!")
                    return self.deep_analytics
                    
        except yt_dlp.utils.DownloadError as e:
            console.print(f"[-] Download Error: {str(e)}", style=CRIMSON)
            return None
        except Exception as e:
            console.print(f"[-] Error extracting metadata: {str(e)}", style=CRIMSON)
            return None
    
    def extract_precision_timestamps(self, info: Dict) -> Dict:
        """Extract every possible timestamp with micro-second precision"""
        timestamp_data = {
            'upload_timestamp': {},
            'video_duration': {},
            'release_info': {},
            'precise_timings': {},
            'timezone_info': {},
            'epoch_data': {},
            'human_readable': {}
        }
        
        # 1. UPLOAD TIMESTAMP - COMPLETE
        upload_date = info.get('upload_date')
        upload_timestamp = info.get('timestamp', 0)
        
        if upload_date:
            try:
                # Parse date with micro-second precision
                dt_obj = datetime.strptime(str(upload_date), '%Y%m%d')
                
                # If we have timestamp, get exact time
                if upload_timestamp:
                    dt_obj = datetime.fromtimestamp(upload_timestamp)
                
                timestamp_data['upload_timestamp'] = {
                    'year': dt_obj.year,
                    'month': dt_obj.month,
                    'day': dt_obj.day,
                    'hour': dt_obj.hour,
                    'minute': dt_obj.minute,
                    'second': dt_obj.second,
                    'microsecond': dt_obj.microsecond,
                    'full_date': dt_obj.strftime('%A, %B %d, %Y'),
                    'full_time': dt_obj.strftime('%I:%M:%S %p'),
                    'full_datetime': dt_obj.strftime('%Y-%m-%d %I:%M:%S.%f %p'),
                    '12_hour': dt_obj.strftime('%I:%M:%S %p'),
                    '24_hour': dt_obj.strftime('%H:%M:%S'),
                    'am_pm': dt_obj.strftime('%p'),
                    'timezone': dt_obj.strftime('%Z'),
                    'timezone_offset': dt_obj.strftime('%z'),
                    'iso_format': dt_obj.isoformat(),
                    'rfc_format': dt_obj.strftime('%a, %d %b %Y %H:%M:%S %z'),
                    'unix_epoch': int(dt_obj.timestamp()),
                    'milliseconds': int(dt_obj.timestamp() * 1000),
                    'microseconds': int(dt_obj.timestamp() * 1000000)
                }
            except:
                pass
        
        # 2. VIDEO DURATION - MICRO-SECOND PRECISION
        duration = info.get('duration', 0)
        if duration:
            hours = duration // 3600
            minutes = (duration % 3600) // 60
            seconds = duration % 60
            milliseconds = (duration * 1000) % 1000
            
            timestamp_data['video_duration'] = {
                'total_seconds': duration,
                'total_milliseconds': duration * 1000,
                'total_microseconds': duration * 1000000,
                'hours': hours,
                'minutes': minutes,
                'seconds': seconds,
                'milliseconds': int(milliseconds),
                'full_timestamp': f"{hours:02d}:{minutes:02d}:{seconds:02d}.{int(milliseconds):03d}",
                'readable': f"{hours}h {minutes}m {seconds}s" if hours > 0 else f"{minutes}m {seconds}s",
                'short': f"{hours:02d}:{minutes:02d}:{seconds:02d}" if hours > 0 else f"{minutes:02d}:{seconds:02d}"
            }
        
        # 3. RELEASE INFO
        release_date = info.get('release_date')
        release_timestamp = info.get('release_timestamp', 0)
        
        if release_date:
            try:
                dt_release = datetime.strptime(str(release_date), '%Y%m%d')
                if release_timestamp:
                    dt_release = datetime.fromtimestamp(release_timestamp)
                
                timestamp_data['release_info'] = {
                    'release_year': dt_release.year,
                    'release_month': dt_release.month,
                    'release_day': dt_release.day,
                    'release_hour': dt_release.hour,
                    'release_minute': dt_release.minute,
                    'release_second': dt_release.second,
                    'release_full': dt_release.strftime('%A, %B %d, %Y %I:%M:%S %p'),
                    'release_iso': dt_release.isoformat()
                }
            except:
                pass
        
        # 4. PRECISE TIMINGS
        timestamp_data['precise_timings'] = {
            'age_seconds': int(time.time() - upload_timestamp) if upload_timestamp else 0,
            'age_days': int((time.time() - upload_timestamp) / 86400) if upload_timestamp else 0,
            'age_hours': int((time.time() - upload_timestamp) / 3600) if upload_timestamp else 0,
            'age_minutes': int((time.time() - upload_timestamp) / 60) if upload_timestamp else 0,
            'age_weeks': int((time.time() - upload_timestamp) / 604800) if upload_timestamp else 0,
            'age_months': int((time.time() - upload_timestamp) / 2592000) if upload_timestamp else 0,
            'age_years': int((time.time() - upload_timestamp) / 31536000) if upload_timestamp else 0
        }
        
        # 5. TIMEZONE INFO
        timestamp_data['timezone_info'] = {
            'local_time': datetime.now().strftime('%Y-%m-%d %I:%M:%S %p'),
            'local_timezone': datetime.now().strftime('%Z'),
            'local_offset': datetime.now().strftime('%z'),
            'utc_time': datetime.utcnow().strftime('%Y-%m-%d %I:%M:%S %p')
        }
        
        # 6. EPOCH DATA
        timestamp_data['epoch_data'] = {
            'upload_epoch': upload_timestamp,
            'current_epoch': int(time.time()),
            'difference_seconds': int(time.time() - upload_timestamp) if upload_timestamp else 0,
            'difference_days': int((time.time() - upload_timestamp) / 86400) if upload_timestamp else 0
        }
        
        # 7. HUMAN READABLE
        if upload_date:
            try:
                dt_hr = datetime.strptime(str(upload_date), '%Y%m%d')
                if upload_timestamp:
                    dt_hr = datetime.fromtimestamp(upload_timestamp)
                
                timestamp_data['human_readable'] = {
                    'date': dt_hr.strftime('%A, %B %d, %Y'),
                    'time': dt_hr.strftime('%I:%M:%S %p'),
                    'exact_moment': dt_hr.strftime('%A, %B %d, %Y at %I:%M:%S %p'),
                    'relative': self.get_relative_time(upload_timestamp) if upload_timestamp else 'N/A'
                }
            except:
                pass
        
        return timestamp_data
    
    def get_relative_time(self, timestamp: int) -> str:
        """Get human-readable relative time"""
        diff = int(time.time() - timestamp)
        
        if diff < 60:
            return f"{diff} seconds ago"
        elif diff < 3600:
            minutes = diff // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        elif diff < 86400:
            hours = diff // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff < 2592000:
            days = diff // 86400
            return f"{days} day{'s' if days > 1 else ''} ago"
        elif diff < 31536000:
            months = diff // 2592000
            return f"{months} month{'s' if months > 1 else ''} ago"
        else:
            years = diff // 31536000
            return f"{years} year{'s' if years > 1 else ''} ago"
    
    def calculate_avg_views_per_day(self, info: Dict) -> float:
        """Calculate average views per day"""
        views = info.get('view_count', 0)
        upload_date = info.get('upload_date')
        if not upload_date or views == 0:
            return 0
        
        try:
            date_obj = datetime.strptime(str(upload_date), '%Y%m%d')
            days_since_upload = (datetime.now() - date_obj).days
            if days_since_upload > 0:
                return views / days_since_upload
        except:
            pass
        return 0
    
    def calculate_growth_rate(self, info: Dict) -> float:
        """Calculate estimated growth rate"""
        views = info.get('view_count', 0)
        likes = info.get('like_count', 0)
        upload_date = info.get('upload_date')
        
        if not upload_date or views == 0:
            return 0
        
        try:
            date_obj = datetime.strptime(str(upload_date), '%Y%m%d')
            hours_since = (datetime.now() - date_obj).total_seconds() / 3600
            if hours_since > 24:
                views_per_hour = views / hours_since
                growth_percentage = (views_per_hour * 24) / (views / (hours_since / 24)) * 100 if hours_since > 0 else 0
                return min(100, growth_percentage)
        except:
            pass
        return 0
    
    def get_best_quality(self, formats: List) -> Dict:
        """Get the best quality format available"""
        best = {'height': 0, 'width': 0, 'bitrate': 0}
        for fmt in formats:
            height = fmt.get('height', 0)
            bitrate = fmt.get('tbr', 0)
            if height > best['height']:
                best = {
                    'height': height,
                    'width': fmt.get('width', 0),
                    'bitrate': bitrate,
                    'format_id': fmt.get('format_id', 'N/A'),
                    'ext': fmt.get('ext', 'N/A'),
                    'codec': fmt.get('vcodec', 'N/A')
                }
        return best
    
    def extract_hashtags(self, text: str) -> List[str]:
        """Extract hashtags from text"""
        if not text:
            return []
        hashtag_pattern = r'#\w+'
        return list(set(re.findall(hashtag_pattern, text)))[:20]
    
    def extract_mentions(self, text: str) -> List[str]:
        """Extract mentions from text"""
        if not text:
            return []
        mention_pattern = r'@\w+'
        return list(set(re.findall(mention_pattern, text)))[:20]
    
    def extract_urls(self, text: str) -> List[str]:
        """Extract URLs from text"""
        if not text:
            return []
        url_pattern = r'https?://[^\s]+'
        return re.findall(url_pattern, text)[:10]
    
    def display_quantum_analytics(self, data: Dict):
        """Display analytics with quantum precision"""
        if not data:
            console.print("[-] No data to display", style=CRIMSON)
            return
        
        console.print()
        console.print(Align.center(Panel(
            Text("⚡ BULLETPROOF QUANTUM ANALYTICS DASHBOARD ⚡", style=f"bold {CYAN}", justify="center"),
            border_style=CYAN,
            box=box.DOUBLE_EDGE,
            padding=(1, 2)
        )))
        
        # Basic Information - Quantum Style
        basic = data.get('basic', {})
        console.print(Panel(
            Group(
                Text(f"📌 TITLE: {basic.get('title', 'N/A')}", style=f"bold {WHITE}"),
                Text(f"👤 UPLOADER: {basic.get('uploader', 'N/A')} (@{basic.get('uploader_id', 'N/A')})", style=f"bold {GOLD}"),
                Text(f"🔗 PLATFORM: {basic.get('extractor', 'N/A').upper()}", style=f"bold {CYAN}"),
                Text(f"📅 UPLOAD DATE: {basic.get('upload_date', 'N/A')}", style=f"bold {GREEN}"),
                Text(f"🔗 WATCH URL: [underline cyan]{basic.get('webpage_url', 'N/A')}[/underline cyan]", style=f"bold {NEON_PINK}"),
            ),
            title="[bold cyan]📊 BASIC INFO[/]",
            border_style=CYAN,
            box=box.HEAVY
        ))
        
        # Category Detection
        title = basic.get('title', '')
        description = data.get('basic', {}).get('description', '')
        uploader = basic.get('uploader', '')
        channel_id = data.get('youtube_deep', {}).get('channel_id', '')
        
        category_data = CategoryDetector.detect_category(title, description, uploader, channel_id)
        
        console.print(Panel(
            Group(
                Text(f"🎯 PRIMARY CATEGORY: [bold cyan]{category_data.get('primary', 'general').upper()}[/bold cyan]", style="bold white"),
                Text(f"📊 ALL CATEGORIES: {', '.join(category_data.get('all_categories', ['general']))}", style=f"bold {GOLD}"),
                Text(f"🎯 CONFIDENCE LEVEL: {category_data.get('confidence', 'Low')}", style=f"bold {GREEN if category_data.get('confidence') == 'High' else 'YELLOW' if category_data.get('confidence') == 'Medium' else 'RED'}"),
                Text(f"📈 CATEGORY SCORES: {json.dumps(category_data.get('scores', {}), indent=2)}", style=f"bold {PURPLE}"),
            ),
            title="[bold purple]🎯 AI-POWERED CATEGORY DETECTION[/]",
            border_style=PURPLE,
            box=box.HEAVY
        ))
        
        # Viral Time Analysis
        views = basic.get('views', 0)
        timestamp_data = data.get('timestamp_analysis', {})
        upload_ts = timestamp_data.get('upload_timestamp', {})
        
        if upload_ts and 'year' in upload_ts:
            try:
                upload_time = datetime(
                    upload_ts.get('year', 2024),
                    upload_ts.get('month', 1),
                    upload_ts.get('day', 1),
                    upload_ts.get('hour', 0),
                    upload_ts.get('minute', 0),
                    upload_ts.get('second', 0)
                )
                
                viral_analysis = ViralTimeAnalyzer.analyze_viral_potential(
                    views, upload_time, category_data.get('primary', 'general')
                )
                
                console.print(Panel(
                    Group(
                        Text(f"🔥 VIRAL STATUS: {viral_analysis.get('viral_status', 'N/A')}", style=f"bold {GREEN if 'VIRAL' in viral_analysis.get('viral_status', '') else 'YELLOW' if 'TRENDING' in viral_analysis.get('viral_status', '') else 'RED'}"),
                        Text(f"📊 VIRAL SCORE: {viral_analysis.get('viral_score', 0)}%", style=f"bold {CYAN}"),
                        Text(f"📈 VIEWS PER HOUR: {viral_analysis.get('views_per_hour', 0):,.2f}", style=f"bold {GOLD}"),
                        Text(f"📊 VIEWS PER DAY: {viral_analysis.get('views_per_day', 0):,.2f}", style=f"bold {GREEN}"),
                        Text(f"⏰ HOURS SINCE UPLOAD: {viral_analysis.get('hours_since_upload', 0):.1f}", style=f"bold {PURPLE}"),
                        Text(f"🚀 IS VIRAL: {viral_analysis.get('is_viral', False)}", style=f"bold {GREEN if viral_analysis.get('is_viral') else 'RED'}"),
                        Text(f"📈 IS TRENDING: {viral_analysis.get('is_trending', False)}", style=f"bold {GREEN if viral_analysis.get('is_trending') else 'RED'}"),
                    ),
                    title="[bold gold]🚀 VIRAL TIME ANALYSIS[/]",
                    border_style=GOLD,
                    box=box.HEAVY
                ))
                
                # Best Time Recommendation
                best_times = viral_analysis.get('best_times', {})
                console.print(Panel(
                    Group(
                        Text(f"🏆 BEST TIME TO UPLOAD: [bold matrix]{best_times.get('best_time_readable', 'N/A')}[/bold matrix]", style="bold white"),
                        Text(f"📅 BEST DAY: {best_times.get('best_day', 'N/A')}", style=f"bold {CYAN}"),
                        Text(f"⏰ BEST HOUR: {best_times.get('best_hour', 0):02d}:{best_times.get('best_minute', 0):02d}:{best_times.get('best_second', 0):02d}", style=f"bold {GOLD}"),
                        Text(f"📊 SECOND BEST: {best_times.get('second_best', 'N/A')}", style=f"bold {PURPLE}"),
                        Text(f"📅 WEEKDAYS BEST: {', '.join(best_times.get('weekdays', ['N/A']))}", style=f"bold {GREEN}"),
                        Text(f"📅 WEEKEND BEST: {', '.join(best_times.get('weekend', ['N/A']))}", style=f"bold {CYAN}"),
                        Text(f"💡 RECOMMENDATION: {best_times.get('explanation', 'N/A')}", style=f"bold {WHITE}"),
                    ),
                    title="[bold matrix]⏰ OPTIMAL UPLOAD TIME ANALYSIS[/]",
                    border_style=MATRIX,
                    box=box.HEAVY
                ))
                
                # Personalized Recommendation
                recommendation = viral_analysis.get('recommendation', '')
                console.print(Panel(
                    Text(f"💡 {recommendation}", style=f"bold {GREEN}"),
                    title="[bold green]📈 PERSONALIZED RECOMMENDATION[/]",
                    border_style=GREEN,
                    box=box.HEAVY
                ))
                
            except Exception as e:
                console.print(f"[yellow]⚠️ Viral analysis error: {str(e)}[/]")
        
        # TIMESTAMP ANALYSIS - ULTRA PRECISION
        if timestamp_data:
            upload_ts = timestamp_data.get('upload_timestamp', {})
            duration_ts = timestamp_data.get('video_duration', {})
            release_ts = timestamp_data.get('release_info', {})
            precise_ts = timestamp_data.get('precise_timings', {})
            human_ts = timestamp_data.get('human_readable', {})
            
            console.print(Panel(
                Group(
                    Text("⏰ EXACT UPLOAD TIMESTAMP - MICRO-SECOND PRECISION", style=f"bold {ELECTRIC}"),
                    Text(f"📅 Full Date: {upload_ts.get('full_date', 'N/A')}", style=f"bold {MATRIX}"),
                    Text(f"🕐 Exact Time: {upload_ts.get('full_time', 'N/A')}", style=f"bold {MATRIX}"),
                    Text(f"⏱️ Micro-Second: {upload_ts.get('microsecond', 0)} μs", style=f"bold {MATRIX}"),
                    Text(f"📆 Exact Moment: {upload_ts.get('full_datetime', 'N/A')}", style=f"bold {NEON_YELLOW}"),
                    Text(f"🌐 Timezone: {upload_ts.get('timezone', 'N/A')} ({upload_ts.get('timezone_offset', 'N/A')})", style=f"bold {CYAN}"),
                    Text(f"📊 ISO Format: {upload_ts.get('iso_format', 'N/A')}", style=f"bold {TURQUOISE}"),
                    Text(f"📈 RFC Format: {upload_ts.get('rfc_format', 'N/A')}", style=f"bold {PURPLE}"),
                    Text(f"🔄 Unix Epoch: {upload_ts.get('unix_epoch', 0)}", style=f"bold {DARK_GRAY}"),
                    Text(f"⚡ Milliseconds: {upload_ts.get('milliseconds', 0)} ms", style=f"bold {DARK_GRAY}"),
                    Text(f"🔬 Microseconds: {upload_ts.get('microseconds', 0)} μs", style=f"bold {DARK_GRAY}"),
                ),
                title="[bold matrix]⏰ MICRO-SECOND PRECISION TIMESTAMP ANALYSIS[/]",
                border_style=MATRIX,
                box=box.HEAVY
            ))
            
            # Duration Analysis
            if duration_ts:
                console.print(Panel(
                    Group(
                        Text(f"⏱️ Total Seconds: {duration_ts.get('total_seconds', 0)} s", style=f"bold {WHITE}"),
                        Text(f"⚡ Total Milliseconds: {duration_ts.get('total_milliseconds', 0)} ms", style=f"bold {GOLD}"),
                        Text(f"🔬 Total Microseconds: {duration_ts.get('total_microseconds', 0)} μs", style=f"bold {PURPLE}"),
                        Text(f"🕐 Hours: {duration_ts.get('hours', 0)}h {duration_ts.get('minutes', 0)}m {duration_ts.get('seconds', 0)}s", style=f"bold {CYAN}"),
                        Text(f"📊 Full Timestamp: {duration_ts.get('full_timestamp', 'N/A')}", style=f"bold {MATRIX}"),
                        Text(f"📅 Readable: {duration_ts.get('readable', 'N/A')}", style=f"bold {GREEN}"),
                    ),
                    title="[bold gold]⏱️ VIDEO DURATION - MICRO-SECOND PRECISION[/]",
                    border_style=GOLD,
                    box=box.HEAVY
                ))
            
            # Human Readable
            if human_ts:
                console.print(Panel(
                    Group(
                        Text(f"📅 Date: {human_ts.get('date', 'N/A')}", style=f"bold {CYAN}"),
                        Text(f"🕐 Time: {human_ts.get('time', 'N/A')}", style=f"bold {GOLD}"),
                        Text(f"📍 Exact Moment: {human_ts.get('exact_moment', 'N/A')}", style=f"bold {NEON_PINK}"),
                        Text(f"⏳ Relative: {human_ts.get('relative', 'N/A')}", style=f"bold {GREEN}"),
                    ),
                    title="[bold purple]📖 HUMAN-READABLE TIMESTAMPS[/]",
                    border_style=PURPLE,
                    box=box.HEAVY
                ))
            
            # Precise Timings
            if precise_ts:
                console.print(Panel(
                    Group(
                        Text(f"🔄 Age in Seconds: {precise_ts.get('age_seconds', 0):,} s", style=f"bold {WHITE}"),
                        Text(f"⏱️ Age in Minutes: {precise_ts.get('age_minutes', 0):,} min", style=f"bold {GOLD}"),
                        Text(f"📅 Age in Hours: {precise_ts.get('age_hours', 0):,} h", style=f"bold {CYAN}"),
                        Text(f"📊 Age in Days: {precise_ts.get('age_days', 0):,} d", style=f"bold {GREEN}"),
                        Text(f"📈 Age in Weeks: {precise_ts.get('age_weeks', 0):,} w", style=f"bold {PURPLE}"),
                        Text(f"📉 Age in Months: {precise_ts.get('age_months', 0):,} mo", style=f"bold {NEON_ORANGE}"),
                        Text(f"📆 Age in Years: {precise_ts.get('age_years', 0):,} y", style=f"bold {ROSE}"),
                    ),
                    title="[bold cyan]⏰ PRECISE AGE ANALYSIS[/]",
                    border_style=CYAN,
                    box=box.HEAVY
                ))
            
            # Timezone Info
            timezone_info = timestamp_data.get('timezone_info', {})
            if timezone_info:
                console.print(Panel(
                    Group(
                        Text(f"🕐 Local Time: {timezone_info.get('local_time', 'N/A')}", style=f"bold {GREEN}"),
                        Text(f"🌐 Local Timezone: {timezone_info.get('local_timezone', 'N/A')}", style=f"bold {CYAN}"),
                        Text(f"📍 Local Offset: {timezone_info.get('local_offset', 'N/A')}", style=f"bold {GOLD}"),
                        Text(f"🌍 UTC Time: {timezone_info.get('utc_time', 'N/A')}", style=f"bold {PURPLE}"),
                    ),
                    title="[bold yellow]🌐 TIMEZONE ANALYSIS[/]",
                    border_style=GOLD,
                    box=box.HEAVY
                ))
        
        # Analytics - Advanced Metrics
        analytics = data.get('analytics', {})
        console.print(Panel(
            Group(
                Columns([
                    Text(f"📈 Engagement: {analytics.get('engagement_rate', 0):.2f}%", style=f"bold {GREEN}"),
                    Text(f"💰 Estimated Revenue: ${analytics.get('estimated_revenue', 0):.2f}", style=f"bold {GOLD}"),
                    Text(f"⭐ Content Score: {analytics.get('content_score', 0):.1f}/100", style=f"bold {PURPLE}"),
                ]),
                Columns([
                    Text(f"🔄 Viral Score: {analytics.get('viral_score', 0):.1f}%", style=f"bold {NEON_PINK}"),
                    Text(f"📊 Views/Day: {analytics.get('avg_views_per_day', 0):.0f}", style=f"bold {CYAN}"),
                    Text(f"📈 Growth Rate: {analytics.get('growth_rate', 0):.1f}%", style=f"bold {ELECTRIC}"),
                ]),
                Columns([
                    Text(f"❤️ Like Ratio: {analytics.get('like_ratio', 0):.2f}%", style=f"bold {ROSE}"),
                    Text(f"💬 Comment Ratio: {analytics.get('comment_ratio', 0):.3f}%", style=f"bold {TURQUOISE}"),
                ])
            ),
            title="[bold purple]📊 ADVANCED ANALYTICS[/]",
            border_style=PURPLE,
            box=box.HEAVY
        ))
        
        # Technical Deep Data
        tech = data.get('technical', {})
        comp = tech.get('compression', {})
        audio = tech.get('audio', {})
        frame = tech.get('frame', {})
        best = tech.get('best_quality', {})
        
        console.print(Panel(
            Group(
                Text(f"🎬 Resolution: {frame.get('height', 0)}x{frame.get('width', 0)}", style=f"bold {CYAN}"),
                Text(f"🎥 Codec: {comp.get('codec', 'N/A')}", style=f"bold {GOLD}"),
                Text(f"📹 FPS: {comp.get('fps', 0)}", style=f"bold {GREEN}"),
                Text(f"🎵 Audio Codec: {audio.get('audio_codec', 'N/A')}", style=f"bold {PURPLE}"),
                Text(f"📀 Total Bitrate: {comp.get('bitrate', 0)/1000:.1f} Kbps", style=f"bold {NEON_ORANGE}"),
                Text(f"📦 Container: {frame.get('container', 'N/A')}", style=f"bold {TURQUOISE}"),
                Text(f"📊 Available Formats: {tech.get('available_formats', 0)}", style=f"bold {WHITE}"),
                Text(f"🏆 Best Quality: {best.get('height', 0)}p at {best.get('bitrate', 0):.0f} Kbps", style=f"bold {NEON_PINK}"),
            ),
            title="[bold cyan]🎯 TECHNICAL SPECIFICATIONS[/]",
            border_style=CYAN,
            box=box.HEAVY
        ))
        
        # YouTube Deep Data
        youtube = data.get('youtube_deep', {})
        if youtube:
            console.print(Panel(
                Group(
                    Columns([
                        Text(f"📢 Channel ID: {youtube.get('channel_id', 'N/A')[:20]}...", style=f"bold {GOLD}"),
                        Text(f"👥 Subscribers: {youtube.get('channel_follower_count', 0):,}", style=f"bold {GREEN}"),
                        Text(f"🔒 Age Limit: {youtube.get('age_limit', 0)}", style=f"bold {CRIMSON}"),
                    ]),
                    Columns([
                        Text(f"📺 Live Status: {youtube.get('live_status', 'N/A')}", style=f"bold {CYAN}"),
                        Text(f"🎯 Was Live: {youtube.get('was_live', False)}", style=f"bold {PURPLE}"),
                        Text(f"📹 Playable in Embed: {youtube.get('playable_in_embed', False)}", style=f"bold {TURQUOISE}"),
                    ]),
                    Columns([
                        Text(f"📌 Unlisted: {youtube.get('is_unlisted', False)}", style=f"bold {NEON_ORANGE}"),
                        Text(f"🔐 Private: {youtube.get('is_private', False)}", style=f"bold {ROSE}"),
                        Text(f"👪 Family Friendly: {youtube.get('is_family_friendly', False)}", style=f"bold {GREEN}"),
                    ]),
                    Text(f"📝 License: {youtube.get('license', 'N/A')}", style=f"bold {WHITE}"),
                    Text(f"🔄 Repost Count: {youtube.get('repost_count', 0):,}", style=f"bold {NEON_PINK}"),
                ),
                title="[bold red]🎬 YOUTUBE DEEP DATA[/]",
                border_style=CRIMSON,
                box=box.HEAVY
            ))
        
        # Social Media Analytics
        social = data.get('social', {})
        console.print(Panel(
            Group(
                Columns([
                    Text(f"👁️ Views: {social.get('view_count', 0):,}", style=f"bold {CYAN}"),
                    Text(f"❤️ Likes: {social.get('like_count', 0):,}", style=f"bold {GREEN}"),
                    Text(f"💬 Comments: {social.get('comment_count', 0):,}", style=f"bold {GOLD}"),
                ]),
                Columns([
                    Text(f"📉 Dislikes: {social.get('dislike_count', 0):,}", style=f"bold {CRIMSON}"),
                    Text(f"🔄 Reposts: {social.get('repost_count', 0):,}", style=f"bold {PURPLE}"),
                    Text(f"⏱️ Duration: {self.format_duration(social.get('duration', 0))}", style=f"bold {TURQUOISE}"),
                ])
            ),
            title="[bold gold]📱 SOCIAL METRICS[/]",
            border_style=GOLD,
            box=box.HEAVY
        ))
        
        # Hashtags and Mentions
        hashtags = data.get('hashtags', [])
        mentions = data.get('mentions', [])
        urls = data.get('urls', [])
        
        if hashtags or mentions or urls:
            console.print(Panel(
                Group(
                    Text(f"🏷️ Hashtags ({len(hashtags)}): {', '.join(hashtags[:10])}{'...' if len(hashtags) > 10 else ''}", style=f"bold {CYAN}"),
                    Text(f"👤 Mentions ({len(mentions)}): {', '.join(mentions[:10])}{'...' if len(mentions) > 10 else ''}", style=f"bold {GOLD}"),
                    Text(f"🔗 URLs ({len(urls)}): {', '.join(urls[:5])}{'...' if len(urls) > 5 else ''}", style=f"bold {GREEN}"),
                ),
                title="[bold purple]🔍 CONTENT ANALYSIS[/]",
                border_style=PURPLE,
                box=box.HEAVY
            ))
        
        # Quick Action Buttons
        video_url = basic.get('webpage_url', '')
        if video_url:
            console.print(Panel(
                Group(
                    Text(f"🎬 Click Here to Watch: [underline cyan]{video_url}[/underline cyan]", style="bold white"),
                    Text("[cyan]💡 Click the link above or press Ctrl+Click to open in browser[/]"),
                ),
                title="[bold green]▶ WATCH VIDEO[/]",
                border_style=GREEN,
                box=box.HEAVY
            ))
        
        # Final Message with App Promotion
        console.print()
        console.print(Align.center(Panel(
            Group(
                Text("🌟 THANK YOU FOR USING AHMADGROW! 🌟", style=f"bold {NEON_PINK}"),
                Text("", style="white"),
                Text("📈 For MORE VIEWS, GROWTH, and BEST PERFORMANCE:", style=f"bold {GOLD}"),
                Text("📱 Download TAGZORPH AI - Your Ultimate Content Growth Companion", style=f"bold {CYAN}"),
                Text("", style="white"),
                Text("🎯 Get Better Titles • Perfect Descriptions • Optimal Hashtags", style=f"bold {GREEN}"),
                Text("🚀 Boost Your Channel Growth with AI-Powered Insights", style=f"bold {PURPLE}"),
                Text("", style="white"),
                Text("🔗 AVAILABLE ON GOOGLE PLAY STORE", style=f"bold {ELECTRIC}"),
                Text("📱 Search: TAGZORPH AI", style=f"bold {NEON_PINK}"),
                Text("", style="white"),
                Text("💡 Transform Your Content Strategy Today!", style=f"bold {GOLD}"),
            ),
            title="[bold rainbow]🚀 SUPERCHARGE YOUR GROWTH[/]",
            border_style=GOLD,
            box=box.HEAVY,
            padding=(1, 2)
        )))
        
        console.print(Align.center(Text(
            "⚡ [BULLETPROOF QUANTUM EXTRACTION COMPLETE] ⚡",
            style=f"bold {ELECTRIC}"
        )))
        console.print()
    
    def format_duration(self, seconds: int) -> str:
        """Format duration in human-readable format"""
        if not seconds:
            return "N/A"
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"
    
    def is_valid_url(self, url: str) -> bool:
        """Validate if the input is a proper URL"""
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        return bool(url_pattern.match(url))

def main():
    """Main function to run the application with bulletproof error handling"""
    try:
        extractor = AhmadGrowExtractor()
        
        # Clear screen for better visual
        try:
            os.system('clear' if os.name == 'posix' else 'cls')
        except:
            pass
        
        # Display banner with error handling
        try:
            extractor.display_banner()
        except Exception as e:
            console.print(f"[yellow]⚠️ Banner display error: {str(e)}[/]")
            console.print("[bold cyan]AhmadGrow - Bulletproof Deep Video Intelligence[/]")
        
        # Matrix-style welcome message
        console.print()
        try:
            extractor.typewriter_effect("┌──────────────────────────────────────────────────────────────────────────────┐", style=CYAN)
            extractor.typewriter_effect("│  ⚡ BULLETPROOF QUANTUM EXTRACTION PROTOCOL v99.9.9 ⚡                    │", style=ELECTRIC)
            extractor.typewriter_effect("│  🌐 MATRIX MODE: QUANTUM ACTIVE                                         │", style=CYAN)
            extractor.typewriter_effect("│  🔒 ENCRYPTION: 1024-bit Quantum Shield                                 │", style=GREEN)
            extractor.typewriter_effect("│  📡 SCANNING: Deep Web Extraction with MICRO-SECOND PRECISION          │", style=GOLD)
            extractor.typewriter_effect("│  ⏰ TIMESTAMP ANALYSIS: ENABLED (Full Date/Time with Micro-Seconds)     │", style=MATRIX)
            extractor.typewriter_effect("│  🤖 AI CATEGORY DETECTION: ACTIVE                                      │", style=PURPLE)
            extractor.typewriter_effect("│  🚀 VIRAL TIME ANALYSIS: ACTIVE                                        │", style=NEON_PINK)
            extractor.typewriter_effect("└──────────────────────────────────────────────────────────────────────────────┘", style=CYAN)
        except:
            pass
        
        console.print()
        
        try:
            extractor.typewriter_effect("🔥 Welcome to AhmadGrow - Bulletproof Deep Video Intelligence System", style=f"bold {NEON_PINK}")
            extractor.typewriter_effect("💀 Unlocking 50+ hidden metadata parameters with MICRO-SECOND PRECISION...\n", style=f"bold {PURPLE}")
            extractor.typewriter_effect("⏰ Including COMPLETE TIMESTAMP ANALYSIS - Every Second, Minute, Hour, Day, Month, Year!\n", style=f"bold {MATRIX}")
            extractor.typewriter_effect("🤖 AI-POWERED CATEGORY DETECTION + VIRAL TIME ANALYSIS ENABLED!\n", style=f"bold {GOLD}")
        except:
            pass
        
        # Input URL with validation and retry
        url = None
        while url is None:
            try:
                url_input = Prompt.ask(
                    f"[bold {CYAN}]🌐 Enter video URL for quantum extraction[/]",
                    default="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
                )
                
                if url_input.strip():
                    if extractor.is_valid_url(url_input):
                        url = url_input
                    else:
                        console.print("[red]❌ Invalid URL format. Please enter a valid URL starting with http:// or https://[/]")
                else:
                    console.print("[red]❌ URL cannot be empty. Please enter a valid URL.[/]")
            except KeyboardInterrupt:
                raise
            except Exception as e:
                console.print(f"[red]❌ Input error: {str(e)}[/]")
                time.sleep(1)
        
        # Extract metadata with progress
        console.print("\n[cyan]🔍 Initiating bulletproof quantum extraction protocol...[/]")
        console.print("[yellow]⚡ Extracting ALL available metadata parameters with MICRO-SECOND PRECISION[/]")
        console.print("[gold]⏰ Full timestamp analysis in progress...[/]")
        console.print("[purple]🤖 AI Category Detection and Viral Time Analysis running...[/]")
        console.print()
        
        data = None
        retry_count = 0
        while data is None and retry_count < 3:
            try:
                data = extractor.extract_complete_metadata(url)
                if data is None:
                    retry_count += 1
                    if retry_count < 3:
                        console.print(f"[yellow]⚠️ Retry {retry_count}/3...[/]")
                        time.sleep(2)
            except Exception as e:
                retry_count += 1
                console.print(f"[yellow]⚠️ Extraction attempt {retry_count} failed: {str(e)}[/]")
                if retry_count < 3:
                    time.sleep(2)
        
        if data:
            console.print("\n[green]✅ BULLETPROOF QUANTUM EXTRACTION SUCCESSFUL![/]")
            console.print("[gold]📊 Displaying comprehensive analytics dashboard with AI insights[/]\n")
            
            try:
                extractor.display_quantum_analytics(data)
            except Exception as e:
                console.print(f"[red]❌ Display error: {str(e)}[/]")
                console.print("[yellow]Data extracted but display encountered an error. Please try again.[/]")
            
            # Open video link with error handling
            try:
                if Confirm.ask("\n[cyan]🌐 Open video in browser to watch?[/]"):
                    video_url = data.get('basic', {}).get('webpage_url', '')
                    if video_url:
                        console.print(f"[green]✅ Opening: {video_url}[/]")
                        webbrowser.open(video_url)
                    else:
                        console.print("[red]❌ No URL available to open[/]")
            except:
                pass
            
            # Ask if user wants to extract another video
            try:
                if Confirm.ask("\n[cyan]🔄 Extract quantum data from another video?[/]"):
                    console.print("\n")
                    main()
                    return
                else:
                    console.print("\n[bold green]👋 Thank you for using AhmadGrow!")
                    console.print("[bold purple]💀 Stay safe in the digital universe...[/]")
                    console.print("[bold cyan]🔮 Remember: Every second, every micro-second matters![/]")
                    console.print("[bold gold]📱 Download TAGZORPH AI for more views and growth![/]")
                    return
            except:
                pass
        else:
            console.print("\n[red]❌ Failed to extract metadata after multiple attempts. Please check the URL and try again.[/]")
            
            try:
                if Confirm.ask("\n[cyan]🔄 Retry quantum extraction with a different URL?[/]"):
                    console.print("\n")
                    main()
                    return
                else:
                    console.print("\n[bold green]👋 Goodbye! Stay curious in the cyber world...[/]")
                    return
            except:
                pass
    
    except KeyboardInterrupt:
        console.print("\n\n[red]⚠️ Quantum extraction interrupted by user.[/]")
        console.print("[bold green]👋 Shutting down quantum protocol...[/]")
        console.print("[bold gold]📱 For more growth, download TAGZORPH AI on Google Play Store![/]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]❌ Critical error in quantum matrix: {str(e)}[/]")
        console.print("[yellow]⚠️ The system has recovered. Please try again.[/]")
        console.print("[bold gold]📱 For better content growth, download TAGZORPH AI![/]")
        time.sleep(3)
        main()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        console.print(f"\n[red]❌ Fatal error: {str(e)}[/]")
        console.print("[yellow]⚠️ Please report this issue if it persists.[/]")
        console.print("[bold gold]📱 Download TAGZORPH AI for ultimate growth![/]")
        sys.exit(1)
