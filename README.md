
# End-to-End Gen AI Project Using LangChain, OpenAI in Retail Industry

## Overview
This project showcases an **LLM-powered** application for a retail scenario using:
- LangChain
- HuggingFace
- Streamlit
- ChromaDB
- MySQL

The application allows communication with a SQL database using **natural English language queries**.

---

## Project Requirements
- The store sells 4 brands of T-shirts:
  - Van Heusen
  - Levis
  - Nike
  - Adidas

---

## MySQL Database Schema

### Table: `tshirt`
| tshirt_id | brand       | color  | size | price | stock_quantity |
|-----------|-------------|--------|------|-------|----------------|
| 1         | Levis       | Black  | S    | 19    | 15             |
| 2         | Nike        | White  | S    | 24    | 64             |
| 3         | Adidas      | White  | XS   | 14    | 55             |
| 4         | Van Heusen  | Blue   | XL   | 43    | 60             |
| 5         | Levis       | White  | XL   | 23    | 86             |

### Table: `discounts`
| discount_id | tshirt_id | pct_discount |
|-------------|-----------|--------------|
| 1           | 1         | 10.00        |
| 2           | 2         | 15.00        |
| 3           | 3         | 20.00        |
| 4           | 4         | 5.00         |
| 5           | 5         | 25.00        |

---

## Natural Language Query Examples

### 1. Inventory Query
**Q:** How many white color Nike T-shirts are left in the stock?  
**SQL:**
```sql
SELECT SUM(stock_quantity)
FROM tshirt
WHERE brand = "Nike" AND color = "White";
```

### 2. Revenue After Discounts
**Q:** If we have to sell all the Levi’s T-shirts today with discounts applied, how much revenue will our store generate (post discounts)?  
**SQL:**
```sql
SELECT SUM(a.total_amount * ((100 - COALESCE(discounts.pct_discount, 0)) / 100))
FROM (
  SELECT price * stock_quantity AS total_amount, t_shirt_id
  FROM tshirt
  WHERE brand = "Levis"
) a
LEFT JOIN discounts
ON a.t_shirt_id = discounts.t_shirt_id;
```

### 3. Total Inventory Value for S-size
**Q:** How much is the total price of the inventory for all S-size T-shirts?  
**SQL:**
```sql
SELECT SUM(price * stock_quantity)
FROM tshirt
WHERE size = 'S';
```

---

## Few-Shot Learning Table (Prompt Engineering)

| Natural Language Question                                               | SQL Query Snippet                                                      |
|------------------------------------------------------------------------|------------------------------------------------------------------------|
| How many white Nike t-shirts do we have in stock?                     | `SELECT SUM(stock_quantity) FROM tshirt WHERE brand="Nike" AND color="White"` |
| What is the total inventory value of S-size T-shirts?                 | `SELECT SUM(price*stock_quantity) FROM tshirt WHERE size='S'`         |
| Revenue from selling all Levi's t-shirts after discount?              | `SELECT SUM(...) LEFT JOIN discounts ON ...`                          |

---

## Embedding and Vector Search

Using **HuggingFace Transformers** to convert natural language queries into **embedding vectors**.

Example vectors:
```
[-6.77, 5.4, 0.11, 4.4, ..., 9.81]
[0.23, 1.62, 0.33, 8.31, ..., -1.8]
```

Stored and queried using:
- Vector DB: **ChromaDB (Free)**

---

**Note**: You are the **Manager of the Store** in this project scenario.