from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
from datetime import datetime, timedelta
import json
import math

from backend.app.core.config import settings
from backend.app.services.analytics.queries import fetch_transactions
from backend.app.database.redis_store import get_redis_client