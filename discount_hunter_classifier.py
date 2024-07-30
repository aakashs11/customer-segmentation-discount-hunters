"""
This service classifies the discount hunter based on the user's purchase history.
Input: Dataframe containing order data for a customer.
Output: A dictionary containing the following
        - is_discount_hunter: Boolean indicating whether the customer is a discount hunter.
        - score: Weighted score based on the provided metrics.
        - duf: Discount Usage Frequency (DUF) value.
        - discount_proportion: Discount Proportion value.
        - pfds: Purchase Frequency During Sales (PFDS) value.
        - dscaf: Discount Sensitive Cart Abandonment Frequency (DSCAF) value.
"""

import pandas as pd

def calculate_duf(orders):
    """
    Calculates the Discount Usage Frequency (DUF) for a customer.

    Args:
        orders: A list of dictionaries containing the following keys:
            - order_id
            - customer_id
            - discount_applied (boolean or amount)

    Returns:
        float: DUF value.
    """
    df = pd.DataFrame(orders)
    # Filter orders with discounts
    discounted_orders = df[df['discount_applied'] > 0]
    # Count orders
    total_orders = len(df)
    # Count discounted orders
    discounted_order_count = len(discounted_orders)
    # Calculate DUF
    duf = discounted_order_count / total_orders if total_orders > 0 else 0
    return duf

def calculate_dscaf(orders):
    """
    Calculates the Discount Sensitive Cart Abandonment Frequency (DSCAF) for a customer.

    Args:
        orders: A list of dictionaries containing the following keys:
            - cart_id: Unique identifier for each cart.
            - customer_id: Unique identifier for each customer.
            - cart_status: Indicates whether the cart was 'abandoned' or 'completed'.
            - discount_viewed: Boolean indicating whether a discount was viewed in the cart.

    Returns:
        float: DSCAF value.
    """
    df = pd.DataFrame(orders)
    # Handle missing values
    df = df.fillna({
        'cart_status': 'completed',  # Assume missing cart_status means completed (not abandoned)
        'discount_viewed': False    # Assume missing discount_viewed means no discount was viewed
    })
    df['discount_viewed'] = df['discount_viewed'].astype(bool)

    # Filter relevant carts (abandoned and discount viewed)
    abandoned_discount_viewed = df[
        (df['cart_status'] == 'abandoned') & (df['discount_viewed'])
    ]

    # Filter all carts where a discount was viewed
    all_discount_viewed = df[df['discount_viewed']]

    # Count occurrences
    abandoned_count = len(abandoned_discount_viewed)
    total_count = len(all_discount_viewed)

    # Calculate DSCAF
    dscaf = abandoned_count / total_count if total_count > 0 else 0
    print("DSCAF: ", dscaf)
    return dscaf

def calculate_discount_proportion(orders):
    """
    Calculates the Discount Proportion for a customer.

    Args:
        orders: A list of dictionaries containing the following keys:
            - order_id: Unique identifier for each order
            - item_id: Unique identifier for each item within an order
            - discount_applied: Indicates whether a discount was applied to an item
                (True, False, or a numerical discount amount)

    Returns:
        float: Discount proportion value.
    """
    df = pd.DataFrame(orders)
    df["discount_applied"] = df["discount_applied"].fillna(0)
    df["is_discounted"] = df["discount_applied"] > 0

    # Calculate discount proportion
    discount_proportion = df["is_discounted"].mean() if len(df) > 0 else 0
    print("Discount Proportion: ", discount_proportion)
    return discount_proportion

def calculate_pfds(orders):
    """
    Calculates the Purchase Frequency During Sales (PFDS) for a customer.

    Args:
        orders: A list of dictionaries containing the following keys:
            - order_id: Unique identifier for each order
            - customer_id: Unique identifier for each customer
            - order_date: Datetime value indicating the date of purchase
            - sale_period: Boolean (True/False) or datetime range 
                           indicating whether the purchase was made during a sale

    Returns:
        float: PFDS value.
    """
    df = pd.DataFrame(orders)
    df['sale_period'] = df['sale_period'].fillna(False)

    if pd.api.types.is_datetime64_any_dtype(df['sale_period']):
        df['sale_period'] = df['sale_period'].apply(
            lambda x: True if x.left <= df['order_date'] <= x.right else False
        )
    
    # Calculate total purchases
    total_purchases = len(df)
    # Filter to purchases made during sales
    sale_purchases = df[df['sale_period']]

    # Calculate PFDS
    pfds = len(sale_purchases) / total_purchases if total_purchases > 0 else 0
    print("PFDS: ", pfds)
    return pfds
def calculate_discount_hunter_score(metrics):
        """
        Calculates the weighted discount hunter score based on provided metrics.

        Args:
            metrics: A list of metric values in the order:
                - Discount Usage Frequency (DUF)
                - Discount items Proportion
                - Purchase Frequency During Sales (PFDS)
                - Discount Sensitive Cart Abandonment Frequency (DSCAF)

        Returns:
            float: Weighted discount hunter score.
        """
        metric_weights = {
            'Discount Usage Frequency (DUF)': 0.7,
            'Discount items Proportion': 0.4,
            'Purchase Frequency During Sales (PFDS)': 0.5,
            'Discount Sensitive Cart Abandonment Frequency (DSCAF)': -0.5 # Negative weight as it indicates non-discount behavior
        }

        # Normalize weights to ensure they sum to 1
        total_weight = sum(metric_weights.values())
        normalized_weights = {k: v / total_weight for k, v in metric_weights.items()}

        weighted_score = (
            normalized_weights['Discount Usage Frequency (DUF)'] * metrics[0] +
            normalized_weights['Discount items Proportion'] * metrics[1] +
            normalized_weights['Purchase Frequency During Sales (PFDS)'] * metrics[2] +
            normalized_weights['Discount Sensitive Cart Abandonment Frequency (DSCAF)'] * metrics[3]
        )
        return weighted_score

def run(orders):
     
    # Calculate the metrics
    duf = calculate_duf(orders)
    discount_proportion = calculate_discount_proportion(orders)
    pfds = calculate_pfds(orders)
    dscaf = calculate_dscaf(orders)
    print("Metrics: ", duf, discount_proportion, pfds, dscaf)
    
    # Combine the metrics
    metrics = [duf, discount_proportion, pfds, dscaf]
    
    # Calculate the weighted score
    score = calculate_discount_hunter_score(metrics)
    print("Score: ", score)
    # Flag customers based on score
    is_discount_hunter = score > 0.7
    
    # Prepare the output
    output = {'is_discount_hunter': is_discount_hunter,
              'score': score,
              'duf': duf,
              'discount_proportion': discount_proportion,
              'pfds': pfds,
              'dscaf': dscaf}
    
    return output