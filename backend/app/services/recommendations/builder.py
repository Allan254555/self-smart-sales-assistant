from app.database.clickhouse import get_clickhouse_client
from app.core.config import settings


DDL_PRODUCT_RECO = """
CREATE TABLE IF NOT EXISTS product_reco
(
    productid UInt32,
    reco_productid UInt32,
    score Float64,
    cooc UInt64,
    rank UInt16,
    updated_at DateTime64(3)
)
ENGINE = MergeTree
ORDER BY (productid, rank);
"""

DDL_CATEGORY_TOP = """
CREATE TABLE IF NOT EXISTS category_top_products
(
    categoryid UInt32,
    productid UInt32,
    qty UInt64,
    rank UInt16,
    updated_at DateTime64(3)
)
ENGINE = MergeTree
ORDER BY (categoryid, rank);
"""


def build_category_top_products(year: int, topn: int = 50) -> None:
    """
    Popular products per category (fallback list).
    """
    ch = get_clickhouse_client()
    ch.command(DDL_CATEGORY_TOP)

    # Rebuild (simple approach)
    ch.command("TRUNCATE TABLE category_top_products")

    sql = f"""
    INSERT INTO category_top_products
    WITH
        toDateTime64(now(), 3) AS ts
    SELECT
        p.categoryid AS categoryid,
        s.productid AS productid,
        sum(s.quantity) AS qty,
        toUInt16(row_number() OVER (PARTITION BY p.categoryid ORDER BY sum(s.quantity) DESC)) AS rank,
        ts AS updated_at
    FROM sales s
    INNER JOIN products p ON p.productid = s.productid
    WHERE toYear(s.salesdate) = {year}
    GROUP BY
        p.categoryid, s.productid
    QUALIFY rank <= {topn}
    """
    ch.command(sql)


def build_product_reco_item_item(
    year: int,
    top_per_item: int = 30,
    min_cooc: int = 2
) -> None:
    """
    Item-to-item collaborative filtering using co-occurrence in the same transactionnumber.
    Score uses cosine similarity: cooc / sqrt(cntA * cntB)
    """
    ch = get_clickhouse_client()
    ch.command(DDL_PRODUCT_RECO)

    # Rebuild
    ch.command("TRUNCATE TABLE product_reco")

    # This query:
    # 1) counts how many transactions each product appears in (cnt)
    # 2) counts co-occurrence pairs within same transaction
    # 3) cosine similarity, then top-N per product
    sql = f"""
    INSERT INTO product_reco
    WITH
      toDateTime64(now(), 3) AS ts,

      -- transactions per product
      prod_cnt AS (
        SELECT
          productid,
          countDistinct(transactionnumber) AS tx_cnt
        FROM sales
        WHERE toYear(salesdate) = {year}
        GROUP BY productid
      ),

      -- co-occurrence counts (A,B) within same transaction
      pair_cnt AS (
        SELECT
          a.productid AS productid,
          b.productid AS reco_productid,
          countDistinct(a.transactionnumber) AS cooc
        FROM
          (SELECT transactionnumber, productid
           FROM sales
           WHERE toYear(salesdate) = {year}
           GROUP BY transactionnumber, productid) a
        INNER JOIN
          (SELECT transactionnumber, productid
           FROM sales
           WHERE toYear(salesdate) = {year}
           GROUP BY transactionnumber, productid) b
        ON a.transactionnumber = b.transactionnumber
        WHERE a.productid != b.productid
        GROUP BY a.productid, b.productid
      )

    SELECT
      pc.productid AS productid,
      pc.reco_productid AS reco_productid,
      (pc.cooc / sqrt(toFloat64(ca.tx_cnt) * toFloat64(cb.tx_cnt))) AS score,
      pc.cooc AS cooc,
      toUInt16(row_number() OVER (PARTITION BY pc.productid ORDER BY (pc.cooc / sqrt(toFloat64(ca.tx_cnt) * toFloat64(cb.tx_cnt))) DESC, pc.cooc DESC)) AS rank,
      ts AS updated_at
    FROM pair_cnt pc
    INNER JOIN prod_cnt ca ON ca.productid = pc.productid
    INNER JOIN prod_cnt cb ON cb.productid = pc.reco_productid
    WHERE pc.cooc >= {min_cooc}
    QUALIFY rank <= {top_per_item}
    """
    ch.command(sql)


def build_all() -> None:
    year = settings.RECO_YEAR
    build_category_top_products(year=year, topn=50)
    build_product_reco_item_item(
        year=year,
        top_per_item=settings.RECO_PER_ITEM,
        min_cooc=settings.RECO_MIN_COOC
    )


if __name__ == "__main__":
    build_all()
    print("✅ Recommendation tables built successfully.")
