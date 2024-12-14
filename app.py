from flask import Flask, render_template, request, redirect, url_for
import requests
import shaped

app = Flask(__name__)

DEFAULT_ID_CODE = "783346030"  # Default ID code to pre-fill in the input box
API_KEY = "dQRowDdtmU4mCZdHyKALGGvYJxOo9Mw9Ye5bR544" # Yujian's Shaped.AI API Key

# Route for the home page
@app.route("/", methods=["GET", "POST"])
def index():
    products = []
    error_message = None

    if request.method == "POST":
        id_code = request.form.get("id_code", DEFAULT_ID_CODE)  # Get the ID code from the form or use default
        if not id_code:
            error_message = "Please enter an ID code."
        else:
            try:
                # Shaped API call to get the image URL (replace with actual API logic)
                # Define client
                client = shaped.Client(api_key=API_KEY)
                # similar items for a candidate item_id
                response = client.similar_items(
                    model_name="h_and_m_product_recs_demo", 
                    item_id=str(id_code),
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
                # convert response to dictionary
                resp_dict = response.to_dict()
                # get metadata
                meta = resp_dict["metadata"]
                # for each of the 5 responses, create a dictionary of product name, product id, and image url
                for i in range(0, 5):
                    prod_dict = {"product_id": meta[i]['item_id'], 
                                 "product_name": meta[i]['product_name'], 
                                 "image_url": meta[i]['image']}
                    products.append(prod_dict)

            except Exception as e:
                error_message = f"Failed to fetch image: {str(e)}"

    return render_template(
        "index.html", 
        default_id_code=DEFAULT_ID_CODE, 
        products=products, 
        error_message=error_message
    )


if __name__ == "__main__":
    app.run(debug=True)
