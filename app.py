from flask import Flask, render_template, request, redirect, url_for
import requests
import shaped

app = Flask(__name__)

# Route for the home page
@app.route("/", methods=["GET", "POST"])
def index():
    image_url = None
    error_message = None
    API_KEY = "dQRowDdtmU4mCZdHyKALGGvYJxOo9Mw9Ye5bR544"

    if request.method == "POST":
        id_code = request.form.get("id_code")  # Get the ID code from the form
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
                resp_dict = response.to_dict()
                image_url = resp_dict['metadata'][1]['image']

            except Exception as e:
                error_message = f"Failed to fetch image: {str(e)}"

    return render_template("index.html", image_url=image_url, error_message=error_message)


if __name__ == "__main__":
    app.run(debug=True)
