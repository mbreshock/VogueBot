# load libraries
import pandas as pd
import yaml
import json
import shaped
import os

# initalize Yujian's Shaped.AI API Key
API_KEY = "dQRowDdtmU4mCZdHyKALGGvYJxOo9Mw9Ye5bR544"

# Define client
client = shaped.Client(api_key=API_KEY)

# Make a request to the shaped API
# return a list of relevant items for a given user.
response = client.rank(
    model_name="h_and_m_product_recs_demo",
    user_id="a8f8851c9ca25414947073f42a377d522c89aeb3ce5769b2c2dbaa5bc7e7c2ee",
    return_metadata=True,
    config=shaped.InferenceConfig(
        exploration_factor=0.1,
        diversity_factor=0.1,
        retrieval_k=600,
        retrieval_k_override=shaped.RetrieverTopKOverride(
            knn=300,
            chronological=0,
            toplist=0,
            trending=300,
            random=0,
            cold_start=0,
        ),
        limit=5,
    ),
)

print(response)

# similar items for a candidate item_id
similar = client.similar_items(
    model_name="h_and_m_product_recs_demo", 
    item_id="783346030",
    return_metadata=True,
    config=shaped.InferenceConfig(
        exploration_factor=0.1,
        diversity_factor=0.1,
        retrieval_k=600,
        retrieval_k_override=shaped.RetrieverTopKOverride(
            knn=300,
            chronological=0,
            toplist=0,
            trending=300,
            random=0,
            cold_start=0,
        ),
        limit=5,
    ),
)

print(similar)
dict = similar.to_dict()

dict['metadata'][1]['image']