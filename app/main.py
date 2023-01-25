from typing import List
from fastapi import FastAPI
from cassandra.cqlengine.management import sync_table

from . import(
    db,
    crud,
    config,
    models,
    schema
)

settings = config.get_settings()

app = FastAPI()

@app.on_event("startup")
def on_startup():
    global session
    session = db.get_session()
    sync_table(models.Product)
    sync_table(models.ProductScrapeEvent)

@app.get("/")
def read_index():
    return {"hello":"world", "name":settings.name}

@app.get("/products", response_model=List[schema.ProductListSchema])
def products_list_view():
    return list(models.Product.objects.all())

@app.post("/events/scrape")
def events_scrape_create_view(data:schema.ProductListSchema):
    product, _ = crud.add_scrape_event(data.dict())
    return product

@app.get("/products/{asin}")
def products_deatail_view(asin):
    data = dict(models.Product.objects.get(asin=asin))
    events = list(models.ProductScrapeEvent.objects().filter(asin=asin).limit(5))
    events = [schema.ProductScrapeEventDetailSchema(**x) for x in events]
    data['events'] = events
    data['events_url'] = f"/products/{asin}/events"
    return data

@app.get("/products/{asin}/events", response_model=List[schema.ProductScrapeEventDetailSchema])
def product_scrapes_list_view(asin):
        return list(models.ProductScrapeEvent.objects().filter(asin=asin).limit(5))