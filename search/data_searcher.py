import pandas as pd
import os
from src.config import MOBILES_CSV_PATH

def search_mobiles(min_price: float = None, 
                   max_price: float = None, 
                   brand: str = None, 
                   title: str = None, 
                   min_storage_gb: int = None,
                   max_storage_gb: int = None,
                   min_rating: float = None) -> str:
    """
    Searches the mobiles dataset based on various criteria.

    Args:
        min_price (float, optional): Minimum price of the phone.
        max_price (float, optional): Maximum price of the phone.
        brand (str, optional): Brand of the phone (e.g., 'Apple', 'Samsung').
        title (str, optional): Specific title or model name of the phone (e.g., 'iPhone 15').
        min_storage_gb (int, optional): Minimum storage in GB.
        max_storage_gb (int, optional): Maximum storage in GB.
        min_rating (float, optional): Minimum rating.

    Returns:
        str: A string summary of matching mobile phones or a message if none are found.
    """
    if not os.path.exists(MOBILES_CSV_PATH):
        return f"Error: Mobiles dataset not found at {MOBILES_CSV_PATH}. Please ensure the file exists."

    try:
        df = pd.read_csv(MOBILES_CSV_PATH)
    except Exception as e:
        return f"Error reading mobiles dataset: {e}"

    filtered_df = df.copy()
    if min_price is not None:
        filtered_df = filtered_df[filtered_df['price'] >= min_price]
    if max_price is not None:
        filtered_df = filtered_df[filtered_df['price'] <= max_price]
    if brand:
        filtered_df = filtered_df[filtered_df['brand'].str.contains(brand, case=False, na=False)]
    if title:
        filtered_df = filtered_df[filtered_df['title'].str.contains(title, case=False, na=False)]
    if min_storage_gb is not None:
        filtered_df = filtered_df[filtered_df['storage_gb'] >= min_storage_gb]
    if max_storage_gb is not None:
        filtered_df = filtered_df[filtered_df['storage_gb'] <= max_storage_gb]
    if min_rating is not None:
        filtered_df = filtered_df[filtered_df['rating'] >= min_rating]

    if filtered_df.empty:
        return "No mobile phones found matching the specified criteria."
    else:
        results = []
        for index, row in filtered_df.head(5).iterrows():
            results.append(f"{row['title']} ({row['brand']}): ${row['price']}, {row['storage_gb']}GB, Rating: {row['rating']}")
        
        summary = f"Found {len(filtered_df)} matching phones. Here are a few:\n" + "\n".join(results)
        if len(filtered_df) > 5:
            summary += f"\n...and {len(filtered_df) - 5} more."
        return summary

# Example usage (for testing this module directly)
if __name__ == "__main__":
    # Ensure data directory exists and mobiles.csv is there for testing
    if not os.path.exists(os.path.dirname(MOBILES_CSV_PATH)):
        os.makedirs(os.path.dirname(MOBILES_CSV_PATH))
    # You might want to programmatically create a dummy mobiles.csv here for robust testing
    # if not os.path.exists(MOBILES_CSV_PATH):
    #     dummy_data = """title,brand,price,rating,storage_gb
    #     iPhone 15 Pro Max,Apple,1199,4.9,256
    #     Samsung Galaxy S24 Ultra,Samsung,1299,4.8,512
    #     """
    #     with open(MOBILES_CSV_PATH, "w") as f:
    #         f.write(dummy_data)


    print("--- Testing search_mobiles function ---")
    print("\nSearching for iPhones under $800:")
    print(search_mobiles(brand="Apple", max_price=800))

    print("\nSearching for Samsung phones with at least 256GB storage:")
    print(search_mobiles(brand="Samsung", min_storage_gb=256))

    print("\nSearching for phones between $400 and $700:")
    print(search_mobiles(min_price=400, max_price=700))

    print("\nSearching for 'Pixel' phones:")
    print(search_mobiles(title="Pixel"))

    print("\nSearching for non-existent criteria:")
    print(search_mobiles(brand="Sony"))
