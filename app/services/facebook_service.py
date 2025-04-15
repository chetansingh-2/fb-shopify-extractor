from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adsinsights import AdsInsights
from datetime import datetime, timedelta
from ..config import FB_APP_ID, FB_APP_SECRET, FB_ACCESS_TOKEN, FB_AD_ACCOUNT_ID
from ..models.facebook_model import FacebookAdSet, FacebookAd, FacebookInsight

class FacebookAdsService:
    def __init__(self):
        self.api = FacebookAdsApi.init(app_id=FB_APP_ID, 
                                      app_secret=FB_APP_SECRET, 
                                      access_token=FB_ACCESS_TOKEN)
        self.account = AdAccount(FB_AD_ACCOUNT_ID)
        
    def get_adsets(self, limit=50):
        adsets_data = []
        fields = [
            'id',
            'name',
            'campaign_id',
            'daily_budget',
            'start_time',
            'end_time',
            'targeting'
        ]
        
        # FIXED: Use params dictionary for limit instead of direct argument
        params = {
            'limit': limit
        }
        
        # Correct way to pass limit parameter
        adsets = self.account.get_ad_sets(fields=fields, params=params)
        
        for adset in adsets:
            adset_dict = adset.export_all_data()
            adsets_data.append(FacebookAdSet(
                id=adset_dict['id'],
                name=adset_dict['name'],
                campaign_id=adset_dict['campaign_id'],
                daily_budget=adset_dict.get('daily_budget'),
                start_time=datetime.strptime(adset_dict['start_time'], '%Y-%m-%dT%H:%M:%S%z'),
                end_time=datetime.strptime(adset_dict['end_time'], '%Y-%m-%dT%H:%M:%S%z') 
                    if adset_dict.get('end_time') else None,
                targeting=adset_dict.get('targeting')
            ))
            
        return adsets_data
    
    def get_ads(self, limit=50):
        ads_data = []
        fields = [
            'id',
            'name',
            'adset_id',
            'status',
            'created_time'
        ]
        
        params = {
            'limit': limit
        }
        
        ads = self.account.get_ads(fields=fields, params=params)
        
        for ad in ads:
            ad_dict = ad.export_all_data()
            ads_data.append(FacebookAd(
                id=ad_dict['id'],
                name=ad_dict['name'],
                adset_id=ad_dict['adset_id'],
                status=ad_dict['status'],
                created_time=datetime.strptime(ad_dict['created_time'], '%Y-%m-%dT%H:%M:%S%z')
            ))
            
        return ads_data
    
    def get_insights(self, days=30, level='account'):
        insights_data = []
        
        fields = [
            'date_start',
            'date_stop',
            'impressions',
            'clicks',
            'spend',
            'cpc',
            'ctr'
        ]
        
        if level in ['campaign', 'adset', 'ad']:
            fields.append(f'{level}_id')
        
        date_preset = 'last_30d' if days == 30 else 'last_7d' if days == 7 else 'yesterday'
        
        params = {
            'level': level,
            'date_preset': date_preset,
            'time_increment': 1  
        }
        
        insights = self.account.get_insights(fields=fields, params=params)
        
        for insight in insights:
            insight_dict = insight.export_all_data()
            
            additional_fields = {}
            if level == 'campaign':
                additional_fields['campaign_id'] = insight_dict.get('campaign_id')
            elif level == 'adset':
                additional_fields['adset_id'] = insight_dict.get('adset_id')
            elif level == 'ad':
                additional_fields['ad_id'] = insight_dict.get('ad_id')
            
            insights_data.append(FacebookInsight(
                date_start=insight_dict['date_start'],
                date_stop=insight_dict['date_stop'],
                impressions=insight_dict['impressions'],
                clicks=insight_dict['clicks'],
                spend=insight_dict['spend'],
                cpc=insight_dict.get('cpc'),
                ctr=insight_dict.get('ctr'),
                **additional_fields
            ))
            
        return insights_data