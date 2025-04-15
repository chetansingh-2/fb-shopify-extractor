from fastapi import APIRouter, Query, HTTPException, Depends
from typing import Optional
from app.services.shopify_service import ShopifyService
from app.services.facebook_service import FacebookAdsService
from app.models.shopify_model import ShopifyDataResponse
from app.models.facebook_model import FacebookDataResponse

router = APIRouter()


## inject dependecy here

def get_shopify_service():
    service = ShopifyService()
    service.authenticate()
    return service

def get_facebook_service():
    return FacebookAdsService()

# Shopify endpoints
@router.get("/shopify/products", response_model=ShopifyDataResponse)
async def get_shopify_products(
    limit: int = Query(50, description="Maximum number of products to retrieve"),
    shopify_service: ShopifyService = Depends(get_shopify_service)
):
    try:
        products = shopify_service.get_products(limit=limit)
        return ShopifyDataResponse(products=products)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching Shopify products: {str(e)}")



@router.get("/shopify/orders", response_model=ShopifyDataResponse)
async def get_shopify_orders(
    days: int = Query(30, description="Number of days to look back"),
    limit: int = Query(50, description="Maximum number of orders to retrieve"),
    shopify_service: ShopifyService = Depends(get_shopify_service)
):
    try:
        orders = shopify_service.get_orders(days=days, limit=limit)
        return ShopifyDataResponse(orders=orders)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching Shopify orders: {str(e)}")



@router.get("/facebook/adsets", response_model=FacebookDataResponse)
async def get_facebook_adsets(
    limit: int = Query(50, description="Maximum number of ad sets to retrieve"),
    facebook_service: FacebookAdsService = Depends(get_facebook_service)
):
    try:
        adsets = facebook_service.get_adsets(limit=limit)
        return FacebookDataResponse(adsets=adsets)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching Facebook ad sets: {str(e)}")

@router.get("/facebook/ads", response_model=FacebookDataResponse)
async def get_facebook_ads(
    limit: int = Query(50, description="Maximum number of ads to retrieve"),
    facebook_service: FacebookAdsService = Depends(get_facebook_service)
):
    try:
        ads = facebook_service.get_ads(limit=limit)
        return FacebookDataResponse(ads=ads)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching Facebook ads: {str(e)}")

@router.get("/facebook/insights", response_model=FacebookDataResponse)
async def get_facebook_insights(
    days: int = Query(30, description="Number of days to look back"),
    level: str = Query("account", description="Level of insights: account, campaign, adset, or ad"),
    facebook_service: FacebookAdsService = Depends(get_facebook_service)
):
    try:
        insights = facebook_service.get_insights(days=days, level=level)
        return FacebookDataResponse(insights=insights)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching Facebook insights: {str(e)}")


@router.get("/combined-data")
async def get_combined_data(
    product_limit: int = Query(50, description="Maximum number of Shopify products"),
    order_days: int = Query(30, description="Days to look back for Shopify orders"),
    order_limit: int = Query(50, description="Maximum number of Shopify orders"),
    fb_adset_limit: int = Query(50, description="Maximum number of Facebook ad sets"),
    fb_ad_limit: int = Query(50, description="Maximum number of Facebook ads"),
    fb_insight_days: int = Query(30, description="Days to look back for Facebook insights"),
    fb_insight_level: str = Query("account", description="Level for Facebook insights"),
    shopify_service: ShopifyService = Depends(get_shopify_service),
    facebook_service: FacebookAdsService = Depends(get_facebook_service)
):
    try:
        products = shopify_service.get_products(limit=product_limit)
        orders = shopify_service.get_orders(days=order_days, limit=order_limit)
        adsets = facebook_service.get_adsets(limit=fb_adset_limit)
        ads = facebook_service.get_ads(limit=fb_ad_limit)
        insights = facebook_service.get_insights(days=fb_insight_days, level=fb_insight_level)
        
        return {
            "shopify": {
                "products": [p.dict() for p in products],
                "orders": [o.dict() for o in orders]
            },
            "facebook": {
                "adsets": [a.dict() for a in adsets],
                "ads": [a.dict() for a in ads],
                "insights": [i.dict() for i in insights]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching combined data: {str(e)}")