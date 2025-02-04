# Discount Hunter Classifier with Time Decay Factor

This repository provides a set of Python scripts and functions to classify customers as "Discount Hunters" based on their purchase history. The classifier incorporates a time decay factor into various metrics so that recent transactions have a higher impact on the final score. It calculates a weighted score using several key metrics, and flags a customer as a discount hunter if the score exceeds a predefined threshold (0.7 by default).

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technical Details](#technical-details)
  - [Time Decay Factor & Weighted Metrics](#time-decay-factor--weighted-metrics)
  - [Metric Calculations](#metric-calculations)
- [Usage](#usage)
- [Example Output](#example-output)
- [Installation](#installation)
- [License](#license)

---

## Overview

The Discount Hunter Classifier analyzes customer purchase data to determine whether a customer exhibits discount-hunting behavior. By applying an exponential time decay factor, the classifier weights recent orders more heavily than older ones. Key metrics computed include:

- **Discount Usage Frequency (DUF):** The ratio of orders with discounts to total orders.
- **Discount Proportion:** The proportion of items purchased with a discount.
- **Purchase Frequency During Sales (PFDS):** The ratio of purchases made during sale periods.
- **Discount Sensitive Cart Abandonment Frequency (DSCAF):** The ratio of carts abandoned (with discount views) to total carts where discounts were viewed.

These metrics are combined using predefined weights to generate a final score. A customer is classified as a discount hunter if the score exceeds 0.7.

---

## Features

- **Time Decay Factor:** Applies exponential decay to metric values based on the number of days since the most recent purchase.
- **Metric Computation:** Calculates several metrics including DUF, Discount Proportion, PFDS, and DSCAF.
- **Weighted Scoring:** Combines normalized metrics using specific weights to compute a final Discount Hunter Score.
- **Classification:** Flags customers as discount hunters if their weighted score is above a threshold.
- **CSV Integration:** Supports reading customer order data from CSV files and saving classification results.

---

## Technical Details

### Time Decay Factor & Weighted Metrics

A time decay factor is applied so that more recent transactions contribute more heavily. The decay is calculated as follows:

\[
\text{Time Decay Weight} = e^{-0.005 \times (\text{Days Since Most Recent Purchase})}
\]

Each metric (e.g., DUF, DSR, PFDS) is multiplied by this weight to yield a weighted metric that reflects the recency of purchases.

### Metric Calculations

The following functions are implemented:

- **calculate_duf(orders):**  
  Computes the Discount Usage Frequency (DUF) as the ratio of orders with discounts to total orders.
  
- **calculate_discount_proportion(orders):**  
  Determines the proportion of items purchased with a discount.

- **calculate_pfds(orders):**  
  Calculates the Purchase Frequency During Sales (PFDS) by dividing the number of sale purchases by the total number of purchases.

- **calculate_dscaf(orders):**  
  Computes the Discount Sensitive Cart Abandonment Frequency (DSCAF) as the ratio of carts that were abandoned (when discounts were viewed) to the total number of carts with a discount view.

- **calculate_discount_hunter_score(metrics):**  
  Combines the metrics using the following weights:
  - Discount Usage Frequency (DUF): 0.7
  - Discount Proportion: 0.4
  - PFDS: 0.5
  - DSCAF: -0.5 (negative weight as a higher DSCAF indicates less discount-hunting behavior)

  The weighted score is calculated by normalizing the weights and summing the product of each metric with its respective normalized weight.

- **run(orders):**  
  A wrapper function that:
  1. Calculates the individual metrics (DUF, Discount Proportion, PFDS, DSCAF) for a given list of orders.
  2. Computes the final weighted Discount Hunter Score.
  3. Flags the customer as a discount hunter if the score exceeds 0.7.
  4. Returns a dictionary with the score and metric values.

---


# Discount hunter classification

## Requirements

Python, pandas, jupyter notebooks

## Description

This repository contains the code and documentation for the classifying a customer as Discount hunter.


- [Files](#files)
- [Usage](#usage)
- [Links](#links)


## Files

- [notebook_metrics.ipynb](notebook_metrics.ipynb) - Jupyter notebook for calculating the metrics. 
- [notebook_enhancements.ipynb](notebook_enhancements.ipynb) - Demonstration of enhancements.
- [outputs.csv](outputs.csv) - customer data with added column 'is_discount_hunter'
- [synthetic_ecommerce_data.csv](sample_data.csv) - synthetic e-commerce customer data with 100 rows and 23 columns. Total 45 unique customers.
- [discount_hunter_classifier.py](discount_hunter_classifier.py) - service returning classification data
- [run.ipynb](run.ipynb) - testing the classifier

## Usage

1. Solution is present in the py file
2. It can be tested using [run.ipynb](run.ipynb)
3. Files are supported with comments for easier understanding

## Links
- [Solution slider] (https://docs.google.com/presentation/d/1ioUV64F-lU-ZNgajkupVulQ0fDnKCKL-k8L3Zzsu3iE/edit?usp=sharing)
- [Feature Analysis] (https://docs.google.com/spreadsheets/d/1PGuOcqOnnwy_Kva14mnztT58GGTJvZBNfo21Ue2Xqzs/edit?gid=1278169757#gid=1278169757)
- [Drive Link] (https://drive.google.com/drive/folders/1eZYJ50HUygwwyr0SkuBwch3E32GbLcJT?usp=sharing) 
