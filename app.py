import streamlit as st
import shaped

# Initialize Shaped.AI API Key
API_KEY = "dQRowDdtmU4mCZdHyKALGGvYJxOo9Mw9Ye5bR544"

# Define client
client = shaped.Client(api_key=API_KEY)

def get_recommendations(user_id):
    """Fetch recommendations for a given user ID."""
    try:
        config = {
            "exploration_factor": 0.1,
            "diversity_factor": 0.1,
            "retrieval_k": 600,
            "retrieval_k_override": {
                "knn": 300,
                "chronological": 0,
                "toplist": 0,
                "trending": 300,
                "random": 0,
                "cold_start": 0,
            },
            "limit": 5,
        }
        response = client.rank(
            model_name="h_and_m_product_recs_demo",
            user_id=user_id,
            return_metadata=True,
            config=config,
        )
        return response
    except Exception as e:
        return {"error": str(e)}

def get_similar_items(item_id):
    """Fetch similar items for a given item ID."""
    try:
        config = {
            "exploration_factor": 0.1,
            "diversity_factor": 0.1,
            "retrieval_k": 600,
            "retrieval_k_override": {
                "knn": 300,
                "chronological": 0,
                "toplist": 0,
                "trending": 300,
                "random": 0,
                "cold_start": 0,
            },
            "limit": 5,
        }
        similar = client.similar_items(
            model_name="h_and_m_product_recs_demo",
            item_id=item_id,
            return_metadata=True,
            config=config,
        )
        return similar
    except Exception as e:
        return {"error": str(e)}

# Streamlit UI
def main():
    st.title("Shaped.AI Product Recommendations")

    # CSS for box styling
    st.markdown(
        """
        <style>
        .box {
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 10px;
            margin: 10px;
            text-align: center;
            box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
        }
        .box img {
            width: 150px;
            height: auto;
            border-radius: 5px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Input user ID for recommendations
    st.header("Get Recommendations for a User")
    user_id = st.text_input("Enter User ID:")

    if st.button("Generate Recommendations"):
        if user_id:
            response = get_recommendations(user_id)
            resp_dict = response.to_dict()

            if 'metadata' in resp_dict and len(resp_dict['metadata']) > 0:
                st.subheader("Recommended Products")
                cols = st.columns(5)  # Create five columns for displaying products

                for idx, item in enumerate(resp_dict['metadata']):
                    image_url = item.get('image', None)
                    product_name = item.get('product_name', 'No name available')
                    description = item.get('description', 'No description available')

                    with cols[idx % 5]:
                        st.markdown(
                            f"""
                            <div class='box'>
                                <img src='{image_url}' alt='Product Image'>
                                <h4>{product_name}</h4>
                                <p>{description}</p>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
            else:
                st.error("No metadata or image data available.")
        else:
            st.error("Please enter a valid User ID.")

    # Input item ID for similar items
    st.header("Find Similar Items")
    item_id = st.text_input("Enter Item ID:")

    if st.button("Find Similar Items"):
        if item_id:
            similar = get_similar_items(item_id)
            resp_dict = similar.to_dict()

            if 'metadata' in resp_dict and len(resp_dict['metadata']) > 0:
                st.subheader("Similar Items")
                cols = st.columns(5)  # Create five columns for displaying similar items

                for idx, item in enumerate(resp_dict['metadata']):
                    image_url = item.get('image', None)
                    product_name = item.get('product_name', 'No name available')
                    description = item.get('description', 'No description available')

                    with cols[idx % 5]:
                        st.markdown(
                            f"""
                            <div class='box'>
                                <img src='{image_url}' alt='Product Image'>
                                <h4>{product_name}</h4>
                                <p>{description}</p>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
            else:
                st.error("No metadata or image data available.")
        else:
            st.error("Please enter a valid Item ID.")

if __name__ == "__main__":
    main()
