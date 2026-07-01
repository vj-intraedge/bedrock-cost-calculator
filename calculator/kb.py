"""
Knowledge Base cost calculator.

Computes monthly costs for:
- Storage (managed vector store)
- Embedding (Titan Text Embedding V2)
- Retrieval queries
- Sync/Ingestion
- Web Crawler
"""

from calculator.models import CostResult
from pricing.aws_pricing import AWSPricingProvider


def calculate_kb_costs(
    provider: AWSPricingProvider,
    sessions_per_month: int,
    messages_per_session: int,
    kb_queries_per_message: int,
    kb_size_gb: float,
    crawl_frequency: str,
    input_tokens_per_message: int,
) -> list[CostResult]:
    """
    Calculate Knowledge Base costs.

    Returns a list of CostResult for each KB cost component.
    """
    kb = provider.get_kb_pricing()
    results = []

    # --- Storage ---
    storage_cost = kb_size_gb * kb.storage_per_gb_month
    results.append(CostResult(
        service="Knowledge Base",
        component="Storage",
        subtotal=storage_cost,
        formula=f"{kb_size_gb} GB × ${kb.storage_per_gb_month}/GB-month = ${storage_cost:.4f}",
        unit_price=f"${kb.storage_per_gb_month}/GB-month",
        usage=f"{kb_size_gb} GB",
        assumptions=["Managed vector store (Bedrock-managed KB)"],
    ))

    # --- Embedding ---
    # Estimate: each GB of raw text produces ~250M tokens when chunked and embedded
    # This is a rough estimate; actual depends on content density
    tokens_per_gb = 250_000_000
    syncs_per_month = {"Daily": 30, "Weekly": 4, "Monthly": 1}[crawl_frequency]

    # Only re-embed on sync (incremental, assume 10% changes per sync)
    change_rate = 0.10
    tokens_to_embed = kb_size_gb * tokens_per_gb * change_rate * syncs_per_month
    embedding_cost = (tokens_to_embed / 1_000_000) * kb.embedding_per_million_tokens
    results.append(CostResult(
        service="Knowledge Base",
        component="Embedding",
        subtotal=embedding_cost,
        formula=(
            f"{kb_size_gb} GB × 250M tokens/GB × {change_rate*100:.0f}% change × "
            f"{syncs_per_month} syncs × ${kb.embedding_per_million_tokens}/M tokens = "
            f"${embedding_cost:.4f}"
        ),
        unit_price=f"${kb.embedding_per_million_tokens}/M tokens (Titan Embedding V2)",
        usage=f"{tokens_to_embed/1_000_000:.1f}M tokens embedded/month",
        assumptions=[
            "~250M tokens per GB of source text",
            f"10% incremental change per sync cycle",
            f"Crawl frequency: {crawl_frequency} ({syncs_per_month} syncs/month)",
        ],
    ))

    # --- Retrieval ---
    total_messages = sessions_per_month * messages_per_session
    total_queries = total_messages * kb_queries_per_message
    retrieval_cost = (total_queries / 1000) * kb.retrieval_per_1000_queries
    results.append(CostResult(
        service="Knowledge Base",
        component="Retrieval",
        subtotal=retrieval_cost,
        formula=(
            f"{sessions_per_month:,} sessions × {messages_per_session} msgs × "
            f"{kb_queries_per_message} queries/msg = {total_queries:,} queries × "
            f"${kb.retrieval_per_1000_queries}/1K = ${retrieval_cost:.4f}"
        ),
        unit_price=f"${kb.retrieval_per_1000_queries}/1,000 queries",
        usage=f"{total_queries:,} queries",
        assumptions=["Retrieve API calls"],
    ))

    # --- Sync/Ingestion ---
    # Estimate number of objects (documents): ~100 per GB
    objects_per_gb = 100
    total_objects = kb_size_gb * objects_per_gb * change_rate * syncs_per_month
    sync_cost = (total_objects / 1000) * kb.sync_per_1000_objects
    results.append(CostResult(
        service="Knowledge Base",
        component="Sync/Ingestion",
        subtotal=sync_cost,
        formula=(
            f"{kb_size_gb} GB × {objects_per_gb} objects/GB × {change_rate*100:.0f}% change × "
            f"{syncs_per_month} syncs = {total_objects:.0f} objects × "
            f"${kb.sync_per_1000_objects}/1K = ${sync_cost:.4f}"
        ),
        unit_price=f"${kb.sync_per_1000_objects}/1,000 objects",
        usage=f"{total_objects:.0f} objects synced/month",
        assumptions=[
            "~100 documents per GB",
            "10% incremental change per sync",
        ],
    ))

    # --- Web Crawler ---
    # Estimate: 10 URLs per document
    urls_per_object = 10
    total_urls = kb_size_gb * objects_per_gb * urls_per_object * change_rate * syncs_per_month
    crawler_cost = (total_urls / 1000) * kb.crawler_per_1000_urls
    results.append(CostResult(
        service="Knowledge Base",
        component="Web Crawler",
        subtotal=crawler_cost,
        formula=(
            f"{kb_size_gb} GB × {objects_per_gb} objects/GB × {urls_per_object} URLs/object × "
            f"{change_rate*100:.0f}% change × {syncs_per_month} syncs = "
            f"{total_urls:.0f} URLs × ${kb.crawler_per_1000_urls}/1K = ${crawler_cost:.4f}"
        ),
        unit_price=f"${kb.crawler_per_1000_urls}/1,000 URLs",
        usage=f"{total_urls:.0f} URLs crawled/month",
        assumptions=[
            "~10 URLs per document (web data source)",
            "Only crawled content incurs this cost",
        ],
    ))

    return results
