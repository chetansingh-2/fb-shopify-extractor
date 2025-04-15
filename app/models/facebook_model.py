from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class FacebookAdSet(BaseModel):
    id: str
    name: str
    campaign_id: str
    daily_budget: Optional[str] = None
    start_time: datetime
    end_time: Optional[datetime] = None
    targeting: Optional[Dict[str, Any]] = None

class FacebookAd(BaseModel):
    id: str
    name: str
    adset_id: str
    status: str
    created_time: datetime

class FacebookInsight(BaseModel):
    date_start: str
    date_stop: str
    campaign_id: Optional[str] = None
    adset_id: Optional[str] = None
    ad_id: Optional[str] = None
    impressions: str
    clicks: str
    spend: str
    cpc: Optional[str] = None
    ctr: Optional[str] = None
    
class FacebookDataResponse(BaseModel):
    adsets: Optional[List[FacebookAdSet]] = None
    ads: Optional[List[FacebookAd]] = None
    insights: Optional[List[FacebookInsight]] = None